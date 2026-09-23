"""AWGN, multipath, Doppler and CFO channel models."""


def add_awgn(signal, snr_db: float, rng=None):
    """Add complex AWGN at the requested SNR."""
    raise NotImplementedError


def apply_multipath(signal, taps, delays):
    """Apply complex multipath taps at sample delays."""
    raise NotImplementedError


def apply_doppler(signal, frequency_hz: float, sample_rate_hz: float):
    """Apply a Doppler frequency shift to a complex waveform."""
    raise NotImplementedError


def apply_cfo(signal, cfo_hz: float, sample_rate_hz: float):
    """Apply carrier-frequency offset to a complex waveform."""
    raise NotImplementedError