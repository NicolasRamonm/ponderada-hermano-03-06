# Relatorio tecnico: experimento de metricas em CI/CD

## Repositorio e base do projeto

- Repositorio: <https://github.com/NicolasRamonm/ponderada-hermano-03-06>
- Branch do experimento: `experimento-ci-base-livre`
- Workflow YAML: <https://github.com/NicolasRamonm/ponderada-hermano-03-06/blob/experimento-ci-base-livre/.github/workflows/ci-metrics.yml>
- Projeto-base livre: [PyPA sampleproject](https://github.com/pypa/sampleproject)
- Licenca do projeto-base: MIT, preservada em [`LICENSE.txt`](../LICENSE.txt)
- Descricao da adaptacao: [`PROJECT_BASE.md`](../PROJECT_BASE.md)
- Script de coleta: [`scripts/collect_metrics.py`](../scripts/collect_metrics.py)
- Base CSV: [`data/pipeline_metrics.csv`](../data/pipeline_metrics.csv)
- Base JSON: [`data/pipeline_metrics.json`](../data/pipeline_metrics.json)
- Resumo por execucao CSV: [`data/pipeline_run_summary.csv`](../data/pipeline_run_summary.csv)
- Resumo por execucao JSON: [`data/pipeline_run_summary.json`](../data/pipeline_run_summary.json)
- Estatisticas consolidadas: [`data/pipeline_stats.json`](../data/pipeline_stats.json)
- Script de graficos: [`scripts/generate_charts.py`](../scripts/generate_charts.py)
- Checklist de requisitos: [`reports/checklist.md`](./checklist.md)

## Hipotese inicial

A hipotese inicial foi que cache e jobs paralelos reduziriam o tempo total do pipeline, enquanto teste lento e aumento artificial da quantidade de testes elevariam principalmente o tempo do job de testes.

O resultado confirmou parcialmente essa hipotese. O cache reduziu o tempo medio de instalacao, mas o tempo total continuou bastante influenciado por overhead de runner, checkout, setup de Python, upload de artefatos e variacao natural do GitHub Actions. A execucao com mais testes nao cresceu de forma linear porque a suite baseada no `sampleproject` ainda e muito pequena e os testes parametrizados sao baratos.

## Desenho do experimento

O projeto usa Python, Pytest e Ruff. A aplicacao-base esta em `src/sample/` e foi adaptada do PyPA `sampleproject`, com a funcao `add_one`. O arquivo `experiment_config.json` controla:

- `execution_mode`: ativa jobs paralelos (`lint-parallel` e `tests-parallel`) ou job unico sequencial (`quality-sequential`);
- `extra_test_cases`: aumenta artificialmente a quantidade de testes parametrizados;
- `slow_test_ms`: adiciona atraso artificial em um teste;
- `intentional_failure`: gera falha controlada;
- `cache_buster`: muda a chave do cache de dependencias.

O workflow gera artefatos por job com:

- `ci_summary.json`: resumo de cenario, cache, testes e falha;
- `junit.xml`: resultado de testes;
- `step_metrics.jsonl`: duracao e exit code das etapas internas.

O script `collect_metrics.py` consulta a API do GitHub Actions, baixa os artefatos e cruza os dados em CSV/JSON. Alem da base detalhada por job, ele gera resumo por execucao e estatisticas consolidadas.

## Execucoes reais do GitHub Actions

| Ordem | Run ID | Link | Commit | Mensagem | Variacao | Status | Duracao | Testes | Falhas |
|---:|---:|---|---|---|---|---|---:|---:|---:|
| 1 | 27102177249 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27102177249) | `9053999` | Adapta experimento para base livre sampleproject | `baseline-pass` | success | 36s | 9 | 0 |
| 2 | 27102184396 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27102184396) | `1af706b` | Mede cache na base sampleproject | `baseline-cache-hit` | success | 29s | 9 | 0 |
| 3 | 27102188950 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27102188950) | `1efa7f8` | Aumenta testes na base sampleproject | `more-tests-25` | success | 33s | 34 | 0 |
| 4 | 27102195431 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27102195431) | `4ac8198` | Adiciona teste lento na base sampleproject | `slow-test-1500ms` | success | 33s | 9 | 0 |
| 5 | 27102200902 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27102200902) | `ece32a4` | Registra falha controlada na base sampleproject | `controlled-failure` | failure | 36s | 9 | 1 |
| 6 | 27102206525 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27102206525) | `db4fa62` | Restaura pipeline verde da base sampleproject | `recovery-pass` | success | 35s | 9 | 0 |
| 7 | 27102213090 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27102213090) | `055a33e` | Altera cache da base sampleproject | `cache-bust` | success | 32s | 9 | 0 |
| 8 | 27102218632 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27102218632) | `3054ba3` | Compara modo sequencial na base sampleproject | `sequential-baseline` | success | 32s | 9 | 0 |
| 9 | 27102223129 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27102223129) | `f3eedcf` | Combina sequencial e teste lento na base sampleproject | `sequential-slow` | success | 38s | 9 | 0 |
| 10 | 27102228786 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27102228786) | `de16176` | Aumenta carga paralela na base sampleproject | `parallel-more-tests-60` | success | 35s | 69 | 0 |
| 11 | 27102235236 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27102235236) | `cb7ba4e` | Reaproveita cache da base sampleproject | `cache-hit-after-bust` | success | 34s | 9 | 0 |
| 12 | 27102240744 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27102240744) | `a6c1042` | Finaliza serie da base sampleproject | `final-green` | success | 37s | 19 | 0 |

