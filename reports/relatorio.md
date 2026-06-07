# Relatorio tecnico: experimento de metricas em CI/CD

## Repositorio

- Repositorio: <https://github.com/NicolasRamonm/ponderada-hermano-03-06>
- Workflow: <https://github.com/NicolasRamonm/ponderada-hermano-03-06/blob/experimento-ci-metricas/.github/workflows/ci-metrics.yml>
- Branch do experimento: `experimento-ci-metricas`

## Hipotese inicial

A hipotese inicial foi que execucoes com cache e jobs paralelos reduziriam o tempo total do pipeline, enquanto testes lentos e aumento artificial da quantidade de testes elevariam principalmente o tempo do job de testes.

## Desenho do experimento

O pipeline foi configurado com leitura de `experiment_config.json`, permitindo controlar:

- modo de execucao: `parallel` ou `sequential`;
- quantidade artificial de testes;
- atraso artificial em teste lento;
- falha intencional de teste;
- chave de cache de dependencias.

Cada variacao deve ser registrada por um commit separado. O workflow gera artefatos com `ci_summary.json`, `junit.xml` e `step_metrics.jsonl`. O script `scripts/collect_metrics.py` consulta a API do GitHub Actions, baixa os artefatos e gera `data/pipeline_metrics.csv` e `data/pipeline_metrics.json`.

## Execucoes reais

Preencher apos a coleta final.

| Ordem | Run ID | Link | Commit | Mensagem | Variacao | Status |
|---:|---:|---|---|---|---|---|
| 1 | A preencher | A preencher | A preencher | A preencher | A preencher | A preencher |

## Variacoes planejadas

| Ordem | Cenario | Objetivo |
|---:|---|---|
| 1 | baseline-pass | Medir baseline com pipeline verde e cache inicial |
| 2 | baseline-cache-hit | Medir repeticao com cache reaproveitado |
| 3 | more-tests-25 | Aumentar quantidade de testes |
| 4 | slow-test-1500ms | Introduzir teste lento |
| 5 | controlled-failure | Registrar falha intencional de teste |
| 6 | recovery-pass | Medir tentativa ate voltar a verde |
| 7 | cache-bust | Alterar chave de cache |
| 8 | sequential-baseline | Comparar jobs sequenciais contra paralelos |
| 9 | sequential-slow | Combinar sequencial com teste lento |
| 10 | parallel-more-tests-60 | Aumentar carga em modo paralelo |
| 11 | cache-hit-after-bust | Medir novo cache hit |
| 12 | final-green | Execucao final estavel |

## Graficos

Os graficos sao gerados em `charts/`:

- `pipeline_duration_by_run.png`
- `job_duration_by_run.png`
- `success_failure_rate.png`
- `tests_vs_pipeline_duration.png`
- `install_duration_by_cache.png`
- `failure_frequency_by_type.png`

## Analise

### Qual etapa mais contribuiu para o tempo total do pipeline?

A preencher com base nos dados de `job_duration_seconds`, `install_duration_seconds`, `lint_duration_seconds` e `test_duration_seconds`.

### Houve diferenca significativa entre execucoes com e sem cache?

A preencher comparando `cache_hit`, `install_duration_seconds` e `cache_saved_seconds_estimate`.

### O paralelismo reduziu o tempo total? Em que condicoes?

A preencher comparando `execution_mode=parallel` e `execution_mode=sequential`.

### Quais falhas foram mais frequentes?

A preencher usando `failure_type`.

### O pipeline fornece feedback rapido o suficiente?

A preencher considerando a duracao total, o lead time e a frequencia de falhas.

### Melhorias propostas

A preencher apos observacao dos gargalos reais.

### Limitacoes

A preencher com limitacoes dos dados, amostra e variacoes.

### Resultados inesperados

A preencher com pelo menos dois resultados observados.

### Decisoes de engenharia apoiadas pela analise

A preencher com decisoes praticas derivadas das metricas.

## Reproducao

```bash
python -m pip install -e ".[dev]"
ruff check src tests scripts
pytest -q

export GITHUB_TOKEN="seu_token_com_actions_read"
python scripts/collect_metrics.py \
  --repo NicolasRamonm/ponderada-hermano-03-06 \
  --workflow ci-metrics.yml \
  --branch experimento-ci-metricas \
  --limit 30 \
  --output data/pipeline_metrics.csv \
  --json-output data/pipeline_metrics.json \
  --download-artifacts

python scripts/generate_charts.py \
  --input data/pipeline_metrics.csv \
  --output-dir charts
```
