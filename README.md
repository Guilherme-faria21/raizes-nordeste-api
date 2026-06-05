# API REST para Gestão de Pedidos — Rede Raízes do Nordeste

Projeto desenvolvido para a disciplina **Projeto Multidisciplinar — Trilha Back-End** do curso de **Tecnologia em Análise e Desenvolvimento de Sistemas**.

A aplicação implementa uma API REST para gestão de pedidos da rede fictícia **Raízes do Nordeste**, com autenticação JWT, controle de acesso por perfis, unidades, produtos, estoque, pedidos, pagamento mock determinístico, fidelidade e auditoria.

---

## 1. Visão Geral

O objetivo do projeto é demonstrar um fluxo back-end funcional, persistente e testável para uma rede de restaurantes/lanchonetes com múltiplas unidades e múltiplos canais de pedido.

Fluxo principal implementado:

```text
Cliente autenticado
        ↓
Criação de pedido
        ↓
Validação de unidade, produtos e estoque
        ↓
Pagamento mock determinístico
        ↓
Atualização automática do status do pedido
        ↓
Baixa de estoque em caso de aprovação
        ↓
Acúmulo de pontos de fidelidade
        ↓
Registro de auditoria
```

Fluxo obrigatório escolhido no roteiro:

```text
Pedido → Pagamento mock → Atualização de status
```

---

## 2. Funcionalidades Implementadas

- Cadastro de usuários com consentimento LGPD.
- Login com JWT.
- Autorização por perfis/roles.
- Gestão de unidades.
- Gestão de produtos.
- Consulta e entrada de estoque por unidade.
- Registro de movimentações de estoque.
- Criação de pedidos com itens, canal de origem e forma de pagamento.
- Campo de multicanalidade no pedido: `canal_pedido`.
- Filtro de pedidos por canal.
- Pagamento mock determinístico.
- Atualização automática do status do pedido conforme pagamento.
- Baixa de estoque em pedidos aprovados.
- Programa de fidelidade com consulta e resgate de pontos.
- Auditoria de ações relevantes.
- Soft-delete em unidades e produtos.
- Documentação automática via Swagger/OpenAPI.
- Coleção Postman com testes positivos e negativos.

---

## 3. Requisitos Atendidos

### 3.1 Requisitos Funcionais

| ID | Requisito | Status |
|---|---|---|
| RF01 | Cadastro de usuário com nome, e-mail, senha, perfil e consentimento LGPD | Implementado |
| RF02 | Login com e-mail e senha, retornando token JWT | Implementado |
| RF03 | Listagem e consulta de unidades ativas | Implementado |
| RF04 | Cadastro, atualização e desativação de unidades | Implementado |
| RF05 | Listagem e consulta de produtos ativos | Implementado |
| RF06 | Cadastro, atualização e desativação de produtos | Implementado |
| RF07 | Consulta de estoque por unidade | Implementado |
| RF08 | Registro de entrada de estoque | Implementado |
| RF09 | Consulta de movimentações de estoque | Implementado |
| RF10 | Criação de pedido com unidade, canal, forma de pagamento e itens | Implementado |
| RF11 | Validação de estoque antes da criação do pedido | Implementado |
| RF12 | Processamento de pagamento mock | Implementado |
| RF13 | Atualização de status conforme resultado do pagamento | Implementado |
| RF14 | Baixa de estoque em pedidos aprovados | Implementado |
| RF15 | Acúmulo de pontos de fidelidade em pedidos aprovados | Implementado |
| RF16 | Consulta de saldo de fidelidade pelo cliente | Implementado |
| RF17 | Consulta de saldo de fidelidade por administradores/gerentes | Implementado |
| RF18 | Resgate de pontos | Implementado |
| RF19 | Registro de auditoria | Implementado |
| RF20 | Consulta de auditoria com filtros | Implementado |
| RF21 | Atualização manual de status pela cozinha | Documentado como regra conceitual |
| RF22 | Promoções/campanhas | Documentado como proposta |

### 3.2 Requisitos Não Funcionais

- Arquitetura modular.
- Persistência em banco de dados.
- ORM com SQLAlchemy.
- Autenticação JWT.
- Autorização por perfil.
- Senhas armazenadas com hash.
- Documentação Swagger/OpenAPI.
- Padrão de erro em JSON.
- Auditoria de ações sensíveis.
- Pagamento mock determinístico.
- Testes reproduzíveis via Postman.

