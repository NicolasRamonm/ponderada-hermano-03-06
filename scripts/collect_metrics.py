from __future__ import annotations

import argparse
import csv
import io
import json
import os
import statistics
import zipfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

API_ROOT = "https://api.github.com"


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def seconds_between(start: str | None, end: str | None) -> float:
    started = parse_time(start)
    completed = parse_time(end)
    if not started or not completed:
        return 0.0
    return round((completed - started).total_seconds(), 3)


def seconds_between_datetimes(start: datetime | None, end: datetime | None) -> float:
    if not start or not end:
        return 0.0
    return round((end - start).total_seconds(), 3)


class GitHubClient:
    def __init__(self, token: str | None) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        )
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def get(self, url: str, **params: Any) -> Any:
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_bytes(self, url: str) -> bytes:
        response = self.session.get(url, timeout=60, allow_redirects=True)
        response.raise_for_status()
        return response.content


def fetch_runs(
    client: GitHubClient, repo: str, workflow: str, branch: str | None, limit: int
) -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    page = 1
    while len(runs) < limit:
        payload = client.get(
            f"{API_ROOT}/repos/{repo}/actions/workflows/{workflow}/runs",
            branch=branch,
            per_page=min(100, limit),
            page=page,
        )
        batch = payload.get("workflow_runs", [])
        if not batch:
            break
        runs.extend(batch)
        page += 1
    return runs[:limit]


def fetch_all_pages(client: GitHubClient, url: str, key: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    page = 1
    while True:
        payload = client.get(url, per_page=100, page=page)
        batch = payload.get(key, [])
        if not batch:
            return items
        items.extend(batch)
        page += 1


def read_summary_from_artifact(
    client: GitHubClient, artifact: dict[str, Any]
) -> dict[str, Any] | None:
    archive = client.get_bytes(artifact["archive_download_url"])
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
        for name in zipped.namelist():
            if name.endswith("ci_summary.json"):
                return json.loads(zipped.read(name).decode("utf-8"))
    return None


def step_duration(summary: dict[str, Any] | None, name: str) -> float:
    if not summary:
        return 0.0
    for step in summary.get("steps", []):
        if step.get("name") == name:
            return float(step.get("duration_seconds", 0.0))
    return 0.0


def normalize_cache_hit(summary: dict[str, Any] | None) -> str:
    if not summary:
        return ""
    return "true" if str(summary.get("cache_hit", "")).lower() == "true" else "false"


def percentile(values: list[float], percentile_value: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = (len(ordered) - 1) * percentile_value
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    weight = index - lower
    return round(ordered[lower] * (1 - weight) + ordered[upper] * weight, 3)


def first_non_empty(rows: list[dict[str, Any]], key: str) -> str:
    for row in rows:
        value = str(row.get(key, "")).strip()
        if value:
            return value
    return ""


def max_numeric(rows: list[dict[str, Any]], key: str) -> float:
    values = [float(row.get(key, 0) or 0) for row in rows]
    return round(max(values), 3) if values else 0.0


def sum_numeric(rows: list[dict[str, Any]], key: str) -> float:
    return round(sum(float(row.get(key, 0) or 0) for row in rows), 3)


def build_run_summary_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["run_id"])].append(row)

    summary_rows: list[dict[str, Any]] = []
    for run_id, run_rows in grouped.items():
        first = run_rows[0]
        active_rows = [row for row in run_rows if row.get("job_status") != "skipped"]
        measured_rows = [
            row
            for row in active_rows
            if row.get("job_name") != "read-config" and row.get("scenario")
        ]
        failure_type = first_non_empty(
            [row for row in measured_rows if row.get("failure_type") not in {"", "none"}],
            "failure_type",
        )
        summary_rows.append(
            {
                "run_id": run_id,
                "run_number": first["run_number"],
                "run_attempt": first["run_attempt"],
                "run_url": first["run_url"],
                "commit_sha": first["commit_sha"],
                "commit_message": first["commit_message"],
                "status": first["status"],
                "timestamp": first["timestamp"],
                "completed_at": first["completed_at"],
                "workflow_duration_seconds": first["workflow_duration_seconds"],
                "queue_duration_seconds": first["queue_duration_seconds"],
                "lead_time_seconds": first["lead_time_seconds"],
                "scenario": first_non_empty(measured_rows, "scenario"),
                "execution_mode": first_non_empty(measured_rows, "execution_mode"),
                "test_count": int(max_numeric(measured_rows, "test_count")),
                "test_failures": int(max_numeric(measured_rows, "test_failures")),
                "test_average_seconds": max_numeric(measured_rows, "test_average_seconds"),
                "active_job_count": len(active_rows),
                "critical_job_duration_seconds": max_numeric(active_rows, "job_duration_seconds"),
                "install_duration_seconds": max_numeric(measured_rows, "install_duration_seconds"),
                "lint_duration_seconds": max_numeric(measured_rows, "lint_duration_seconds"),
                "test_duration_seconds": max_numeric(measured_rows, "test_duration_seconds"),
                "artifact_size_bytes": int(sum_numeric(measured_rows, "artifact_size_bytes")),
                "cache_saved_seconds_estimate": max_numeric(
                    measured_rows, "cache_saved_seconds_estimate"
                ),
                "failure_type": failure_type or "none",
                "attempts_until_green": first["attempts_until_green"],
            }
        )

    return sorted(summary_rows, key=lambda row: int(row["run_number"]))


