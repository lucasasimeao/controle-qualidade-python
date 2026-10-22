# Controle de Qualidade Industrial em Python + SQLite

> Sistema de terminal que inspeciona peças de uma linha de produção, aprova ou reprova cada uma por critérios de qualidade, salva tudo em SQLite e gera um relatório consolidado.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)

## Sobre o projeto

Protótipo de **automação da inspeção de qualidade** em uma linha de montagem. Em vez de conferir peça por peça manualmente e anotar em papel, o operador digita as medidas e o sistema:

1. aplica as regras de aprovação automaticamente;
2. registra o resultado e o motivo da reprovação;
3. controla quantas caixas de expedição já foram fechadas;
4. gera um relatório com os totais e os motivos de falha.

Projeto acadêmico da graduação em IA e Automação Digital (UniFECAF).

## Funcionalidades

- **Cadastro de peça** (ID, peso, cor e comprimento) com resultado imediato.
- **Regras de qualidade**: a peça é aprovada só se cumprir todos os critérios:
  - peso entre 95 g e 105 g;
  - cor azul ou verde (sem diferenciar maiúsculas e minúsculas);
  - comprimento entre 10 cm e 20 cm.
- **Motivos de reprovação** guardados junto com a peça (ex.: `Peso fora (95g-105g) | Cor inválida`).
- **Listagem** de todo o histórico para rastreabilidade.
- **Remoção** de peça pelo ID.
- **Relatório consolidado** com consultas SQL: total de aprovadas e reprovadas, taxa de aprovação, caixas fechadas (10 peças aprovadas por caixa), peças na caixa atual e lista de motivos de reprovação.
- **Persistência em SQLite**: o banco `producao_industrial.db` é criado na primeira execução.
- Tratamento de entrada inválida para peso e comprimento.

## Tecnologias

- Python 3.11+ (apenas biblioteca padrão)
- SQLite (`sqlite3`) com consultas parametrizadas

## Como executar

```bash
git clone https://github.com/lucasasimeao/controle-qualidade-python.git
cd controle-qualidade-python
python main.py
python -m unittest   # roda os testes
```

Menu:

```text
1. Cadastrar nova peça
2. Listar peças cadastradas
3. Remover peça (ID)
4. Relatório final
0. Sair
```

## Estrutura do projeto

```text
.
├── main.py                  # Camada de dados, regras de qualidade e menu
├── test_main.py             # Testes (unittest) das regras e do banco
└── producao_industrial.db   # Banco SQLite (gerado na execução, fora do Git)
```

O código é dividido em três camadas dentro de `main.py`: **dados** (SQLite), **lógica** (validação e relatório) e **interface** (menu no terminal).

## Competências demonstradas

- **Python** estruturado e modular, com regras de negócio isoladas em funções.
- **SQL** na prática: criação de tabela, `INSERT`/`DELETE` parametrizados e agregações com `COUNT` e filtros.
- **Modelagem de dados** simples para rastreabilidade (status + motivo da falha por peça).
- **Automação de processo industrial** e geração de indicadores de qualidade (taxa de aprovação, motivos de falha).

## Próximos passos

- Gerar o ID automaticamente (hoje ele é digitado; IDs repetidos são recusados com aviso).
- Exportar os dados para CSV e analisar a taxa de reprovação por critério com Pandas.
- Criar um painel simples (Streamlit ou Power BI) com os indicadores do relatório.
