# Base livre usada no experimento

Este experimento usa como base o projeto livre [PyPA sampleproject](https://github.com/pypa/sampleproject).

## Motivo da escolha

O `sampleproject` e pequeno, publico, mantido pela Python Packaging Authority e possui licenca MIT. Ele e adequado para um experimento de CI/CD porque permite instalar dependencias, executar lint, rodar testes automatizados e variar o comportamento do pipeline sem introduzir complexidade de dominio.

## Adaptacoes feitas

- Mantido o pacote Python `sample`.
- Mantida a funcao base `add_one`.
- Mantida a licenca MIT original em `LICENSE.txt`.
- Adicionados testes Pytest controlados por `experiment_config.json`.
- Adicionados scripts de instrumentacao, coleta de metricas, graficos e relatorio.

## Referencias

- Repositorio original: <https://github.com/pypa/sampleproject>
- Licenca original: <https://github.com/pypa/sampleproject/blob/main/LICENSE.txt>
