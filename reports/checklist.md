# Checklist de rastreabilidade dos requisitos

Este arquivo mapeia cada requisito do enunciado para a evidencia correspondente no repositorio.

| Requisito | Status | Evidencia |
|---|---|---|
| Link do repositorio GitHub | Feito | <https://github.com/NicolasRamonm/ponderada-hermano-03-06> |
| Pipeline no GitHub Actions | Feito | [`.github/workflows/ci-metrics.yml`](../.github/workflows/ci-metrics.yml) |
| Instalacao de dependencias | Feito | Job `Install dependencies` no workflow |
| Lint ou analise estatica | Feito | Job/etapa `Lint` com Ruff |
| Testes automatizados | Feito | Pytest em [`tests/test_calculator.py`](../tests/test_calculator.py) |
| Artefato com resultados | Feito | `actions/upload-artifact` publica `ci_summary.json`, `junit.xml` e `step_metrics.jsonl` |
| Coleta de metricas do pipeline | Feito | [`scripts/collect_metrics.py`](../scripts/collect_metrics.py) |
| Pelo menos 12 execucoes reais | Feito | 12 run IDs reais em [`reports/relatorio.md`](./relatorio.md) |
| Variacoes controladas | Feito | `experiment_config.json` variado por commit; tabela no relatorio |
| Teste passando | Feito | Runs `baseline-pass`, `recovery-pass`, `final-green` |
| Teste falhando | Feito | Run `controlled-failure`, ID `27101403237` |
| Aumento artificial da quantidade de testes | Feito | Runs `more-tests-25` e `parallel-more-tests-60` |
| Teste lento | Feito | Runs `slow-test-1500ms` e `sequential-slow` |
| Alteracao no cache | Feito | Runs `cache-bust` e `cache-hit-after-bust` |
| Execucao sequencial e paralela | Feito | `execution_mode=sequential` e `execution_mode=parallel` |
| Tempo total do workflow | Feito | Coluna `workflow_duration_seconds` em [`data/pipeline_metrics.csv`](../data/pipeline_metrics.csv) |
| Tempo de cada job | Feito | Coluna `job_duration_seconds` |
| Tempo de etapas relevantes | Feito | Colunas `install_duration_seconds`, `lint_duration_seconds`, `test_duration_seconds` |
| Status da execucao | Feito | Colunas `status` e `job_status` |
| Quantidade de testes | Feito | Coluna `test_count` |
| Quantidade de falhas de teste | Feito | Coluna `test_failures` |
| Tempo medio dos testes | Feito | Coluna `test_average_seconds` |
| Numero do commit | Feito | Coluna `commit_sha` |
| Data e hora da execucao | Feito | Coluna `timestamp` |
| Mensagem resumida do commit | Feito | Coluna `commit_message` |
| Tempo economizado com cache | Feito | Coluna `cache_saved_seconds_estimate` |
| Tamanho dos artefatos | Feito | Coluna `artifact_size_bytes` |
| Tentativas ate pipeline verde | Feito | Coluna `attempts_until_green` |
| Frequencia de falhas por tipo | Feito | Coluna `failure_type` e grafico `failure_frequency_by_type.png` |
| Lead time commit ate conclusao | Feito | Coluna `lead_time_seconds` |
| Script Python proprio | Feito | [`scripts/collect_metrics.py`](../scripts/collect_metrics.py) consulta API do GitHub e baixa artefatos |
| Base CSV ou JSON | Feito | [`data/pipeline_metrics.csv`](../data/pipeline_metrics.csv), [`data/pipeline_metrics.json`](../data/pipeline_metrics.json) |
| Grafico de tempo total por execucao | Feito | [`charts/pipeline_duration_by_run.png`](../charts/pipeline_duration_by_run.png) |
| Grafico de tempo por job/etapa | Feito | [`charts/job_duration_by_run.png`](../charts/job_duration_by_run.png), [`charts/step_time_breakdown.png`](../charts/step_time_breakdown.png) |
| Grafico de sucesso e falha | Feito | [`charts/success_failure_rate.png`](../charts/success_failure_rate.png) |
| Grafico testes vs duracao | Feito | [`charts/tests_vs_pipeline_duration.png`](../charts/tests_vs_pipeline_duration.png) |
| Relatorio tecnico Markdown | Feito | [`reports/relatorio.md`](./relatorio.md) |
| Links das execucoes reais | Feito | Secao "Execucoes reais do GitHub Actions" do relatorio |
| IDs reais dos workflows | Feito | Run IDs `27101381991` a `27101435614` no relatorio |
| Commits reais usados | Feito | Secao "Commits usados" do relatorio |
| Explicacao das variacoes | Feito | Secoes "Desenho do experimento" e "Execucoes reais" |
| Graficos a partir dos dados coletados | Feito | Arquivos em [`charts/`](../charts) gerados por `generate_charts.py` |
| Dois resultados inesperados | Feito | Secao "Resultados inesperados" possui tres itens |
| Hipotese vs resultado observado | Feito | Secao "Comparacao entre hipotese e resultado observado" |
| Limitacoes do experimento | Feito | Subsecao "Quais limitacoes existem nos dados coletados?" |
| Padrao de branch sem Codex | Feito | Branch `experimento-ci-metricas` |
| Commits ligados a conta do aluno | Feito | Commits autorados por `Nicolas Ramon da Silva <nnicolasramonn@gmail.com>` |

## Evidencias adicionais alem do minimo

| Incremento | Evidencia |
|---|---|
| Resumo por execucao | [`data/pipeline_run_summary.csv`](../data/pipeline_run_summary.csv) e [`data/pipeline_run_summary.json`](../data/pipeline_run_summary.json) |
| Percentis p50/p90/p95 | [`data/pipeline_stats.json`](../data/pipeline_stats.json) |
| Tempo de fila | Coluna `queue_duration_seconds` |
| Tendencia temporal | [`charts/pipeline_duration_trend.png`](../charts/pipeline_duration_trend.png) |
| Boxplot por modo | [`charts/workflow_duration_by_mode_boxplot.png`](../charts/workflow_duration_by_mode_boxplot.png) |
| Heatmap de etapas | [`charts/step_duration_heatmap.png`](../charts/step_duration_heatmap.png) |
| Decomposicao do tempo | [`charts/step_time_breakdown.png`](../charts/step_time_breakdown.png) |
