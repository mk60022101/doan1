"""5G NR synchronization sequences from 3GPP TS 38.211, section 7.4.2."""

from __future__ import annotations

import numpy as np


def _binary_m_sequence(taps: tuple[int, ...], length: int = 127) -> np.ndarray:
    state = np.zeros(length + 7, dtype=np.int8)
    state[:7] = (0, 0, 0, 0, 0, 0, 1)
    for index in range(length):
        state[index + 7] = sum(state[index + tap] for tap in taps) % 2
    return state[7 : 7 + length]


def _validate_ids(nid1: int, nid2: int) -> None:
    if not isinstance(nid1, (int, np.integer)) or not 0 <= nid1 <= 335:
        raise ValueError("nid1 must be an integer in [0, 335]")
    if not isinstance(nid2, (int, np.integer)) or not 0 <= nid2 <= 2:
        raise ValueError("nid2 must be an integer in [0, 2]")


def generate_pss(nid2: int) -> np.ndarray:
    """Return the 127-symbol BPSK PSS sequence for N_ID^2."""
    if not isinstance(nid2, (int, np.integer)) or not 0 <= nid2 <= 2:
        raise ValueError("nid2 must be an integer in [0, 2]")
    x = _binary_m_sequence((0, 4))
    return (1 - 2 * x[(np.arange(127) + 43 * int(nid2)) % 127]).astype(np.int8)


def generate_sss(nid1: int, nid2: int) -> np.ndarray:
    """Return the 127-symbol BPSK SSS sequence for N_ID^1 and N_ID^2."""
    _validate_ids(nid1, nid2)
    nid1 = int(nid1)
    nid2 = int(nid2)
    x0 = _binary_m_sequence((0, 4))
    x1 = _binary_m_sequence((0, 1))
    m0 = 15 * (nid1 // 112) + 5 * nid2
    m1 = nid1 % 112
    n = np.arange(127)
    return (
        (1 - 2 * x0[(n + m0) % 127])
        * (1 - 2 * x1[(n + m1) % 127])
        * (1 - 2 * x1[(n + m0) % 127])
        * (1 - 2 * x0[(n + m1) % 127])
    ).astype(np.int8)


def pci_from_ids(nid1: int, nid2: int) -> int:
    """Map N_ID^1 and N_ID^2 to the physical cell identity in [0, 1007]."""
    _validate_ids(nid1, nid2)
    return 3 * int(nid1) + int(nid2)