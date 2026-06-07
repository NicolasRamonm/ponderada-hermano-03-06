# Experimento de CI/CD com GitHub Actions

Este repositório contém um projeto Python pequeno usado para medir execuções reais de um pipeline CI/CD no GitHub Actions.

O experimento inclui:

- instalação de dependências;
- lint com Ruff;
- testes automatizados com Pytest;
- execução sequencial ou paralela dos jobs;
- artefatos com resultados estruturados;
- coleta de métricas via API do GitHub;
- geração de gráficos;
- relatório técnico em Markdown.

## Estrutura

- `.github/workflows/ci-metrics.yml`: pipeline do experimento.
- `experiment_config.json`: cenário controlado usado pelos testes e pelo workflow.
- `src/pipeline_lab/`: código da aplicação de exemplo.
- `tests/`: testes automatizados.
- `scripts/ci_step.py`: mede duração e status das etapas internas do CI.
- `scripts/collect_metrics.py`: consulta GitHub Actions e gera CSV/JSON com métricas.
- `scripts/generate_charts.py`: gera gráficos a partir da base coletada.
- `reports/relatorio.md`: relatório técnico do experimento.

## Execução local

```bash
python -m pip install -e ".[dev]"
ruff check src tests scripts
pytest -q
```

## Coleta das métricas

Após executar o workflow no GitHub Actions, gere a base de dados:

```bash
export GITHUB_TOKEN="seu_token_com_actions_read"
python scripts/collect_metrics.py \
  --repo NicolasRamonm/ponderada-hermano-03-06 \
  --workflow ci-metrics.yml \
  --branch experimento-ci-metricas \
  --limit 30 \
  --output data/pipeline_metrics.csv \
  --json-output data/pipeline_metrics.json \
  --download-artifacts
```

Em seguida, gere os gráficos:

```bash
python scripts/generate_charts.py \
  --input data/pipeline_metrics.csv \
  --output-dir charts
```

## Como reproduzir o experimento

1. Crie ou use a branch `experimento-ci-metricas`.
2. Altere `experiment_config.json` para variar cenário, cache, quantidade de testes, lentidão artificial, falha intencional e modo de execução.
3. Faça um commit por variação e envie para o GitHub.
4. Aguarde as execuções do GitHub Actions terminarem.
5. Rode `scripts/collect_metrics.py`.
6. Rode `scripts/generate_charts.py`.
7. Atualize `reports/relatorio.md` com os IDs reais, links, commits e análise.