---

## 4. Stack Tecnológica

| Tecnologia | Função |
|---|---|
| Python | Linguagem principal |
| FastAPI | Framework web |
| Uvicorn | Servidor ASGI |
| SQLAlchemy | ORM |
| SQLite | Banco de dados local |
| Pydantic | Validação de dados |
| Passlib | Hashing de senhas |
| bcrypt | Algoritmo de hash usado pelo Passlib |
| python-jose | Geração e validação de JWT |
| python-dotenv | Variáveis de ambiente |
| python-multipart | Suporte a login via form-data |
| email-validator | Validação de e-mail no Pydantic |
| Postman | Testes da API |

---

## 5. Estrutura do Projeto

```text
raizes_nordeste/
├── main.py
├── seed.py
├── requirements.txt
├── README.md
├── .env.example
├── raizes_nordeste_postman.json
└── app/
    ├── api/
    │   ├── auth.py
    │   ├── unidades.py
    │   ├── produtos.py
    │   ├── estoque.py
    │   ├── pedidos.py
    │   ├── fidelidade.py
    │   ├── auditoria.py
    │   └── deps.py
    ├── application/
    │   ├── auditoria_service.py
    │   ├── fidelidade_service.py
    │   └── pagamento_service.py
    ├── infrastructure/
    │   ├── database.py
    │   ├── models.py
    │   └── security.py
    └── domain/
        └── __init__.py
```

---

## 6. Como Executar o Projeto

### 6.1 Clonar o repositório

```bash
git clone https://github.com/Guilherme-faria21/raizes-nordeste-api.git
cd raizes-nordeste-api
```

### 6.2 Criar e ativar ambiente virtual

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 6.3 Instalar dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 6.4 Configurar variáveis de ambiente

O projeto possui o arquivo `.env.example`.

Crie uma cópia chamada `.env`:

```bash
cp .env.example .env
```

Exemplo de variáveis esperadas:

```env
SECRET_KEY=sua-chave-secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./raizes.db
```

Caso o projeto já esteja configurado com valores padrão compatíveis com ambiente local, basta manter o `.env.example` como referência.

### 6.5 Criar banco e executar seed

```bash
python seed.py
```

O seed cria usuários, unidades, produtos e estoques iniciais.

Saída esperada:

```text
Seed concluido com sucesso!

Credenciais para teste:
  ADMIN   -> admin@raizes.com   / Admin@123
  GERENTE -> gerente@raizes.com / Gerente@123
  CLIENTE -> maria@email.com    / Cliente@123
  CLIENTE -> joao@email.com     / Cliente@123
```

### 6.6 Iniciar a API

```bash
uvicorn main:app --reload
```

API local:

```text
http://127.0.0.1:8000
```

---

## 7. Documentação Swagger/OpenAPI

Com a API rodando, acesse:

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI JSON:

```text
http://127.0.0.1:8000/openapi.json
```

---

## 8. Credenciais de Teste

| Perfil | E-mail | Senha |
|---|---|---|
| ADMIN | `admin@raizes.com` | `Admin@123` |
| GERENTE | `gerente@raizes.com` | `Gerente@123` |
| CLIENTE | `maria@email.com` | `Cliente@123` |
| CLIENTE | `joao@email.com` | `Cliente@123` |

---

## 9. Endpoints Principais

### 9.1 Autenticação

| Método | Endpoint | Acesso | Descrição |
|---|---|---|---|
| POST | `/auth/registro` | Público | Cadastra usuário |
| POST | `/auth/login` | Público | Autentica usuário e retorna JWT |

