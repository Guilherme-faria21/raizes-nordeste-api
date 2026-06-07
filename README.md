# API REST para Gestão de Pedidos — Rede Raízes do Nordeste

Projeto desenvolvido para a disciplina **Projeto Multidisciplinar — Trilha Back-End** do curso de **Tecnologia em Análise e Desenvolvimento de Sistemas**.

A aplicação implementa uma API REST para gestão de pedidos da rede fictícia **Raízes do Nordeste**, com autenticação JWT, controle de acesso por perfis, unidades, produtos, estoque, pedidos, pagamento mock determinístico, fidelidade e auditoria.

---

## 1. Visão Geral

O objetivo do projeto é demonstrar um fluxo back-end funcional, persistente e testável para uma rede de restaurantes/lanchonetes com múltiplas unidades e múltiplos canais de pedido.

Fluxo principal implementado:

```
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

```
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
- Atualização manual de status do pedido pela cozinha (`EM_PREPARO → PRONTO → ENTREGUE / CANCELADO`).
- Baixa de estoque em pedidos aprovados.
- Programa de fidelidade com consulta e resgate de pontos.
- Auditoria de ações relevantes.
- Soft-delete em unidades e produtos.
- Documentação automática via Swagger/OpenAPI.
- Coleção Postman com testes positivos e negativos.

---

## 3. Requisitos Atendidos

### 3.1 Requisitos Funcionais

| ID   | Requisito                                                                        | Status              |
| ---- | -------------------------------------------------------------------------------- | ------------------- |
| RF01 | Permitir cadastro de usuário com nome, e-mail, senha, perfil e consentimento LGPD | Implementado        |
| RF02 | Permitir login com e-mail e senha, retornando token JWT                           | Implementado        |
| RF03 | Permitir listagem e consulta de unidades ativas                                   | Implementado        |
| RF04 | Permitir cadastro, atualização e desativação de unidades                          | Implementado        |
| RF05 | Permitir listagem e consulta de produtos ativos                                   | Implementado        |
| RF06 | Permitir cadastro, atualização e desativação de produtos                          | Implementado        |
| RF07 | Permitir consulta de estoque por unidade                                          | Implementado        |
| RF08 | Permitir registro de entrada de estoque                                           | Implementado        |
| RF09 | Permitir consulta de movimentações de estoque                                     | Implementado        |
| RF10 | Permitir criação de pedido com unidade, canal, forma de pagamento e itens         | Implementado        |
| RF11 | Validar disponibilidade de estoque antes da criação do pedido                     | Implementado        |
| RF12 | Processar pagamento mock automaticamente durante a criação do pedido              | Implementado        |
| RF13 | Atualizar status do pedido conforme resultado do pagamento                        | Implementado        |
| RF14 | Baixar estoque em pedidos aprovados                                               | Implementado        |
| RF15 | Acumular pontos de fidelidade em pedidos aprovados                                | Implementado        |
| RF16 | Permitir consulta de saldo de fidelidade pelo cliente                             | Implementado        |
| RF17 | Permitir consulta de saldo de fidelidade por administradores e gerentes           | Implementado        |
| RF18 | Permitir resgate de pontos                                                        | Implementado        |
| RF19 | Registrar ações relevantes em log de auditoria                                    | Implementado        |
| RF20 | Permitir consulta dos registros de auditoria com filtros                          | Implementado        |
| RF21 | Permitir atualização manual do status do pedido pela cozinha                      | Implementado        |
| RF22 | Permitir promoções/campanhas com desconto no pedido                               | Proposta            |

### 3.2 Requisitos Não Funcionais

| ID     | Requisito                                                                                  |
| ------ | ------------------------------------------------------------------------------------------ |
| RNF01  | A API deve utilizar arquitetura modular, separando rotas, serviços e infraestrutura        |
| RNF02  | A autenticação deve ser baseada em JWT                                                     |
| RNF03  | As senhas devem ser armazenadas com hash seguro                                            |
| RNF04  | A autorização deve considerar perfis de usuário                                            |
| RNF05  | A API deve possuir documentação automática via Swagger/OpenAPI                             |
| RNF06  | As respostas de erro devem seguir padrão JSON estruturado                                  |
| RNF07  | O banco de dados deve ser acessado por ORM                                                 |
| RNF08  | O sistema deve registrar logs de auditoria para ações importantes                          |
| RNF09  | O pagamento mock deve ter comportamento determinístico para facilitar testes               |
| RNF10  | A estrutura deve ser organizada e permitir manutenção do código                            |
| RNF11  | O sistema deve permitir validação reproduzível por coleção Postman                         |
| RNF12  | O sistema deve preservar dados relevantes por soft-delete em recursos principais           |