def build_experiment_stats(summary_rows: list[dict[str, Any]]) -> dict[str, Any]:
    durations = [float(row["workflow_duration_seconds"]) for row in summary_rows]
    queue_durations = [float(row["queue_duration_seconds"]) for row in summary_rows]
    lead_times = [float(row["lead_time_seconds"]) for row in summary_rows]
    statuses: dict[str, int] = defaultdict(int)
    failure_types: dict[str, int] = defaultdict(int)

    for row in summary_rows:
        statuses[str(row["status"])] += 1
        failure_types[str(row["failure_type"])] += 1

    return {
        "run_count": len(summary_rows),
        "status_counts": dict(statuses),
        "failure_type_counts": dict(failure_types),
        "workflow_duration_seconds": {
            "min": min(durations, default=0.0),
            "max": max(durations, default=0.0),
            "p50": percentile(durations, 0.50),
            "p90": percentile(durations, 0.90),
            "p95": percentile(durations, 0.95),
        },
        "queue_duration_seconds": {
            "min": min(queue_durations, default=0.0),
            "max": max(queue_durations, default=0.0),
            "p50": percentile(queue_durations, 0.50),
            "p90": percentile(queue_durations, 0.90),
            "p95": percentile(queue_durations, 0.95),
        },
        "lead_time_seconds": {
            "min": min(lead_times, default=0.0),
            "max": max(lead_times, default=0.0),
            "p50": percentile(lead_times, 0.50),
            "p90": percentile(lead_times, 0.90),
            "p95": percentile(lead_times, 0.95),
        },
    }


