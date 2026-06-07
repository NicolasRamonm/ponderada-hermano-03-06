from __future__ import annotations

import json
import os
import time
from pathlib import Path

import pytest

from sample.simple import add_one

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def experiment_config() -> dict[str, object]:
    config_path = Path(os.environ.get("EXPERIMENT_CONFIG", ROOT / "experiment_config.json"))
    return json.loads(config_path.read_text(encoding="utf-8"))


def generated_add_one_cases() -> list[tuple[int, int]]:
    config_path = Path(os.environ.get("EXPERIMENT_CONFIG", ROOT / "experiment_config.json"))
    config = json.loads(config_path.read_text(encoding="utf-8"))
    extra_cases = int(config.get("extra_test_cases", 0))
    base_cases = [(-2, -1), (0, 1), (1, 2), (5, 6), (41, 42)]
    generated = [(index, index + 1) for index in range(1, extra_cases + 1)]
    return base_cases + generated


@pytest.mark.parametrize(("value", "expected"), generated_add_one_cases())
def test_add_one_for_generated_cases(value: int, expected: int) -> None:
    assert add_one(value) == expected


def test_add_one_preserves_integer_type() -> None:
    assert isinstance(add_one(10), int)


def test_add_one_supports_negative_numbers() -> None:
    assert add_one(-10) == -9


def test_slow_path_controlled_by_experiment(experiment_config: dict[str, object]) -> None:
    delay_ms = int(experiment_config.get("slow_test_ms", 0))
    if delay_ms > 0:
        time.sleep(delay_ms / 1000)
    assert add_one(delay_ms) == delay_ms + 1


def test_controlled_failure(experiment_config: dict[str, object]) -> None:
    assert not bool(experiment_config.get("intentional_failure", False)), (
        "Falha intencional configurada para medir estabilidade do pipeline."
    )