---

## 4. Stack Tecnológica

| Tecnologia       | Função                                            |
| ---------------- | ------------------------------------------------- |
| Python           | Linguagem principal                               |
| FastAPI          | Framework web para construção da API              |
| Uvicorn          | Servidor ASGI para execução                       |
| SQLAlchemy       | ORM para mapeamento objeto-relacional             |
| SQLite           | Banco de dados utilizado no projeto               |
| Pydantic         | Validação e serialização de dados                 |
| Passlib          | Hashing de senhas                                 |
| bcrypt           | Algoritmo de hashing utilizado pelo Passlib       |
| python-jose      | Geração e validação de tokens JWT                 |
| python-dotenv    | Carregamento de variáveis de ambiente             |
| python-multipart | Suporte a login via form-data                     |
| email-validator  | Validação de campos de e-mail usados pelo Pydantic|
| Postman          | Testes da API                                     |

---

## 5. Estrutura do Projeto

```
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

```
git clone https://github.com/Guilherme-faria21/raizes-nordeste-api.git
cd raizes-nordeste-api
```

### 6.2 Criar e ativar ambiente virtual

Linux/macOS:

```
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 6.3 Instalar dependências

```
pip install --upgrade pip
pip install -r requirements.txt
```

### 6.4 Configurar variáveis de ambiente

O projeto possui o arquivo `.env.example`. Crie uma cópia chamada `.env`:

```
cp .env.example .env
```

Exemplo de variáveis esperadas:

```
SECRET_KEY=sua-chave-secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./raizes.db
```

### 6.5 Criar banco e executar seed

```
python seed.py
```

Saída esperada:

```
Seed concluido com sucesso!

Credenciais para teste:
  ADMIN   -> admin@raizes.com   / Admin@123
  GERENTE -> gerente@raizes.com / Gerente@123
  CLIENTE -> maria@email.com    / Cliente@123
  CLIENTE -> joao@email.com     / Cliente@123
```

### 6.6 Iniciar a API

```
uvicorn main:app --reload
```

API local: `http://127.0.0.1:8000`

---

## 7. Documentação Swagger/OpenAPI

Com a API rodando, acesse:

- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

---

## 8. Credenciais de Teste

| Perfil  | E-mail               | Senha         |
| ------- | -------------------- | ------------- |
| ADMIN   | `admin@raizes.com`   | `Admin@123`   |
| GERENTE | `gerente@raizes.com` | `Gerente@123` |
| CLIENTE | `maria@email.com`    | `Cliente@123` |
| CLIENTE | `joao@email.com`     | `Cliente@123` |

---

## 9. Endpoints Principais

### 9.1 Autenticação

| Método | Endpoint         | Acesso  | Descrição                       |
| ------ | ---------------- | ------- | ------------------------------- |
| POST   | `/auth/registro` | Público | Cadastra novo usuário           |
| POST   | `/auth/login`    | Público | Autentica usuário e retorna JWT |

Exemplo de login:

```
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@raizes.com&password=Admin@123"
```

### 9.2 Unidades

| Método | Endpoint                 | Acesso          | Descrição              |
| ------ | ------------------------ | --------------- | ---------------------- |
| GET    | `/unidades/`             | Público         | Lista unidades ativas  |
| GET    | `/unidades/{unidade_id}` | Público         | Consulta unidade por ID|
| POST   | `/unidades/`             | ADMIN / GERENTE | Cria nova unidade      |
| PUT    | `/unidades/{unidade_id}` | ADMIN / GERENTE | Atualiza unidade       |
| DELETE | `/unidades/{unidade_id}` | ADMIN           | Soft-delete da unidade |

### 9.3 Produtos

| Método | Endpoint                 | Acesso          | Descrição               |
| ------ | ------------------------ | --------------- | ----------------------- |
| GET    | `/produtos/`             | Público         | Lista produtos ativos   |
| GET    | `/produtos/{produto_id}` | Público         | Consulta produto por ID |
| POST   | `/produtos/`             | ADMIN / GERENTE | Cria produto            |
| PUT    | `/produtos/{produto_id}` | ADMIN / GERENTE | Atualiza produto        |
| DELETE | `/produtos/{produto_id}` | ADMIN / GERENTE | Soft-delete do produto  |