def build_rows(
    client: GitHubClient,
    repo: str,
    runs: list[dict[str, Any]],
    download_artifacts: bool,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    attempt_counter = 0

    for run in sorted(runs, key=lambda item: item["created_at"]):
        conclusion = run.get("conclusion") or run.get("status")
        attempt_counter += 1
        attempt_until_green = attempt_counter
        if conclusion == "success":
            attempt_counter = 0

        jobs = fetch_all_pages(client, run["jobs_url"], "jobs")
        artifacts = fetch_all_pages(
            client,
            f"{API_ROOT}/repos/{repo}/actions/runs/{run['id']}/artifacts",
            "artifacts",
        )

        summaries_by_job: dict[str, dict[str, Any]] = {}
        artifact_size_by_job: dict[str, int] = defaultdict(int)
        if download_artifacts:
            for artifact in artifacts:
                artifact_size = int(artifact.get("size_in_bytes", 0))
                try:
                    summary = read_summary_from_artifact(client, artifact)
                except requests.HTTPError as error:
                    print(f"Aviso: nao foi possivel baixar artefato {artifact['name']}: {error}")
                    continue
                if not summary:
                    continue
                job_name = str(summary.get("job_name", artifact["name"]))
                summaries_by_job[job_name] = summary
                artifact_size_by_job[job_name] += artifact_size

        run_summary = next(iter(summaries_by_job.values()), {})

        workflow_duration = seconds_between(run.get("created_at"), run.get("updated_at"))
        run_created_at = parse_time(run.get("created_at"))
        first_job_started_at = min(
            (started for started in (parse_time(job.get("started_at")) for job in jobs) if started),
            default=None,
        )
        queue_duration = seconds_between_datetimes(run_created_at, first_job_started_at)
        commit = run.get("head_commit") or {}
        commit_timestamp = commit.get("timestamp")
        lead_time = seconds_between(commit_timestamp, run.get("updated_at"))

        for job in jobs:
            job_name = job.get("name", "")
            summary = summaries_by_job.get(job_name)
            row = {
                "run_id": run["id"],
                "run_number": run["run_number"],
                "run_attempt": run.get("run_attempt", 1),
                "run_url": run.get("html_url", ""),
                "commit_sha": run.get("head_sha", ""),
                "commit_message": (commit.get("message") or "").splitlines()[0],
                "status": conclusion,
                "workflow_duration_seconds": workflow_duration,
                "queue_duration_seconds": queue_duration,
                "job_name": job_name,
                "job_status": job.get("conclusion") or job.get("status"),
                "job_duration_seconds": seconds_between(
                    job.get("started_at"), job.get("completed_at")
                ),
                "install_duration_seconds": step_duration(summary, "install_dependencies"),
                "lint_duration_seconds": step_duration(summary, "lint"),
                "test_duration_seconds": step_duration(summary, "tests"),
                "test_count": int((summary or {}).get("test_count", 0)),
                "test_failures": int((summary or {}).get("test_failures", 0))
                + int((summary or {}).get("test_errors", 0)),
                "test_average_seconds": float((summary or {}).get("test_average_seconds", 0.0)),
                "timestamp": run.get("created_at", ""),
                "completed_at": run.get("updated_at", ""),
                "lead_time_seconds": lead_time,
                "artifact_size_bytes": artifact_size_by_job.get(job_name, 0),
                "cache_hit": normalize_cache_hit(summary),
                "cache_buster": str((summary or run_summary).get("cache_buster", "")),
                "scenario": str((summary or run_summary).get("scenario", "")),
                "execution_mode": str((summary or run_summary).get("execution_mode", "")),
                "failure_type": str((summary or {}).get("failure_type", "")),
                "attempts_until_green": attempt_until_green,
            }
            rows.append(row)

    install_without_cache = [
        float(row["install_duration_seconds"])
        for row in rows
        if row["install_duration_seconds"] and row["cache_hit"] != "true"
    ]
    baseline_install = statistics.mean(install_without_cache) if install_without_cache else 0.0
    for row in rows:
        install_duration = float(row["install_duration_seconds"])
        if row["cache_hit"] == "true" and baseline_install > install_duration:
            row["cache_saved_seconds_estimate"] = round(baseline_install - install_duration, 3)
        else:
            row["cache_saved_seconds_estimate"] = 0.0

    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Coleta metricas reais do GitHub Actions.")
    parser.add_argument("--repo", required=True, help="Repositorio no formato owner/name.")
    parser.add_argument("--workflow", default="ci-metrics.yml", help="Arquivo do workflow.")
    parser.add_argument("--branch", default=None, help="Branch filtrada.")
    parser.add_argument("--limit", type=int, default=20, help="Quantidade maxima de runs.")
    parser.add_argument("--output", default="data/pipeline_metrics.csv")
    parser.add_argument("--json-output", default="data/pipeline_metrics.json")
    parser.add_argument("--summary-output", default="data/pipeline_run_summary.csv")
    parser.add_argument("--summary-json-output", default="data/pipeline_run_summary.json")
    parser.add_argument("--stats-output", default="data/pipeline_stats.json")
    parser.add_argument("--download-artifacts", action="store_true")
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"))
    args = parser.parse_args()

    client = GitHubClient(args.token)
    runs = fetch_runs(client, args.repo, args.workflow, args.branch, args.limit)
    rows = build_rows(client, args.repo, runs, args.download_artifacts)
    summary_rows = build_run_summary_rows(rows)
    stats = build_experiment_stats(summary_rows)

    write_csv(Path(args.output), rows)
    write_csv(Path(args.summary_output), summary_rows)
    Path(args.json_output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_output).write_text(
        json.dumps(rows, indent=2, ensure_ascii=True), encoding="utf-8"
    )
    Path(args.summary_json_output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.summary_json_output).write_text(
        json.dumps(summary_rows, indent=2, ensure_ascii=True), encoding="utf-8"
    )
    Path(args.stats_output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.stats_output).write_text(
        json.dumps(stats, indent=2, ensure_ascii=True), encoding="utf-8"
    )

    print(f"Runs processadas: {len(runs)}")
    print(f"Linhas geradas: {len(rows)}")
    print(f"Resumo por run: {len(summary_rows)}")
    print(f"CSV: {args.output}")
    print(f"JSON: {args.json_output}")
    print(f"Resumo CSV: {args.summary_output}")
    print(f"Resumo JSON: {args.summary_json_output}")
    print(f"Stats JSON: {args.stats_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
