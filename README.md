# Vibe Coding - Sistema de Gestão de Automóveis

Este projeto foi desenvolvido como uma aplicação web de gerenciamento de automóveis, com foco em cadastro de veículos, categorias, clientes, usuários, reservas e vendas. A aplicação foi construída com Streamlit, SQLAlchemy e suporte a SQLite para testes locais e MySQL para produção.

## Objetivo

O sistema permite:

- cadastrar e consultar veículos;
- registrar proprietários e clientes;
- organizar categorias e organizações;
- controlar reservas e vendas;
- manter registros históricos e facilitar a operação diária de uma revenda ou concessionária.

## Stack

- Streamlit
- SQLAlchemy
- SQLite (desenvolvimento/testes)
- MySQL + PyMySQL (produção)
- uv para gerenciamento de dependências

## Estrutura do projeto

```text
.
├── README.md
├── .gitignore
├── pyproject.toml
├── src/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   └── __init__.py
├── tests/
│   └── test_database.py
└── .env.example
```

## Pré-requisitos

- Python 3.11+
- uv instalado

## Instalação

1. Abra o terminal na raiz do projeto.
2. Execute:

```bash
uv sync
```

3. Crie um arquivo `.env` baseado em `.env.example`.

## Configuração de banco de dados

O sistema usa SQLite por padrão em ambiente local e MySQL quando a variável de ambiente `APP_ENV=production` estiver ativa.

Exemplo de `.env`:

```env
APP_ENV=local
SQLITE_DATABASE_URL=sqlite:///./local.db
MYSQL_DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/vibe_coding
```

Em produção, a aplicação usa `MYSQL_DATABASE_URL` para conectar ao MySQL.

## Execução

Para iniciar a aplicação:

```bash
uv run streamlit run src/app.py
```

A interface web abrirá no navegador local e permitirá o gerenciamento das entidades do sistema.

## Observações

- O SQLite é indicado para testes locais e desenvolvimento.
- O MySQL é a opção de produção e deve ser configurado por variável de ambiente.
- Os arquivos de código ficam dentro da pasta `src`, como solicitado no projeto.