### 9.4 Estoque

| Método | Endpoint                              | Acesso          | Descrição                   |
| ------ | ------------------------------------- | --------------- | --------------------------- |
| GET    | `/estoque/{unidade_id}`               | ADMIN / GERENTE | Consulta estoque da unidade |
| POST   | `/estoque/entrada`                    | ADMIN / GERENTE | Registra entrada de estoque |
| GET    | `/estoque/{unidade_id}/movimentacoes` | ADMIN / GERENTE | Lista movimentações         |

### 9.5 Pedidos

| Método | Endpoint                      | Acesso                           | Descrição                             |
| ------ | ----------------------------- | -------------------------------- | ------------------------------------- |
| POST   | `/pedidos/`                   | CLIENTE                          | Cria pedido e processa pagamento mock |
| GET    | `/pedidos/`                   | ADMIN / GERENTE / CLIENTE        | Lista pedidos conforme perfil         |
| GET    | `/pedidos/{pedido_id}`        | ADMIN / GERENTE / dono do pedido | Consulta detalhes de um pedido        |
| PATCH  | `/pedidos/{pedido_id}/status` | ADMIN / GERENTE                  | Atualiza status do pedido (cozinha)   |

Filtro por canal: `GET /pedidos/?canal_pedido=APP`

Transições de status válidas (cozinha):

```
EM_PREPARO → PRONTO
EM_PREPARO → CANCELADO
PRONTO     → ENTREGUE
```

### 9.6 Fidelidade

| Método | Endpoint                         | Acesso          | Descrição                       |
| ------ | -------------------------------- | --------------- | ------------------------------- |
| GET    | `/fidelidade/saldo`              | CLIENTE         | Consulta saldo próprio          |
| GET    | `/fidelidade/saldo/{usuario_id}` | ADMIN / GERENTE | Consulta saldo de outro usuário |
| POST   | `/fidelidade/resgatar`           | CLIENTE         | Resgata pontos de fidelidade    |

### 9.7 Auditoria

| Método | Endpoint      | Acesso | Descrição                                    |
| ------ | ------------- | ------ | -------------------------------------------- |
| GET    | `/auditoria/` | ADMIN  | Lista registros de auditoria com filtros opcionais |

---

## 10. Fluxo Principal

### 10.1 Login do cliente

```
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=maria@email.com&password=Cliente@123"
```

Retorno:

```json
{
  "access_token": "TOKEN_JWT",
  "token_type": "bearer",
  "perfil": "CLIENTE",
  "nome": "Maria"
}
```

### 10.2 Criar pedido aprovado

```
curl -X POST http://127.0.0.1:8000/pedidos/ \
  -H "Authorization: Bearer TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "unidade_id": 1,
    "canal_pedido": "APP",
    "forma_pagamento": "PIX",
    "itens": [{"produto_id": 1, "quantidade": 1}]
  }'
```

Resposta esperada:

```json
{
  "status": "EM_PREPARO",
  "forma_pagamento": "PIX",
  "pagamento": {"status": "APROVADO", "metodo": "PIX"}
}
```

### 10.3 Criar pedido recusado

```
curl -X POST http://127.0.0.1:8000/pedidos/ \
  -H "Authorization: Bearer TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "unidade_id": 1,
    "canal_pedido": "APP",
    "forma_pagamento": "MOCK_RECUSADO",
    "itens": [{"produto_id": 1, "quantidade": 1}]
  }'
```

Resposta esperada:

```json
{
  "status": "PAGAMENTO_RECUSADO",
  "forma_pagamento": "MOCK_RECUSADO",
  "pagamento": {"status": "RECUSADO", "metodo": "MOCK_RECUSADO"}
}
```

### 10.4 Atualizar status pela cozinha

```
curl -X PATCH http://127.0.0.1:8000/pedidos/1/status \
  -H "Authorization: Bearer TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{"novo_status": "PRONTO"}'
```

Resposta esperada:

```json
{
  "pedido_id": 1,
  "status_anterior": "EM_PREPARO",
  "status_atual": "PRONTO"
}
```

---

## 11. Pagamento Mock Determinístico

O serviço de pagamento mock está em `app/application/pagamento_service.py`.

Métodos aprovados: `PIX`, `CARTAO_CREDITO`, `CARTAO_DEBITO`, `DINHEIRO`, `MOCK`

Métodos recusados: `RECUSADO`, `MOCK_RECUSADO`, `CARTAO_RECUSADO`, `CARTAO_CREDITO_RECUSADO`

