# Relatorio tecnico: experimento de metricas em CI/CD

## Repositorio e artefatos

- Repositorio: <https://github.com/NicolasRamonm/ponderada-hermano-03-06>
- Branch do experimento: `experimento-ci-metricas`
- Workflow YAML: <https://github.com/NicolasRamonm/ponderada-hermano-03-06/blob/experimento-ci-metricas/.github/workflows/ci-metrics.yml>
- Script de coleta: [`scripts/collect_metrics.py`](../scripts/collect_metrics.py)
- Base CSV: [`data/pipeline_metrics.csv`](../data/pipeline_metrics.csv)
- Base JSON: [`data/pipeline_metrics.json`](../data/pipeline_metrics.json)
- Resumo por execucao CSV: [`data/pipeline_run_summary.csv`](../data/pipeline_run_summary.csv)
- Resumo por execucao JSON: [`data/pipeline_run_summary.json`](../data/pipeline_run_summary.json)
- Estatisticas consolidadas: [`data/pipeline_stats.json`](../data/pipeline_stats.json)
- Script de graficos: [`scripts/generate_charts.py`](../scripts/generate_charts.py)
- Checklist de requisitos: [`reports/checklist.md`](./checklist.md)

## Hipotese inicial

A hipotese inicial foi que execucoes com cache e jobs paralelos reduziriam o tempo total do pipeline, enquanto testes lentos e aumento artificial da quantidade de testes elevariam principalmente o tempo do job de testes.

O resultado confirmou parcialmente essa hipotese: o cache reduziu o tempo medio de instalacao, mas o tempo total do workflow foi dominado por overhead de runner, checkout, setup e concorrencia entre jobs. A maior carga de testes tambem nao aumentou o tempo total de forma linear, porque os testes eram pequenos e a instalacao de dependencias pesou mais.

## Desenho do experimento

O projeto usa Python, Pytest e Ruff. O arquivo `experiment_config.json` controla as variacoes:

- `execution_mode`: ativa jobs paralelos (`lint-parallel` e `tests-parallel`) ou job unico sequencial (`quality-sequential`);
- `extra_test_cases`: aumenta artificialmente a quantidade de testes parametrizados;
- `slow_test_ms`: adiciona atraso artificial em um teste;
- `intentional_failure`: gera falha controlada;
- `cache_buster`: muda a chave do cache de dependencias.

O workflow gera artefatos por job com:

- `ci_summary.json`: resumo de cenario, cache, testes e falha;
- `junit.xml`: resultado de testes;
- `step_metrics.jsonl`: duracao e exit code das etapas internas.

O script `collect_metrics.py` consulta a API do GitHub Actions, baixa os artefatos e cruza os dados em CSV/JSON.

## Execucoes reais do GitHub Actions

