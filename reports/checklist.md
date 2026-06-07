# Checklist de rastreabilidade dos requisitos

Este arquivo mapeia cada requisito para evidência correspondente no repositório.

| Requisito | Status | Evidência |
|---|---|---|
| Link do repositório GitHub | Feito | <https://github.com/NicolasRamonm/ponderada-hermano-03-06> |
| Projeto pequeno existente e livre como base | Feito | PyPA `sampleproject`, documentado em [`PROJECT_BASE.md`](../PROJECT_BASE.md) |
| Licença do projeto-base preservada | Feito | [`LICENSE.txt`](../LICENSE.txt) |
| Pipeline no GitHub Actions | Feito | [`.github/workflows/ci-metrics.yml`](../.github/workflows/ci-metrics.yml) |
| README permite rodar e testar | Feito | [`README.md`](../README.md), seções "Como rodar localmente" e "Como reproduzir o experimento completo" |
| Instalação de dependências | Feito | Etapa `Install dependencies` no workflow |
| Lint ou análise estática | Feito | Etapa `Lint` com Ruff |
| Testes automatizados | Feito | [`tests/test_sample.py`](../tests/test_sample.py) |
| Artefato com resultados | Feito | `actions/upload-artifact` publica `ci_summary.json`, `junit.xml` e `step_metrics.jsonl` |
| Coleta de métricas do pipeline | Feito | [`scripts/collect_metrics.py`](../scripts/collect_metrics.py) |
| Pelo menos 12 execuções reais | Feito | 12 run IDs reais em [`reports/relatorio.md`](./relatorio.md) |
| Variações controladas | Feito | `experiment_config.json` variado por commit; tabela no relatório |
| Teste passando | Feito | Runs `baseline-pass`, `recovery-pass`, `final-green` |
| Teste falhando | Feito | Run `controlled-failure`, ID `27102200902` |
| Aumento artificial da quantidade de testes | Feito | Runs `more-tests-25` e `parallel-more-tests-60` |
| Teste lento | Feito | Runs `slow-test-1500ms` e `sequential-slow` |
| Alteração no cache | Feito | Runs `cache-bust` e `cache-hit-after-bust` |
| Execução sequencial e paralela | Feito | `execution_mode=sequential` e `execution_mode=parallel` |
| Tempo total do workflow | Feito | Coluna `workflow_duration_seconds` em [`data/pipeline_metrics.csv`](../data/pipeline_metrics.csv) |
| Tempo de cada job | Feito | Coluna `job_duration_seconds` |
| Tempo de etapas relevantes | Feito | Colunas `install_duration_seconds`, `lint_duration_seconds`, `test_duration_seconds` |
| Status da execução | Feito | Colunas `status` e `job_status` |
| Quantidade de testes | Feito | Coluna `test_count` |
| Quantidade de falhas de teste | Feito | Coluna `test_failures` |
| Tempo médio dos testes | Feito | Coluna `test_average_seconds` |
| Número do commit | Feito | Coluna `commit_sha` |
| Data e hora da execução | Feito | Coluna `timestamp` |
| Mensagem resumida do commit | Feito | Coluna `commit_message` |
| Tempo economizado com cache | Feito | Coluna `cache_saved_seconds_estimate` |
| Tamanho dos artefatos | Feito | Coluna `artifact_size_bytes` |
| Tentativas até pipeline verde | Feito | Coluna `attempts_until_green` |
| Frequência de falhas por tipo | Feito | Coluna `failure_type` e gráfico `failure_frequency_by_type.png` |
| Lead time commit até conclusão | Feito | Coluna `lead_time_seconds` |
| Script Python próprio | Feito | [`scripts/collect_metrics.py`](../scripts/collect_metrics.py) consulta API do GitHub e baixa artefatos |
| Base CSV ou JSON | Feito | [`data/pipeline_metrics.csv`](../data/pipeline_metrics.csv), [`data/pipeline_metrics.json`](../data/pipeline_metrics.json) |
| Gráfico de tempo total por execução | Feito | [`charts/pipeline_duration_by_run.png`](../charts/pipeline_duration_by_run.png) |
| Gráfico de tempo por job/etapa | Feito | [`charts/job_duration_by_run.png`](../charts/job_duration_by_run.png), [`charts/step_time_breakdown.png`](../charts/step_time_breakdown.png) |
| Gráfico de sucesso e falha | Feito | [`charts/success_failure_rate.png`](../charts/success_failure_rate.png) |
| Gráfico testes vs duração | Feito | [`charts/tests_vs_pipeline_duration.png`](../charts/tests_vs_pipeline_duration.png) |
| Relatório técnico Markdown | Feito | [`reports/relatorio.md`](./relatorio.md) |
| Links das execuções reais | Feito | Seção "Execuções reais do GitHub Actions" do relatório |
| IDs reais dos workflows | Feito | Run IDs `27102177249` a `27102240744` no relatório |
| Explicação das variações | Feito | Seções "Desenho do experimento" e "Execuções reais" |
| Gráficos a partir dos dados coletados | Feito | Arquivos em [`charts/`](../charts) gerados por `generate_charts.py` |
| Dois resultados inesperados | Feito | Seção "Resultados inesperados" possui três itens |
| Hipótese vs resultado observado | Feito | Seção "Comparação entre hipótese e resultado observado" |
| Limitações do experimento | Feito | Subseção "Quais limitações existem nos dados coletados?" |

## Outro

| Incremento | Evidência |
|---|---|
| Resumo por execução | [`data/pipeline_run_summary.csv`](../data/pipeline_run_summary.csv) e [`data/pipeline_run_summary.json`](../data/pipeline_run_summary.json) |
| Percentis p50/p90/p95 | [`data/pipeline_stats.json`](../data/pipeline_stats.json) |
| Tempo de fila | Coluna `queue_duration_seconds` |
| Tendência temporal | [`charts/pipeline_duration_trend.png`](../charts/pipeline_duration_trend.png) |
| Boxplot por modo | [`charts/workflow_duration_by_mode_boxplot.png`](../charts/workflow_duration_by_mode_boxplot.png) |
| Heatmap de etapas | [`charts/step_duration_heatmap.png`](../charts/step_duration_heatmap.png) |
| Decomposição do tempo | [`charts/step_time_breakdown.png`](../charts/step_time_breakdown.png) |
