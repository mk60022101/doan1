"""Smoke and noiseless exhaustive tests for the module contract."""

import numpy as np

from nr_sync import channel, metrics, ofdm, sequences, synchronizer


def test_modules_import():
    assert all((channel, metrics, ofdm, sequences, synchronizer))


def test_pss_sss_pci_noiseless_exhaustive_100_repetitions():
    """C1/C3 gate: every valid ID is deterministic and valid for 100 runs."""
    pss_sequences = {tuple(sequences.generate_pss(nid2)) for nid2 in range(3)}
    assert len(pss_sequences) == 3

    for _ in range(100):
        for nid2 in range(3):
            pss = sequences.generate_pss(nid2)
            assert pss.shape == (127,)
            assert np.all(np.isin(pss, (-1, 1)))
            assert np.array_equal(pss, sequences.generate_pss(nid2))

        for nid1 in range(336):
            for nid2 in range(3):
                sss = sequences.generate_sss(nid1, nid2)
                assert sss.shape == (127,)
                assert np.all(np.isin(sss, (-1, 1)))
                assert np.array_equal(sss, sequences.generate_sss(nid1, nid2))
                assert sequences.pci_from_ids(nid1, nid2) == 3 * nid1 + nid2


def test_pci_covers_all_1008_values():
    pci_values = {
        sequences.pci_from_ids(nid1, nid2)
        for nid1 in range(336)
        for nid2 in range(3)
    }
    assert pci_values == set(range(1008))
