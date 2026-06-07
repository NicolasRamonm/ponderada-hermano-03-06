from __future__ import annotations

import json
import os
from pathlib import Path


def sanitize_output(value: object) -> str:
    return str(value).strip().replace("\n", " ")


def main() -> int:
    config = json.loads(Path("experiment_config.json").read_text(encoding="utf-8"))
    output_path = os.environ.get("GITHUB_OUTPUT")

    if output_path:
        with Path(output_path).open("a", encoding="utf-8") as output:
            for key in [
                "scenario",
                "execution_mode",
                "cache_buster",
                "extra_test_cases",
                "slow_test_ms",
                "intentional_failure",
            ]:
                output.write(f"{key}={sanitize_output(config.get(key, ''))}\n")

    print(json.dumps(config, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