Exemplo de login:

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@raizes.com&password=Admin@123"
```

### 9.2 Unidades

| Método | Endpoint | Acesso | Descrição |
|---|---|---|---|
| GET | `/unidades/` | Público | Lista unidades ativas |
| GET | `/unidades/{unidade_id}` | Público | Consulta unidade |
| POST | `/unidades/` | ADMIN / GERENTE | Cria unidade |
| PUT | `/unidades/{unidade_id}` | ADMIN / GERENTE | Atualiza unidade |
| DELETE | `/unidades/{unidade_id}` | ADMIN | Soft-delete da unidade |

### 9.3 Produtos

| Método | Endpoint | Acesso | Descrição |
|---|---|---|---|
| GET | `/produtos/` | Público | Lista produtos ativos |
| GET | `/produtos/{produto_id}` | Público | Consulta produto |
| POST | `/produtos/` | ADMIN / GERENTE | Cria produto |
| PUT | `/produtos/{produto_id}` | ADMIN / GERENTE | Atualiza produto |
| DELETE | `/produtos/{produto_id}` | ADMIN / GERENTE | Soft-delete do produto |

### 9.4 Estoque

| Método | Endpoint | Acesso | Descrição |
|---|---|---|---|
| GET | `/estoque/{unidade_id}` | ADMIN / GERENTE | Consulta estoque da unidade |
| POST | `/estoque/entrada` | ADMIN / GERENTE | Registra entrada |
| GET | `/estoque/{unidade_id}/movimentacoes` | ADMIN / GERENTE | Lista movimentações |

### 9.5 Pedidos

| Método | Endpoint | Acesso | Descrição |
|---|---|---|---|
| POST | `/pedidos/` | CLIENTE | Cria pedido e processa pagamento mock |
| GET | `/pedidos/` | ADMIN / GERENTE / CLIENTE | Lista pedidos conforme perfil |
| GET | `/pedidos/{pedido_id}` | ADMIN / GERENTE / dono do pedido | Consulta pedido |

Filtro por canal:

```text
GET /pedidos/?canal_pedido=APP
```

### 9.6 Fidelidade

| Método | Endpoint | Acesso | Descrição |
|---|---|---|---|
| GET | `/fidelidade/saldo` | CLIENTE | Consulta saldo próprio |
| GET | `/fidelidade/saldo/{usuario_id}` | ADMIN / GERENTE | Consulta saldo de outro usuário |
| POST | `/fidelidade/resgatar` | CLIENTE | Resgata pontos |

### 9.7 Auditoria

| Método | Endpoint | Acesso | Descrição |
|---|---|---|---|
| GET | `/auditoria/` | ADMIN | Lista logs de auditoria |

---

## 10. Fluxo Principal

### 10.1 Login do cliente

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=maria@email.com&password=Cliente@123"
```

O retorno contém o token JWT:

```json
{
  "access_token": "TOKEN_JWT",
  "token_type": "bearer",
  "perfil": "CLIENTE",
  "nome": "Maria"
}
```

### 10.2 Criar pedido aprovado

```bash
curl -X POST http://127.0.0.1:8000/pedidos/ \
  -H "Authorization: Bearer TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "unidade_id": 1,
    "canal_pedido": "APP",
    "forma_pagamento": "PIX",
    "itens": [
      {"produto_id": 1, "quantidade": 1}
    ]
  }'
```

Resposta esperada:

```json
{
  "status": "EM_PREPARO",
  "forma_pagamento": "PIX",
  "pagamento": {
    "status": "APROVADO",
    "metodo": "PIX"
  }
}
```

### 10.3 Criar pedido recusado

```bash
curl -X POST http://127.0.0.1:8000/pedidos/ \
  -H "Authorization: Bearer TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "unidade_id": 1,
    "canal_pedido": "APP",
    "forma_pagamento": "MOCK_RECUSADO",
    "itens": [
      {"produto_id": 1, "quantidade": 1}
    ]
  }'
```

Resposta esperada:

```json
{
  "status": "PAGAMENTO_RECUSADO",
  "forma_pagamento": "MOCK_RECUSADO",
  "pagamento": {
    "status": "RECUSADO",
    "metodo": "MOCK_RECUSADO"
  }
}
```

---

## 11. Pagamento Mock Determinístico

O serviço de pagamento mock está em:

```text
app/application/pagamento_service.py
```

Métodos aprovados:

- `PIX`
- `CARTAO_CREDITO`
- `CARTAO_DEBITO`
- `DINHEIRO`
- `MOCK`

Métodos recusados:

- `RECUSADO`
- `MOCK_RECUSADO`
- `CARTAO_RECUSADO`
- `CARTAO_CREDITO_RECUSADO`

