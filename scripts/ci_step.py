from __future__ import annotations

import argparse
import json
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(description="Executa um comando e registra metricas da etapa.")
    parser.add_argument("--name", required=True, help="Nome logico da etapa.")
    parser.add_argument("--metrics-file", default="artifacts/step_metrics.jsonl")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if not args.command:
        raise SystemExit("Nenhum comando informado.")
    command = args.command[1:] if args.command[0] == "--" else args.command

    metrics_path = Path(args.metrics_file)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    started_at = utc_now()
    start = time.perf_counter()
    completed = subprocess.run(command, check=False)
    end = time.perf_counter()
    finished_at = utc_now()

    record = {
        "name": args.name,
        "command": command,
        "started_at": started_at,
        "completed_at": finished_at,
        "duration_seconds": round(end - start, 3),
        "exit_code": completed.returncode,
    }
    with metrics_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=True) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
