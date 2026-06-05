# Raizes do Nordeste — API Back-End

Projeto academico desenvolvido para a disciplina de Projeto Multidisciplinar (UNINTER).
API REST construida com FastAPI e SQLite, modelando o sistema de pedidos e gestao da rede de restaurantes "Raizes do Nordeste".

---

## Repositorio

```
https://github.com/Guilherme-faria21/raizes-nordeste-api.git
```

---

## Tecnologias

- Python 3.12.3
- FastAPI 0.136.3
- SQLAlchemy 2.0.50
- SQLite (banco de dados local)
- JWT via python-jose
- Hash de senha: bcrypt via passlib (pre-processamento SHA256 + base64)
- Uvicorn 0.49.0

---

## Pre-requisitos

- Python 3.10 ou superior
- pip
- Git

---

## Como executar o projeto

### 1. Clonar o repositorio

```bash
git clone https://github.com/Guilherme-faria21/raizes-nordeste-api.git
cd raizes-nordeste-api 
```

### 2. Criar e ativar o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar as variaveis de ambiente

Copie o arquivo de exemplo e edite com seus valores:

```bash
cp .env.example .env
```

O arquivo `.env` deve conter:

```
DATABASE_URL=sqlite:///./raizes.db
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Para gerar uma SECRET_KEY segura: `python3 -c "import secrets; print(secrets.token_hex(32))"`

### 5. Popular o banco de dados (seed)

```bash
python seed.py
```

Este comando cria as tabelas e insere os dados iniciais:

- 4 usuarios (ADMIN, GERENTE, 2 CLIENTEs)
- 3 unidades (Recife, Fortaleza, Natal)
- 6 produtos tipicos nordestinos
- Estoque inicial de 50 unidades por produto em cada unidade

O script e idempotente — pode ser executado multiplas vezes sem duplicar dados.

### 6. Iniciar a API

```bash
uvicorn main:app --reload
```

A API estara disponivel em: `http://127.0.0.1:8000`

---

## Documentacao (Swagger)

Apos iniciar a API, acesse:

```
http://127.0.0.1:8000/docs
```

A documentacao interativa (OpenAPI/Swagger) lista todos os endpoints, contratos de request/response e permite testar as rotas diretamente pelo navegador.

---

## Credenciais de teste (apos o seed)

| Perfil  | E-mail                | Senha        |
|---------|-----------------------|--------------|
| ADMIN   | admin@raizes.com      | Admin@123    |
| GERENTE | gerente@raizes.com    | Gerente@123  |
| CLIENTE | maria@email.com       | Cliente@123  |
| CLIENTE | joao@email.com        | Cliente@123  |

---

## Colecao de testes Postman

O arquivo `raizes_nordeste_postman.json` na raiz do repositorio contem 12 cenarios de teste (7 positivos, 5 negativos) cobrindo:

- Autenticacao (login valido e senha errada)
- Criacao de pedido e validacao de status
- Filtro de pedidos por canal
- Programa de fidelidade (saldo e resgate)
- Logs de auditoria
- Cenarios de erro: 401, 403, 404, 409

### Como importar

1. Abra o Postman
2. Clique em **Import**
3. Selecione o arquivo `raizes_nordeste_postman.json`
4. Execute a colecao pelo **Runner** na ordem de 01 a 12

Os requests 03 em diante dependem dos tokens salvos automaticamente pelos requests 01 e 02. Execute sempre na ordem.

---

## Arquitetura do projeto

```
raizes_nordeste/
├── main.py                          # Ponto de entrada da aplicacao
├── seed.py                          # Script de dados iniciais
├── requirements.txt                 # Dependencias do projeto
├── .env                             # Variaveis de ambiente (nao versionar)
├── .env.example                     # Modelo de variaveis de ambiente
├── raizes_nordeste_postman.json     # Colecao de testes Postman
└── app/
    ├── api/                         # Routers e endpoints (controllers)
    │   ├── auth.py                  # POST /auth/login
    │   ├── unidades.py              # CRUD /unidades
    │   ├── produtos.py              # CRUD /produtos
    │   ├── estoque.py               # Movimentacao /estoque
    │   ├── pedidos.py               # Fluxo de pedidos /pedidos
    │   ├── fidelidade.py            # Programa de pontos /fidelidade
    │   └── auditoria.py             # Logs de auditoria /auditoria
    ├── application/                 # Servicos e casos de uso
    │   ├── fidelidade_service.py    # Logica de acumulo e resgate de pontos
    │   └── auditoria_service.py     # Registro de logs de auditoria
    └── infrastructure/              # Persistencia e seguranca
        ├── database.py              # Configuracao do SQLAlchemy
        ├── models.py                # Modelos ORM (tabelas)
        └── security.py             # Hash de senha e JWT
```

---

## Endpoints principais

| Metodo | Rota                        | Descricao                          | Auth       |
|--------|-----------------------------|------------------------------------|------------|
| POST   | /auth/login                 | Autenticacao, retorna JWT          | Nao        |
| GET    | /unidades/                  | Lista unidades ativas              | Nao        |
| GET    | /produtos/                  | Lista produtos ativos              | Nao        |
| POST   | /estoque/entrada            | Registra entrada de estoque        | ADMIN/GER  |
| GET    | /estoque/{unidade_id}       | Consulta estoque por unidade       | Autenticado|
| POST   | /pedidos/                   | Cria pedido com pagamento mock     | CLIENTE    |
| GET    | /pedidos/                   | Lista pedidos (filtro ?canal_pedido)| Autenticado|
| GET    | /fidelidade/saldo           | Consulta pontos do usuario         | Autenticado|
| POST   | /fidelidade/resgatar        | Resgata pontos de fidelidade       | Autenticado|
| GET    | /auditoria/                 | Lista logs de auditoria            | ADMIN      |

---

## Seguranca e LGPD

- Senhas armazenadas com hash bcrypt (pre-processamento SHA256 + base64)
- Autenticacao via JWT (Bearer Token), expiracao configuravel via .env
- Autorizacao por perfis: ADMIN, GERENTE, ATENDENTE, CLIENTE
- Consentimento LGPD registrado obrigatoriamente no cadastro de usuario
- Soft-delete em todos os recursos (campo `ativo = False`, sem exclusao fisica)
- Logs de auditoria para acoes sensiveis: LOGIN, CRIAR_PEDIDO, PAGAMENTO_RECUSADO, RESGATAR_PONTOS, ENTRADA_ESTOQUE
- Dados pessoais nao expostos em respostas de erro

---

## Regras de negocio principais

- Estoque e baixado apenas quando o pagamento e aprovado
- Pagamento mock: PIX e aprovado, DINHEIRO aprovado, CREDITO recusado (simulacao)
- Programa de fidelidade: 1 ponto por R$1,00 gasto (arredondamento para baixo)
- Pontos so acumulam em pedidos com pagamento aprovado
- Canal do pedido obrigatorio: APP, TOTEM, BALCAO, PICKUP ou WEB
- Todos os deletes sao logicos (soft-delete)

---

## Como rodar os testes

Importe a colecao `raizes_nordeste_postman.json` no Postman e execute pelo Runner.
Resultado esperado: 30 testes — Passed (30), Failed (0).