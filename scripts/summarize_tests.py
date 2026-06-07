from __future__ import annotations

import argparse
import json
import os
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from pathlib import Path


def read_jsonl(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def summarize_junit(path: Path) -> dict[str, float | int]:
    if not path.exists():
        return {"test_count": 0, "test_failures": 0, "test_errors": 0, "test_time_seconds": 0.0}

    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))

    test_count = sum(int(suite.attrib.get("tests", 0)) for suite in suites)
    failures = sum(int(suite.attrib.get("failures", 0)) for suite in suites)
    errors = sum(int(suite.attrib.get("errors", 0)) for suite in suites)
    elapsed = sum(float(suite.attrib.get("time", 0.0)) for suite in suites)

    return {
        "test_count": test_count,
        "test_failures": failures,
        "test_errors": errors,
        "test_time_seconds": round(elapsed, 3),
    }


def infer_failure_type(steps: list[dict[str, object]], tests: dict[str, float | int]) -> str:
    failed_steps = {str(step["name"]) for step in steps if int(step.get("exit_code", 0)) != 0}
    if int(tests.get("test_failures", 0)) > 0 or int(tests.get("test_errors", 0)) > 0:
        return "test"
    if "lint" in failed_steps:
        return "lint"
    if "install_dependencies" in failed_steps:
        return "dependency_install"
    if failed_steps:
        return ",".join(sorted(failed_steps))
    return "none"


def main() -> int:
    parser = argparse.ArgumentParser(description="Gera resumo estruturado do job de CI.")
    parser.add_argument("--junit", default="artifacts/junit.xml")
    parser.add_argument("--steps", default="artifacts/step_metrics.jsonl")
    parser.add_argument("--config", default="experiment_config.json")
    parser.add_argument("--output", default="artifacts/ci_summary.json")
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    step_metrics = read_jsonl(Path(args.steps))
    test_summary = summarize_junit(Path(args.junit))
    test_count = int(test_summary["test_count"])
    test_time = float(test_summary["test_time_seconds"])

    summary = {
        "generated_at": datetime.now(UTC).isoformat(),
        "job_name": os.environ.get("CI_JOB_NAME", "local"),
        "scenario": config.get("scenario"),
        "execution_mode": config.get("execution_mode"),
        "cache_buster": config.get("cache_buster"),
        "cache_hit": os.environ.get("CACHE_HIT", ""),
        "experiment_config": config,
        "steps": step_metrics,
        **test_summary,
        "test_average_seconds": round(test_time / test_count, 4) if test_count else 0.0,
        "failure_type": infer_failure_type(step_metrics, test_summary),
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2, ensure_ascii=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
