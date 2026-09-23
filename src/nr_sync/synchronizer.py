"""A0, A1 and A2 synchronization procedures."""


def detect_a0(waveform, config):
    """Estimate timing and NID2 from a received waveform."""
    raise NotImplementedError


def detect_a1(waveform, config):
    """Estimate timing and NID1 using the A1 procedure."""
    raise NotImplementedError


def detect_a2(waveform, config):
    """Estimate timing and PCI using the A2 procedure."""
    raise NotImplementedError