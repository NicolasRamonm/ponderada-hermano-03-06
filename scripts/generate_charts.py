from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

STATUS_COLORS = {"success": "#2E7D32", "failure": "#C62828", "cancelled": "#6A737D"}


def save_current(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Gera graficos do experimento de CI/CD.")
    parser.add_argument("--input", default="data/pipeline_metrics.csv")
    parser.add_argument("--output-dir", default="charts")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    if df.empty:
        raise SystemExit("Base de dados vazia.")

    output_dir = Path(args.output_dir)
    runs = (
        df.sort_values(["timestamp", "run_id"])
        .groupby("run_id", as_index=False)
        .first()
        .sort_values("timestamp")
    )
    runs["label"] = runs["run_number"].astype(str) + " - " + runs["scenario"].fillna("")

    plt.figure(figsize=(12, 5))
    colors = [STATUS_COLORS.get(status, "#455A64") for status in runs["status"]]
    plt.bar(runs["label"], runs["workflow_duration_seconds"], color=colors)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Duracao total (s)")
    plt.title("Tempo total do pipeline por execucao")
    save_current(output_dir / "pipeline_duration_by_run.png")

    job_pivot = df.pivot_table(
        index="run_number",
        columns="job_name",
        values="job_duration_seconds",
        aggfunc="first",
        fill_value=0,
    ).sort_index()
    job_pivot.plot(kind="bar", stacked=False, figsize=(12, 5), width=0.8)
    plt.ylabel("Duracao do job (s)")
    plt.title("Tempo por job")
    plt.xticks(rotation=45, ha="right")
    save_current(output_dir / "job_duration_by_run.png")

    status_counts = runs["status"].value_counts().sort_index()
    plt.figure(figsize=(7, 5))
    plt.bar(
        status_counts.index,
        status_counts.values,
        color=[STATUS_COLORS.get(status, "#455A64") for status in status_counts.index],
    )
    plt.ylabel("Quantidade de execucoes")
    plt.title("Taxa de sucesso e falha")
    save_current(output_dir / "success_failure_rate.png")

    tests_by_run = (
        df.groupby("run_id", as_index=False)
        .agg(
            run_number=("run_number", "first"),
            scenario=("scenario", "first"),
            status=("status", "first"),
            workflow_duration_seconds=("workflow_duration_seconds", "first"),
            test_count=("test_count", "max"),
            execution_mode=("execution_mode", "first"),
        )
        .sort_values("run_number")
    )
    plt.figure(figsize=(9, 5))
    for mode, group in tests_by_run.groupby("execution_mode"):
        plt.scatter(
            group["test_count"],
            group["workflow_duration_seconds"],
            label=mode or "desconhecido",
            s=80,
            alpha=0.85,
        )
    plt.xlabel("Quantidade de testes")
    plt.ylabel("Duracao total do pipeline (s)")
    plt.title("Relacao entre quantidade de testes e duracao")
    plt.legend(title="Modo")
    save_current(output_dir / "tests_vs_pipeline_duration.png")

    cache_df = df[df["install_duration_seconds"] > 0].copy()
    if not cache_df.empty:
        plt.figure(figsize=(8, 5))
        cache_df.boxplot(column="install_duration_seconds", by="cache_hit")
        plt.suptitle("")
        plt.title("Duracao de instalacao por status de cache")
        plt.xlabel("Cache hit")
        plt.ylabel("Duracao de instalacao (s)")
        save_current(output_dir / "install_duration_by_cache.png")

    failure_counts = runs["failure_type"].fillna("unknown").value_counts()
    plt.figure(figsize=(8, 5))
    plt.bar(failure_counts.index, failure_counts.values, color="#546E7A")
    plt.ylabel("Quantidade")
    plt.title("Frequencia de falhas por tipo")
    plt.xticks(rotation=30, ha="right")
    save_current(output_dir / "failure_frequency_by_type.png")

    print(f"Graficos salvos em {output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
