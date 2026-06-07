from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Falha o job quando alguma etapa critica falhou.")
    parser.add_argument("--summary", default="artifacts/ci_summary.json")
    args = parser.parse_args()

    summary = json.loads(Path(args.summary).read_text(encoding="utf-8"))
    failed_steps = [
        step for step in summary.get("steps", []) if int(step.get("exit_code", 0)) != 0
    ]

    if failed_steps:
        names = ", ".join(str(step["name"]) for step in failed_steps)
        print(f"Etapas com falha: {names}")
        return 1

    print("Todas as etapas criticas passaram.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
