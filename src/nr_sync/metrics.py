"""Detection metrics and experiment reporting helpers."""


def probability_of_detection(detections, truth):
    """Compute Pd from detection decisions and ground truth."""
    raise NotImplementedError


def probability_of_false_alarm(false_alarms, trials):
    """Compute Pfa from false alarms and total trials."""
    raise NotImplementedError


def rmse(estimates, truth):
    """Compute root mean squared error."""
    raise NotImplementedError


def confidence_interval(values, confidence: float = 0.95):
    """Estimate a confidence interval for measured values."""
    raise NotImplementedError