| Ordem | Run ID | Link | Commit | Mensagem | Variacao | Status | Duracao | Testes | Falhas |
|---:|---:|---|---|---|---|---|---:|---:|---:|
| 1 | 27101381991 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27101381991) | `1204740` | Configura experimento de metricas do pipeline | `baseline-pass` | success | 35s | 13 | 0 |
| 2 | 27101388549 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27101388549) | `c0bb42e` | Mede baseline com cache reutilizado | `baseline-cache-hit` | success | 33s | 13 | 0 |
| 3 | 27101392374 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27101392374) | `a70e5b5` | Aumenta quantidade de testes para experimento | `more-tests-25` | success | 37s | 38 | 0 |
| 4 | 27101397602 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27101397602) | `28e5ae2` | Adiciona teste lento controlado | `slow-test-1500ms` | success | 35s | 13 | 0 |
| 5 | 27101403237 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27101403237) | `1fa1567` | Registra falha controlada de testes | `controlled-failure` | failure | 34s | 13 | 1 |
| 6 | 27101408745 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27101408745) | `8b6b0c2` | Restaura pipeline verde apos falha | `recovery-pass` | success | 35s | 13 | 0 |
| 7 | 27101412987 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27101412987) | `5cac11c` | Altera chave de cache do experimento | `cache-bust` | success | 36s | 13 | 0 |
| 8 | 27101417665 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27101417665) | `a7fc94a` | Compara pipeline em modo sequencial | `sequential-baseline` | success | 36s | 13 | 0 |
| 9 | 27101422365 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27101422365) | `95204d2` | Combina modo sequencial com teste lento | `sequential-slow` | success | 34s | 13 | 0 |
| 10 | 27101427191 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27101427191) | `45962a5` | Aumenta carga de testes em paralelo | `parallel-more-tests-60` | success | 31s | 73 | 0 |
| 11 | 27101431208 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27101431208) | `143238a` | Reaproveita cache apos nova chave | `cache-hit-after-bust` | success | 36s | 13 | 0 |
| 12 | 27101435614 | [run](https://github.com/NicolasRamonm/ponderada-hermano-03-06/actions/runs/27101435614) | `5995e67` | Finaliza serie de execucoes verdes | `final-green` | success | 30s | 23 | 0 |

## Commits usados

| Commit | Mensagem | Variacao |
|---|---|---|
| `1204740` | Configura experimento de metricas do pipeline | `baseline-pass` |
| `c0bb42e` | Mede baseline com cache reutilizado | `baseline-cache-hit` |
| `a70e5b5` | Aumenta quantidade de testes para experimento | `more-tests-25` |
| `28e5ae2` | Adiciona teste lento controlado | `slow-test-1500ms` |
| `1fa1567` | Registra falha controlada de testes | `controlled-failure` |
| `8b6b0c2` | Restaura pipeline verde apos falha | `recovery-pass` |
| `5cac11c` | Altera chave de cache do experimento | `cache-bust` |
| `a7fc94a` | Compara pipeline em modo sequencial | `sequential-baseline` |
| `95204d2` | Combina modo sequencial com teste lento | `sequential-slow` |
| `45962a5` | Aumenta carga de testes em paralelo | `parallel-more-tests-60` |
| `143238a` | Reaproveita cache apos nova chave | `cache-hit-after-bust` |
| `5995e67` | Finaliza serie de execucoes verdes | `final-green` |

## Graficos

![Tempo total do pipeline por execucao](../charts/pipeline_duration_by_run.png)

![Tempo por job](../charts/job_duration_by_run.png)

![Taxa de sucesso e falha](../charts/success_failure_rate.png)

![Relacao entre quantidade de testes e duracao](../charts/tests_vs_pipeline_duration.png)

![Duracao de instalacao por cache](../charts/install_duration_by_cache.png)

![Frequencia de falhas por tipo](../charts/failure_frequency_by_type.png)

Graficos adicionais para aprofundamento:

![Tendencia de duracao do pipeline](../charts/pipeline_duration_trend.png)

![Boxplot por modo de execucao](../charts/workflow_duration_by_mode_boxplot.png)

![Decomposicao aproximada do tempo](../charts/step_time_breakdown.png)

![Heatmap de etapas por execucao](../charts/step_duration_heatmap.png)

![Tempo de fila por execucao](../charts/queue_time_by_run.png)

## Resultados quantitativos

- Foram 12 execucoes reais: 11 com sucesso e 1 com falha.
- A unica falha foi do tipo `test`, causada por `intentional_failure=true`.
- O tempo total variou de 30s a 37s.
- A duracao teve p50 de 35s, p90 de 36s e p95 de 36,45s.
- O tempo de fila variou de 1s a 3s, com p50 de 2s.
- O lead time entre commit e conclusao variou de 33s a 45s.
- O lead time teve p50 de 38s, p90 de 40s e p95 de 42,25s.
- O job `read-config` durou em media 3,83s.
- Os jobs paralelos de lint e testes duraram em media 24,20s e 23,60s.
- O job sequencial durou em media 26,50s.
- A instalacao de dependencias foi a etapa dominante: media de 15,43s.
- Lint foi praticamente desprezivel: media de 0,03s.
- Testes tiveram media de 0,73s, com maximo de 2,00s no cenario lento.
- Sem cache, a instalacao levou em media 16,95s; com cache, 14,72s.
- O tamanho agregado dos artefatos por execucao variou de 1605 a 2913 bytes.
- A tentativa ate voltar a verde apos falha foi de 2 execucoes: `controlled-failure` e `recovery-pass`.

## Analise das perguntas

### Qual etapa mais contribuiu para o tempo total?

A instalacao de dependencias foi a etapa que mais contribuiu para o tempo total. Mesmo quando os testes aumentaram para 73 casos, o tempo de teste continuou menor do que 1s em algumas execucoes, enquanto a instalacao ficou entre aproximadamente 13s e 18s.

### Houve diferenca significativa entre execucoes com e sem cache?

Houve diferenca na etapa de instalacao, mas o impacto no tempo total foi limitado. A media de instalacao caiu de 16,95s sem cache para 14,72s com cache, uma economia aproximada de 2,23s. Como o workflow tambem paga custo de inicializacao de runner, checkout, setup de Python e upload de artefatos, a reducao nao apareceu de forma linear no tempo total do pipeline.

### O paralelismo reduziu o tempo total? Em que condicoes?

O paralelismo teve ganho pequeno nesta amostra. Execucoes paralelas tiveram media de 34,2s; as sequenciais, 35,0s. A diferenca foi baixa porque lint e testes sao muito rapidos, e ambos os jobs paralelos repetem instalacao de dependencias. Em um projeto maior, o paralelismo tenderia a ajudar mais se os jobs tivessem carga real e se a instalacao fosse compartilhada ou reduzida.

### Quais falhas foram mais frequentes?

Apenas uma falha ocorreu, e foi do tipo `test`. Ela foi planejada no commit `1fa1567`, com a variacao `controlled-failure`.

### O pipeline fornece feedback rapido o suficiente?

Sim para este projeto pequeno. O feedback ficou entre 30s e 37s de workflow, e o lead time entre 33s e 45s. Para um projeto didatico, isso e rapido. Para um projeto real, o ponto de atencao seria manter instalacao e setup sob controle, pois eles representam a maior parte do tempo.

### Que melhorias poderiam ser feitas?

- Evitar instalar dependencias duplicadamente nos jobs paralelos, ou separar dependencias em ambiente preconstruido.
- Manter cache com chave estavel e invalidacao controlada.
- Publicar um resumo consolidado unico por run, alem dos artefatos por job.
- Medir percentis e nao apenas medias quando houver mais execucoes.
- Adicionar testes mais representativos, porque a suite atual e pequena.
- Incluir matriz de versoes Python apenas se houver necessidade, para nao aumentar custo sem ganho.

### Quais limitacoes existem nos dados coletados?

- A amostra tem apenas 12 execucoes.
- Os runners do GitHub sao compartilhados e variam conforme disponibilidade.
- Os commits foram disparados em sequencia rapida, o que afetou a observacao do cache nos primeiros runs.
- O tempo economizado por cache e uma estimativa baseada na diferenca de instalacao, nao uma metrica nativa do GitHub Actions.
- Os testes sao pequenos e artificiais, entao nao representam uma aplicacao real grande.
- A comparacao sequencial/paralela tem apenas 2 execucoes sequenciais.

### Como essa analise apoia decisoes de engenharia?

A analise mostra onde otimizar primeiro. Neste caso, acelerar testes nao mudaria muito o feedback porque a etapa dominante e instalacao. A decisao mais racional seria melhorar cache, reduzir dependencias ou criar ambiente base antes de investir em paralelismo mais complexo. Tambem mostra que falhas de teste sao detectadas e reportadas com artefato, o que ajuda a decidir se o pipeline oferece rastreabilidade suficiente.

## Resultados inesperados

1. O cenario `baseline-cache-hit` nao apresentou cache hit. Como os commits foram enviados rapidamente, o segundo workflow provavelmente iniciou antes de o cache do primeiro workflow estar salvo e disponivel. Isso mostra que cache em GitHub Actions pode depender da ordem real de conclusao dos jobs, nao apenas da chave configurada.

2. O cenario `parallel-more-tests-60`, com 73 testes, teve o menor tempo total observado: 31s. Isso contradiz a expectativa de que mais testes aumentariam claramente o tempo total. A explicacao mais provavel e que os testes ainda eram leves, enquanto variacao de runner e tempo de instalacao dominaram o resultado.

3. O cenario `sequential-slow` terminou em 34s, menor que o `sequential-baseline` de 36s, mesmo com teste lento. Isso reforca que, nesta escala, o overhead externo do CI foi maior do que a diferenca introduzida por 1,5s de sleep.

## Comparacao entre hipotese e resultado observado

A hipotese de que cache ajudaria foi confirmada na etapa de instalacao, mas nao de forma forte no tempo total. A hipotese de que paralelismo reduziria significativamente a duracao nao se confirmou para este projeto, porque o custo de duplicar setup e instalacao nos jobs paralelos anulou boa parte do beneficio. A hipotese de que mais testes aumentariam o tempo total tambem nao se confirmou claramente, pois o custo dos testes foi pequeno diante do overhead do pipeline.

## Incrementos alem do minimo

Para fortalecer a entrega alem do enunciado minimo, foram adicionados:

- resumo agregado por execucao em `pipeline_run_summary.csv` e `pipeline_run_summary.json`;
- estatisticas consolidadas em `pipeline_stats.json`, incluindo p50, p90 e p95;
- metrica de tempo de fila entre criacao do run e inicio do primeiro job;
- grafico de tendencia temporal;
- boxplot de duracao por modo de execucao;
- decomposicao aproximada do tempo por etapa;
- heatmap das etapas por execucao;
- checklist de rastreabilidade entre requisitos e evidencias.

## Reproducao

```bash
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
  --branch experimento-ci-metricas \
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