Esse comportamento determinístico facilita a execução dos testes, porque o mesmo cenário sempre retorna o mesmo resultado.

---

## 12. Multicanalidade

O pedido possui o campo:

```text
canal_pedido
```

Valores esperados:

- `APP`
- `TOTEM`
- `BALCAO`
- `PICKUP`
- `WEB`

Esse campo permite rastrear a origem do pedido.

Exemplo:

```json
{
  "canal_pedido": "APP"
}
```

Filtro por canal:

```text
GET /pedidos/?canal_pedido=APP
```

---

## 13. Segurança e LGPD

Controles implementados:

- Hash de senha com Passlib + bcrypt.
- Preparação de senha com SHA-256 + Base64 antes do bcrypt.
- JWT para autenticação.
- Autorização por perfil.
- Consentimento LGPD no cadastro.
- Minimização de dados.
- Soft-delete em recursos principais.
- Auditoria de ações relevantes.
- Não armazenamento de senha em texto puro.

---

## 14. Testes com Postman

A coleção Postman está disponível no repositório:

```text
raizes_nordeste_postman.json
```

A execução final da coleção resultou em:

```text
46/46 asserções aprovadas
```

### 14.1 Como executar os testes

1. Inicie a API localmente:

```bash
uvicorn main:app --reload
```

2. Importe o arquivo no Postman:

```text
raizes_nordeste_postman.json
```

3. Confirme a variável:

```text
base_url = http://127.0.0.1:8000
```

4. Execute a coleção na ordem.

A coleção armazena automaticamente tokens e IDs gerados durante os testes.

### 14.2 Cenários cobertos

| ID | Cenário | Resultado esperado |
|---|---|---|
| T01 | Login administrador válido | 200 + token ADMIN |
| T02 | Login cliente válido | 200 + token CLIENTE |
| T03 | Criar pedido aprovado | 201 + status `EM_PREPARO` |
| T04 | Listar pedidos por canal | 200 + lista filtrada |
| T05 | Consultar pedido por ID | 200 + dados do pedido |
| T06 | Criar pedido recusado | 201 + status `PAGAMENTO_RECUSADO` |
| T07 | Consultar saldo de fidelidade | 200 + saldo |
| T08 | Resgatar pontos | 200 + saldo atualizado |
| T09 | Consultar auditoria como ADMIN | 200 + logs |
| T10 | Criar unidade teste | 201 + unidade ativa |
| T11 | Soft-delete de unidade | 204 |
| T12 | Listar unidades ativas | 200 + apenas ativas |
| T13 | Login com senha inválida | 401 |
| T14 | Auditoria sem token | 401 |
| T15 | Cliente acessa auditoria | 403 |
| T16 | Resgate acima do saldo | 409 |
| T17 | Pedido com produto inexistente | 404 |

---

## 15. Validação Complementar

Também foi executada validação sintática dos módulos principais:

```bash
python -m compileall app main.py seed.py
```

Resultado: execução concluída sem erros.

Também foi validado o acesso ao OpenAPI:

```text
GET /openapi.json
```

Resultado: HTTP 200.

---

## 16. Histórico de Commits Relevantes

Commits finais de estabilização:

```text
fix: add email-validator dependency
fix: add python-multipart dependency
fix: pin bcrypt version for passlib compatibility
fix: make mock payment deterministic
fix: apply soft delete to units
test: add postman coverage for rejected payment and units
```

---

## 17. Observações de Escopo

Itens documentados como proposta/conceito para evolução:

- Atualização manual de status pela cozinha:
  - `EM_PREPARO → PRONTO → ENTREGUE / CANCELADO`
- Promoções e campanhas com desconto no pedido.

Esses itens foram documentados para atender ao escopo conceitual do estudo de caso, mas o MVP executável priorizou o fluxo pedido → pagamento mock → atualização automática de status.

---

## 18. Referências

- FastAPI Documentation: https://fastapi.tiangolo.com
- SQLAlchemy Documentation: https://docs.sqlalchemy.org
- Pydantic Documentation: https://docs.pydantic.dev
- Passlib Documentation: https://passlib.readthedocs.io
- Python JOSE Documentation: https://python-jose.readthedocs.io
- LGPD — Lei nº 13.709/2018