## Commits usados

| Commit | Mensagem | Variacao |
|---|---|---|
| `9053999` | Adapta experimento para base livre sampleproject | `baseline-pass` |
| `1af706b` | Mede cache na base sampleproject | `baseline-cache-hit` |
| `1efa7f8` | Aumenta testes na base sampleproject | `more-tests-25` |
| `4ac8198` | Adiciona teste lento na base sampleproject | `slow-test-1500ms` |
| `ece32a4` | Registra falha controlada na base sampleproject | `controlled-failure` |
| `db4fa62` | Restaura pipeline verde da base sampleproject | `recovery-pass` |
| `055a33e` | Altera cache da base sampleproject | `cache-bust` |
| `3054ba3` | Compara modo sequencial na base sampleproject | `sequential-baseline` |
| `f3eedcf` | Combina sequencial e teste lento na base sampleproject | `sequential-slow` |
| `de16176` | Aumenta carga paralela na base sampleproject | `parallel-more-tests-60` |
| `cb7ba4e` | Reaproveita cache da base sampleproject | `cache-hit-after-bust` |
| `a6c1042` | Finaliza serie da base sampleproject | `final-green` |

## Graficos

![Tempo total do pipeline por execucao](../charts/pipeline_duration_by_run.png)

![Tempo por job](../charts/job_duration_by_run.png)

![Taxa de sucesso e falha](../charts/success_failure_rate.png)

![Relacao entre quantidade de testes e duracao](../charts/tests_vs_pipeline_duration.png)

![Duracao de instalacao por cache](../charts/install_duration_by_cache.png)

![Frequencia de falhas por tipo](../charts/failure_frequency_by_type.png)

Graficos adicionais:

![Tendencia de duracao do pipeline](../charts/pipeline_duration_trend.png)

![Boxplot por modo de execucao](../charts/workflow_duration_by_mode_boxplot.png)

![Decomposicao aproximada do tempo](../charts/step_time_breakdown.png)

![Heatmap de etapas por execucao](../charts/step_duration_heatmap.png)

![Tempo de fila por execucao](../charts/queue_time_by_run.png)

## Resultados quantitativos

- Foram 12 execucoes reais: 11 com sucesso e 1 com falha.
- A unica falha foi do tipo `test`, causada por `intentional_failure=true`.
- O tempo total variou de 29s a 38s.
- A duracao teve p50 de 34,5s, p90 de 36,9s e p95 de 37,45s.
- O tempo de fila variou de 2s a 4s, com p50 de 2s.
- O lead time entre commit e conclusao variou de 32s a 41s.
- O lead time teve p50 de 37,5s, p90 de 39,9s e p95 de 40,45s.
- A instalacao de dependencias foi a etapa dominante: media de 14,90s.
- Lint foi praticamente desprezivel: media de 0,03s.
- Testes tiveram media de 0,76s, com maior impacto no cenario lento.
- Sem cache, a instalacao levou em media 16,72s; com cache, 14,21s.
- Execucoes paralelas tiveram media de 34,0s; sequenciais, 35,0s.
- A tentativa ate voltar a verde apos falha foi de 2 execucoes: `controlled-failure` e `recovery-pass`.

## Analise das perguntas

### Qual etapa mais contribuiu para o tempo total?

A instalacao de dependencias foi a etapa que mais contribuiu para o tempo total. Mesmo com a base `sampleproject` sendo pequena, o projeto instala dependencias de execucao e de desenvolvimento, e essa etapa ficou muito acima do tempo de lint e testes.