O mesmo cenário sempre retorna o mesmo resultado, facilitando testes reproduzíveis.

---

## 12. Multicanalidade

O pedido possui o campo `canal_pedido`. Valores aceitos: `APP`, `TOTEM`, `BALCAO`, `PICKUP`, `WEB`.

Filtro por canal: `GET /pedidos/?canal_pedido=APP`

---

## 13. Segurança e LGPD

- Hash de senha com Passlib + bcrypt.
- Preparação de senha com SHA-256 + Base64 antes do bcrypt.
- JWT para autenticação.
- Autorização por perfil (ADMIN, GERENTE, CLIENTE).
- Consentimento LGPD no cadastro.
- Minimização de dados.
- Soft-delete em recursos principais.
- Auditoria de ações relevantes.
- Senhas nunca armazenadas em texto puro.

---

## 14. Testes com Postman

A coleção `raizes_nordeste_postman.json` está disponível no repositório. A execução final resultou em **52/52 asserções aprovadas**.

### 14.1 Como executar

1. Inicie a API: `uvicorn main:app --reload`
2. Importe `raizes_nordeste_postman.json` no Postman
3. Confirme a variável `base_url = http://127.0.0.1:8000`
4. Execute a coleção na ordem

### 14.2 Cenários cobertos

| ID  | Cenário                                            | Resultado esperado                  |
| --- | -------------------------------------------------- | ----------------------------------- |
| T01 | Login administrador válido                         | 200 + token ADMIN                   |
| T02 | Login cliente válido                               | 200 + token CLIENTE                 |
| T03 | Criar pedido aprovado                              | 201 + status `EM_PREPARO`           |
| T04 | Listar pedidos por canal                           | 200 + lista filtrada                |
| T05 | Consultar saldo de fidelidade                      | 200 + saldo                         |
| T06 | Resgatar pontos                                    | 200 + saldo atualizado              |
| T07 | Consultar auditoria como ADMIN                     | 200 + logs                          |
| T08 | Login com senha inválida                           | 401                                 |
| T09 | Auditoria sem token                                | 401                                 |
| T10 | Cliente acessa auditoria                           | 403                                 |
| T11 | Resgate acima do saldo                             | 409                                 |
| T12 | Pedido com produto inexistente                     | 404                                 |
| T13 | Consultar pedido por ID                            | 200 + dados do pedido               |
| T14 | Criar pedido recusado                              | 201 + status `PAGAMENTO_RECUSADO`   |
| T15 | Criar unidade teste                                | 201 + unidade ativa                 |
| T16 | Soft-delete de unidade                             | 204                                 |
| T17 | Listar unidades ativas                             | 200 + apenas ativas                 |
| T18 | Atualizar status do pedido: EM_PREPARO → PRONTO    | 200 + status_atual `PRONTO`         |
| T19 | Transição de status inválida (PRONTO → EM_PREPARO) | 422 + error `TRANSICAO_INVALIDA`    |

---

## 15. Validação Complementar

Validação sintática executada com:

```
python -m compileall app main.py seed.py
```

Resultado: execução concluída sem erros. OpenAPI JSON validado com retorno HTTP 200.

---

## 16. Observações de Escopo

Item documentado como proposta para evolução futura:

- Promoções e campanhas com desconto no pedido.

---

## 17. Referências

- BRASIL. **Lei n. 13.709, de 14 de agosto de 2018.** Lei Geral de Proteção de Dados Pessoais (LGPD). Brasília, DF: Presidência da República, 2018.
- FASTAPI. **FastAPI Documentation.** Disponível em: https://fastapi.tiangolo.com
- FIELDING, Roy Thomas. **Architectural Styles and the Design of Network-based Software Architectures.** University of California, Irvine, 2000.
- FOWLER, Martin. **Patterns of Enterprise Application Architecture.** Boston: Addison-Wesley, 2002.
- PASSLIB. **Passlib Documentation.** Disponível em: https://passlib.readthedocs.io
- PYDANTIC. **Pydantic Documentation.** Disponível em: https://docs.pydantic.dev
- PYTHON-JOSE. **Python-JOSE Documentation.** Disponível em: https://python-jose.readthedocs.io
- RICHARDSON, Leonard; RUBY, Sam. **RESTful Web Services.** Sebastopol: O'Reilly Media, 2007.
- SQLALCHEMY. **SQLAlchemy Documentation.** Disponível em: https://docs.sqlalchemy.org
