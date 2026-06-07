# Experimento de CI/CD com GitHub Actions

Este repositório contém um experimento prático para medir execuções reais de um pipeline CI/CD no GitHub Actions.

A base funcional do projeto foi adaptada do projeto livre [PyPA sampleproject](https://github.com/pypa/sampleproject), licenciado sob MIT. A origem e as adaptações estão documentadas em [`PROJECT_BASE.md`](PROJECT_BASE.md), e a licença original está em [`LICENSE.txt`](LICENSE.txt).

## O que este projeto faz

O pacote Python `sample` expõe uma função pequena:

```python
from sample.simple import add_one

add_one(41)  # 42
```

Essa base pequena foi escolhida porque permite executar um pipeline real com instalação de dependências, lint, testes automatizados, artefatos e coleta de métricas sem esconder o foco principal da atividade: medir o comportamento do CI/CD.

## Entregáveis principais

- Repositório: <https://github.com/NicolasRamonm/ponderada-hermano-03-06>
- Workflow: [`.github/workflows/ci-metrics.yml`](.github/workflows/ci-metrics.yml)
- Script de coleta: [`scripts/collect_metrics.py`](scripts/collect_metrics.py)
- Script de gráficos: [`scripts/generate_charts.py`](scripts/generate_charts.py)
- Base detalhada: [`data/pipeline_metrics.csv`](data/pipeline_metrics.csv)
- Resumo por execução: [`data/pipeline_run_summary.csv`](data/pipeline_run_summary.csv)
- Gráficos: [`charts/`](charts)
- Relatório: [`reports/relatorio.md`](reports/relatorio.md)
- Checklist requisito → evidência: [`reports/checklist.md`](reports/checklist.md)

## Estrutura

- `.github/workflows/ci-metrics.yml`: pipeline instrumentado.
- `experiment_config.json`: cenário controlado usado pelos testes e pelo workflow.
- `src/sample/`: projeto-base adaptado do PyPA `sampleproject`.
- `tests/`: testes Pytest parametrizados.
- `scripts/ci_step.py`: mede duração e status das etapas internas do CI.
- `scripts/summarize_tests.py`: consolida JUnit, cache, cenário e etapas.
- `scripts/collect_metrics.py`: consulta a API do GitHub Actions e baixa artefatos.
- `scripts/generate_charts.py`: gera os gráficos a partir do CSV.
- `reports/`: relatório final e checklist.

## Como rodar localmente

Use Python 3.11 ou superior.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
ruff check src tests scripts
pytest -q
```

Resultado esperado com o `experiment_config.json` versionado atualmente (`final-green`, com 10 casos extras):

```text
19 passed
```

Com `extra_test_cases` igual a `0`, a base executa 9 testes. O número muda quando `experiment_config.json` aumenta `extra_test_cases`.

## Como testar variações localmente

Edite `experiment_config.json`:

```json
{
  "scenario": "slow-test-1500ms",
  "execution_mode": "parallel",
  "extra_test_cases": 0,
  "slow_test_ms": 1500,
  "intentional_failure": false,
  "cache_buster": "v1",
  "notes": "Teste lento controlado."
}
```

Depois rode:

```bash
pytest -q
```

Para simular falha controlada:

```json
"intentional_failure": true
```

## Como o pipeline é disparado

O workflow roda em pushes para:

- `main`
- `experimento-ci-metricas`
- `experimento-ci-base-livre`

Também pode ser disparado manualmente por `workflow_dispatch` na interface do GitHub Actions.

## Como reproduzir o experimento completo

1. Use a branch `experimento-ci-base-livre`.
2. Faça um commit inicial com o cenário `baseline-pass`.
3. Altere `experiment_config.json` para cada variação controlada.
4. Faça um commit e um push por variação.
5. Aguarde pelo menos 12 execuções reais no GitHub Actions.
6. Colete as métricas com o script Python.
7. Gere os gráficos.
8. Atualize o relatório com os run IDs, links, commits e análise.

Exemplo de coleta:

```bash
export GITHUB_TOKEN="token_com_actions_read"
python scripts/collect_metrics.py \
  --repo NicolasRamonm/ponderada-hermano-03-06 \
  --workflow ci-metrics.yml \
  --branch experimento-ci-base-livre \
  --limit 12 \
  --output data/pipeline_metrics.csv \
  --json-output data/pipeline_metrics.json \
  --summary-output data/pipeline_run_summary.csv \
  --summary-json-output data/pipeline_run_summary.json \
  --stats-output data/pipeline_stats.json \
  --download-artifacts
```

Geração dos gráficos:

```bash
python scripts/generate_charts.py \
  --input data/pipeline_metrics.csv \
  --output-dir charts
```

## Como conferir se o must-do foi atendido

Após a coleta e atualização do relatório, confira:

```bash
ruff check src tests scripts
pytest -q
python scripts/generate_charts.py --input data/pipeline_metrics.csv --output-dir charts
```

Depois abra:

- [`reports/checklist.md`](reports/checklist.md)
- [`reports/relatorio.md`](reports/relatorio.md)

O checklist aponta cada requisito do `must-do.md` para uma evidência concreta no repositório.
