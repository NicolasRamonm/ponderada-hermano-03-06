from __future__ import annotations

import json
import os
import time
from pathlib import Path

import pytest

from pipeline_lab import average, classify_latency, moving_sum, safe_divide

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def experiment_config() -> dict[str, object]:
    config_path = Path(os.environ.get("EXPERIMENT_CONFIG", ROOT / "experiment_config.json"))
    return json.loads(config_path.read_text(encoding="utf-8"))


def generated_cases() -> list[tuple[int, int, int]]:
    config_path = Path(os.environ.get("EXPERIMENT_CONFIG", ROOT / "experiment_config.json"))
    config = json.loads(config_path.read_text(encoding="utf-8"))
    extra_cases = int(config.get("extra_test_cases", 0))
    base_cases = [(1, 2, 3), (3, 4, 7), (10, -4, 6), (0, 0, 0)]
    generated = [(index, index * 2, index * 3) for index in range(1, extra_cases + 1)]
    return base_cases + generated


@pytest.mark.parametrize(("left", "right", "expected"), generated_cases())
def test_moving_sum_for_generated_cases(left: int, right: int, expected: int) -> None:
    assert moving_sum([left, right], 2) == [expected]


def test_safe_divide_returns_float() -> None:
    assert safe_divide(9, 3) == 3


def test_safe_divide_rejects_zero_denominator() -> None:
    with pytest.raises(ValueError, match="denominator"):
        safe_divide(1, 0)


def test_average() -> None:
    assert average([10, 20, 30]) == 20


def test_average_rejects_empty_list() -> None:
    with pytest.raises(ValueError, match="empty"):
        average([])


@pytest.mark.parametrize(
    ("milliseconds", "expected"),
    [(50, "fast"), (200, "acceptable"), (750, "slow")],
)
def test_classify_latency(milliseconds: float, expected: str) -> None:
    assert classify_latency(milliseconds) == expected


def test_slow_path_controlled_by_experiment(experiment_config: dict[str, object]) -> None:
    delay_ms = int(experiment_config.get("slow_test_ms", 0))
    if delay_ms > 0:
        time.sleep(delay_ms / 1000)
    assert classify_latency(delay_ms) in {"fast", "acceptable", "slow"}


def test_controlled_failure(experiment_config: dict[str, object]) -> None:
    assert not bool(experiment_config.get("intentional_failure", False)), (
        "Falha intencional configurada para medir estabilidade do pipeline."
    )
