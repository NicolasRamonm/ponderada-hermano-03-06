# Base livre usada no experimento

Este experimento usa como base o projeto livre [PyPA sampleproject](https://github.com/pypa/sampleproject).

## Motivo da escolha

O `sampleproject` é pequeno, público, mantido pela Python Packaging Authority e possui licença MIT. Ele é adequado para um experimento de CI/CD porque permite instalar dependências, executar lint, rodar testes automatizados e variar o comportamento do pipeline sem introduzir complexidade de domínio.

## Adaptações feitas

- Mantido o pacote Python `sample`.
- Mantida a função base `add_one`.
- Mantida a licença MIT original em `LICENSE.txt`.
- Adicionados testes Pytest controlados por `experiment_config.json`.
- Adicionados scripts de instrumentação, coleta de métricas, gráficos e relatório.

## Referências

- Repositório original: <https://github.com/pypa/sampleproject>
- Licença original: <https://github.com/pypa/sampleproject/blob/main/LICENSE.txt>
