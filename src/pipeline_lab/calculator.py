from __future__ import annotations


def safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        raise ValueError("denominator must not be zero")
    return numerator / denominator


def average(values: list[float]) -> float:
    if not values:
        raise ValueError("values must not be empty")
    return sum(values) / len(values)


def moving_sum(values: list[int], window: int) -> list[int]:
    if window <= 0:
        raise ValueError("window must be positive")
    if window > len(values):
        return []
    return [sum(values[index : index + window]) for index in range(len(values) - window + 1)]


def classify_latency(milliseconds: float) -> str:
    if milliseconds < 0:
        raise ValueError("milliseconds must be non-negative")
    if milliseconds < 150:
        return "fast"
    if milliseconds < 500:
        return "acceptable"
    return "slow"
