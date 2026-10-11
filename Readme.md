# Stock Management System

Projeto pessoal para praticar Python, SQLite, organização por camadas e conceitos de consistência e atomicidade.

## Objetivo

O sistema permite gerir produtos, stock por produto, entradas e saídas de stock, histórico de movimentos e informação resumida para um dashboard.

## Tecnologias

- Python
- SQLite
- `sqlite3`
- `unittest`

## Estrutura do projeto

```text
model/      Entidades e regras básicas dos objetos
repo/       Acesso à base de dados
service/    Regras de negócio e coordenação dos casos de uso
utils/      Funções auxiliares
tests/      Testes automatizados
database.py Configuração da ligação e criação das tabelas
main.py     Ponto de entrada para executar exemplos
```

## Modelo de dados

O sistema utiliza três tabelas principais:

- `products`: dados dos produtos;
- `stocks`: quantidade atual por produto;
- `movements`: histórico de entradas e saídas.

Cada produto tem um único registo de stock. Os movimentos registam a alteração efetuada, a quantidade e uma nota opcional.

## Atomicidade do stock

Uma alteração de stock é composta por duas operações:

1. atualizar a quantidade em `stocks`;
2. registar o movimento em `movements`.

Estas operações são executadas na mesma transação SQLite. Se alguma falhar, toda a operação é revertida através de `ROLLBACK`. Assim, o stock e o respetivo histórico permanecem consistentes.

Durante a transação, a quantidade atual é lida depois de a transação ser iniciada. Nas saídas, o sistema valida se existe quantidade suficiente antes de atualizar o stock.

## Regras principais

- o nome do produto é obrigatório;
- o preço não pode ser negativo;
- a quantidade de stock não pode ser negativa;
- o stock pode começar com quantidade zero;
- uma saída não pode ultrapassar o stock disponível;
- cada produto pode ter apenas um registo na tabela `stocks`;
- produtos e movimentos utilizam identificadores UUID.

## Como executar

Criar e ativar um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

Executar o programa:

```bash
python main.py
```

Se necessário, a base de dados pode ser inicializada através de `create_table()` em `database.py`.

## Executar os testes

```bash
python -m unittest discover -s tests -v
```

Os testes encontram-se em `tests/` e cobrem as regras dos modelos. A cobertura será expandida para os serviços, repositórios, transações e concorrência.

## Objetivos de aprendizagem

Este projeto está a ser desenvolvido para praticar:

- programação orientada a objetos;
- separação entre modelo, serviço e repositório;
- validação de dados;
- transações e rollback;
- atomicidade;
- integridade referencial em SQLite;
- testes automatizados;
- paginação e consultas agregadas.

## Próximos passos

- aumentar a cobertura de testes;
- testar explicitamente rollback de transações;
- testar operações concorrentes de stock;
- melhorar o sistema de migrações da base de dados;
- separar a criação da ligação SQLite da configuração do schema;
- adicionar uma interface HTTP ou gráfica.
