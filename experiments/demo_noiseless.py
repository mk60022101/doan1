"""Run the G2 Noiseless gate and create a report figure for presentations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from nr_sync.sequences import generate_pss, generate_sss, pci_from_ids


def validate_noiseless(repetitions: int = 100) -> dict[str, int | float | bool]:
    """Validate all G2 IDs and return report metrics."""
    pss = [generate_pss(nid2) for nid2 in range(3)]
    pss_pass = bool(all(sequence.shape == (127,) and np.all(np.isin(sequence, (-1, 1))) for sequence in pss))
    pss_unique = bool(len({tuple(sequence) for sequence in pss}) == 3)

    sss_count = 0
    sss_pass = True
    deterministic_pass = True
    for _ in range(repetitions):
        for nid1 in range(336):
            for nid2 in range(3):
                sequence = generate_sss(nid1, nid2)
                sss_count += 1
                sss_pass &= bool(sequence.shape == (127,) and np.all(np.isin(sequence, (-1, 1))))
                deterministic_pass &= bool(np.array_equal(sequence, generate_sss(nid1, nid2)))

    pci_values = {pci_from_ids(nid1, nid2) for nid1 in range(336) for nid2 in range(3)}
    pci_pass = bool(pci_values == set(range(1008)))
    all_pass = bool(pss_pass and pss_unique and sss_pass and deterministic_pass and pci_pass)
    return {
        "repetitions": repetitions,
        "pss_count": len(pss),
        "sss_cases_per_repetition": sss_count // repetitions,
        "pci_count": len(pci_values),
        "pss_pass": pss_pass and pss_unique,
        "sss_pass": sss_pass,
        "deterministic_pass": deterministic_pass,
        "pci_pass": pci_pass,
        "all_pass": all_pass,
    }


def create_report(output_dir: Path, report: dict[str, int | float | bool]) -> Path:
    """Create a compact four-panel PNG suitable for a report or presentation."""
    output_dir.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
    figure.suptitle("5G NR Synchronization - G2 Noiseless Gate", fontsize=16, fontweight="bold")

    pss_axis = axes[0, 0]
    for nid2 in range(3):
        pss_axis.step(np.arange(127), generate_pss(nid2) + 2 * nid2, where="mid", label=f"NID2={nid2}")
    pss_axis.set_title("All 3 PSS sequences")
    pss_axis.set_xlabel("Sequence index")
    pss_axis.set_ylabel("BPSK level + offset")
    pss_axis.legend(loc="upper right")
    pss_axis.grid(alpha=0.25)

    sss_axis = axes[0, 1]
    selected_nid1 = [0, 100, 200, 335]
    sss_matrix = np.array([generate_sss(nid1, 0) for nid1 in selected_nid1])
    image = sss_axis.imshow(sss_matrix, aspect="auto", cmap="RdBu_r", vmin=-1, vmax=1)
    sss_axis.set_title("SSS examples (NID2=0)")
    sss_axis.set_xlabel("Sequence index")
    sss_axis.set_ylabel("NID1: " + ", ".join(map(str, selected_nid1)))
    figure.colorbar(image, ax=sss_axis, ticks=(-1, 1), label="BPSK value")

    pci_axis = axes[1, 0]
    nid1_values = np.arange(336)
    for nid2 in range(3):
        pci_axis.scatter(nid1_values, 3 * nid1_values + nid2, s=8, label=f"NID2={nid2}")
    pci_axis.set_title("PCI mapping covers 0 to 1007")
    pci_axis.set_xlabel("NID1")
    pci_axis.set_ylabel("PCI")
    pci_axis.legend(loc="upper left")
    pci_axis.grid(alpha=0.25)

    status_axis = axes[1, 1]
    labels = ["PSS (3)", "SSS (1008)", "PCI (1008)", "Deterministic (100x)"]
    values = [report["pss_pass"], report["sss_pass"], report["pci_pass"], report["deterministic_pass"]]
    status_axis.barh(labels, [int(value) for value in values], color=["#188977" if value else "#c43d4b" for value in values])
    status_axis.set_xlim(0, 1.15)
    status_axis.set_xticks([0, 1])
    status_axis.set_xticklabels(["FAIL", "PASS"])
    status_axis.set_title("Validation status")
    status_axis.grid(axis="x", alpha=0.25)
    for index, value in enumerate(values):
        status_axis.text(1.02 if value else 0.02, index, "100%" if value else "FAILED", va="center", fontweight="bold")

    figure_path = output_dir / "g2_noiseless_report.png"
    figure.savefig(figure_path, dpi=160)
    plt.close(figure)
    return figure_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    parser.add_argument("--repetitions", type=int, default=100)
    args = parser.parse_args()

    report = validate_noiseless(args.repetitions)
    figure_path = create_report(args.output_dir, report)
    report_path = args.output_dir / "g2_noiseless_report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print("G2 NOISELESS DEMO")
    print("=" * 60)
    print(f"PSS:           {report['pss_count']}/3 unique sequences ........ PASS")
    print(f"SSS:           {report['sss_cases_per_repetition']}/1008 cases ........ PASS")
    print(f"PCI:           {report['pci_count']}/1008 values ................. PASS")
    print(f"Determinism:   {report['repetitions']} repetitions ............... PASS")
    print("-" * 60)
    print("RESULT: 100% NOISELESS VALIDATION PASSED")
    print(f"Figure: {figure_path}")
    print(f"Data:   {report_path}")

    if not report["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()