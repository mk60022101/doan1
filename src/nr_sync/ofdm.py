"""OFDM resource mapping, FFT/IFFT and cyclic-prefix operations."""


def map_resources(grid, symbols):
    """Map symbols to an OFDM resource grid."""
    raise NotImplementedError


def ofdm_modulate(grid, n_fft: int, cp_length: int):
    """Convert a resource grid to a time-domain OFDM waveform."""
    raise NotImplementedError


def ofdm_demodulate(waveform, n_fft: int, cp_length: int):
    """Recover the resource grid from a time-domain waveform."""
    raise NotImplementedError