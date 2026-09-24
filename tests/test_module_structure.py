"""Independent reference and noiseless tests for the sequence generators."""

import hashlib

import numpy as np

from nr_sync import channel, metrics, ofdm, sequences, synchronizer


def _reference_m_sequence(taps, initial_state):
    """Small independent transcription of the TS 38.211 binary recurrence."""
    values = list(initial_state)
    for index in range(127):
        values.append(sum(values[index + tap] for tap in taps) % 2)
    return np.asarray(values[7:134], dtype=np.int8)


def _reference_pss(nid2):
    x = _reference_m_sequence((0, 4), (0, 1, 1, 0, 1, 1, 1))
    return (1 - 2 * x[(np.arange(127) + 43 * nid2) % 127]).astype(np.int8)


def _reference_sss(nid1, nid2):
    x0 = _reference_m_sequence((0, 4), (1, 0, 0, 0, 0, 0, 0))
    x1 = _reference_m_sequence((0, 1), (1, 0, 0, 0, 0, 0, 0))
    m0 = 15 * (nid1 // 112) + 5 * nid2
    m1 = nid1 % 112
    result = np.empty(127, dtype=np.int8)
    for n in range(64):
        result[2 * n] = (1 - 2 * x0[(n + m0) % 127]) * (1 - 2 * x1[(n + m1) % 127])
    for n in range(63):
        result[2 * n + 1] = (1 - 2 * x0[(n + m1) % 127]) * (1 - 2 * x1[(n + m0) % 127])
    return result


def test_modules_import():
    assert all((channel, metrics, ofdm, sequences, synchronizer))


def test_sequences_match_fixed_reference_vectors():
    """Catch formula regressions, not just output shape or determinism errors."""
    expected = {
        ("pss", 0, None): "3bca62867edc692633de90aed0a9fa70f30c9659ea65a65bb62c15c34deec433",
        ("pss", 1, None): "f97b25a05fb7bfac599167b80d4ff318a68dbf8ae7237b0b7acc427d60651ba5",
        ("pss", 2, None): "9d8aa9f9113a534c11183dbac3d8f22abea7e219024ad72af9aedb17a40094ca",
        ("sss", 0, 0): "880ba4f160197d4a6b46a8dba62f41421a07b942eb9687973c3f18d3428ac8ee",
        ("sss", 100, 1): "ea01207a23580619d4b548f407c3c25f16ebe1f466bac026101e4167adba25e9",
        ("sss", 335, 2): "ab8b7dcf64b3f360f5f0cfcfaf9e85ac2dd18b0eeda2346dab43de940f8bd865",
    }
    for (kind, first_id, second_id), fingerprint in expected.items():
        sequence = (
            sequences.generate_pss(first_id)
            if kind == "pss"
            else sequences.generate_sss(first_id, second_id)
        )
        reference = (
            _reference_pss(first_id)
            if kind == "pss"
            else _reference_sss(first_id, second_id)
        )
        assert np.array_equal(sequence, reference)
        assert hashlib.sha256(sequence.tobytes()).hexdigest() == fingerprint


def test_invalid_sequence_ids_are_rejected():
    with np.testing.assert_raises(ValueError):
        sequences.generate_pss(3)
    with np.testing.assert_raises(ValueError):
        sequences.generate_sss(336, 0)
    with np.testing.assert_raises(ValueError):
        sequences.pci_from_ids(0, 3)


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