### Houve diferenca significativa entre execucoes com e sem cache?

Sim na etapa de instalacao, mas com impacto limitado no workflow completo. A media de instalacao caiu de 16,72s sem cache para 14,21s com cache. A economia aproximada de 2,51s e relevante, mas parte do tempo total vem de overhead externo do GitHub Actions.

### O paralelismo reduziu o tempo total? Em que condicoes?

O paralelismo reduziu pouco. A media paralela foi 34,0s e a sequencial foi 35,0s. O ganho e limitado porque os jobs paralelos repetem checkout, setup e instalacao. Em projetos maiores, paralelismo tende a compensar quando lint/testes sao mais demorados do que o custo duplicado de setup.

### Quais falhas foram mais frequentes?

Apenas uma falha ocorreu, do tipo `test`, planejada no commit `ece32a4` com a variacao `controlled-failure`.

### O pipeline fornece feedback rapido o suficiente?

Sim para um projeto pequeno. O tempo de workflow ficou entre 29s e 38s, e o lead time entre 32s e 41s. Para um projeto real maior, o principal risco seria o crescimento da instalacao de dependencias e a repeticao dessa etapa em jobs paralelos.

### Que melhorias poderiam ser feitas?

- Evitar repetir instalacao de dependencias em jobs paralelos.
- Criar uma imagem base ou ambiente preconstruido para reduzir setup.
- Aumentar a quantidade de execucoes para comparar percentis com mais confianca.
- Separar metricas de overhead do GitHub Actions e metricas de comandos internos.
- Incluir falhas de lint e falhas de instalacao como categorias adicionais.
- Adicionar cobertura de testes e publicar relatorio HTML como artefato.

### Quais limitacoes existem nos dados coletados?

- A amostra tem 12 execucoes, suficiente para a atividade, mas pequena para estatistica robusta.
- Os runners do GitHub Actions sao compartilhados e podem variar.
- Os commits foram enviados em sequencia rapida, o que pode influenciar cache e concorrencia.
- O tempo economizado com cache e estimado por diferenca de instalacao.
- A base `sampleproject` e propositalmente pequena, entao testes nao representam uma aplicacao grande.
- Ha apenas 2 execucoes sequenciais, limitando a comparacao contra paralelo.

### Como essa analise apoia decisoes de engenharia?

A analise mostra que, nesta base, otimizar testes nao traria grande retorno inicial, pois a etapa dominante e instalacao. Uma equipe deveria priorizar cache, reduzir dependencias, evitar setup duplicado e acompanhar percentis de duracao antes de ampliar paralelismo ou matriz de versoes.

## Resultados inesperados

1. O cenario `baseline-cache-hit` foi o run mais rapido, com 29s, abaixo do baseline de 36s. O ganho foi maior do que a economia media de cache sugeriria, indicando influencia de overhead externo e variacao de runner.

2. O cenario `parallel-more-tests-60`, com 69 testes, levou 35s, menor que o baseline de 36s. Isso contradiz a expectativa de crescimento linear e mostra que a suite ainda e barata diante do custo de setup.

3. O cenario `sequential-slow` foi o mais demorado, com 38s, mesmo tendo a mesma quantidade de testes do baseline. Nesse caso, o teste lento apareceu de forma mais clara porque lint e testes estavam no mesmo job sequencial.

## Comparacao entre hipotese e resultado observado

A hipotese de que cache ajudaria foi confirmada na etapa de instalacao. A hipotese de que paralelismo reduziria significativamente a duracao foi apenas parcialmente confirmada, pois a diferenca media foi pequena. A hipotese de que mais testes aumentariam o tempo total nao se confirmou claramente, porque os testes gerados sao simples e o overhead do CI dominou a duracao.

## Incrementos alem do minimo

- Resumo agregado por execucao em `pipeline_run_summary.csv` e `pipeline_run_summary.json`.
- Estatisticas consolidadas em `pipeline_stats.json`, incluindo p50, p90 e p95.
- Metrica de tempo de fila entre criacao do run e inicio do primeiro job.
- Grafico de tendencia temporal.
- Boxplot de duracao por modo de execucao.
- Decomposicao aproximada do tempo por etapa.
- Heatmap das etapas por execucao.
- Checklist de rastreabilidade entre requisitos e evidencias.

## Reproducao

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
ruff check src tests scripts
pytest -q
```

Depois de executar o workflow no GitHub Actions:

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

python scripts/generate_charts.py \
  --input data/pipeline_metrics.csv \
  --output-dir charts
```
