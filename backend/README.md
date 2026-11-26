# Utopy API

Backend da **Plataforma Digital de Participação Cidadã e Transparência Pública**.

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2 + async
- PostgreSQL (produção) / SQLite (desenvolvimento)
- Alembic
- JWT
- Argon2

## Rodar localmente

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload --port 8000
```

Em desenvolvimento, o SQLite pode ser usado pelo `.env`. Para PostgreSQL, configure `DATABASE_URL` com `postgresql+asyncpg://...`.

## Fluxo de propostas

O Laboratório de Projetos registra um ciclo público:

`Ideia inicial → Em análise comunitária → Em análise técnica → Aprovada/Rejeitada → Em execução → Concluída`

Cada mudança de etapa possui histórico com autor, data e nota. Aprovação/rejeição exige justificativa pública. Cidadãos autenticados podem apoiar e comentar propostas.

## Perfis e permissões

- Cadastro público sempre cria um perfil de cidadão; o cliente não pode escolher um papel privilegiado.
- Administradores podem conceder os papéis de cidadão, moderador, agente público e administrador pela página Gestão pública.
- A atribuição de agente público exige o registro do cargo institucional e vincula a conta a um perfil público.
- Agentes públicos vinculados podem publicar propostas institucionais e registrar atividades; moderadores, agentes públicos e administradores podem analisar propostas comunitárias.
- As permissões são verificadas no backend em cada operação protegida; ocultar ações no frontend não é considerado controle de acesso.

## Endpoints principais

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET /api/v1/admin/users` (administrador)
- `PATCH /api/v1/admin/users/{id}/role` (administrador)
- `POST /api/v1/management/proposals` (agente público)
- `POST /api/v1/management/activities` (agente público)
- `GET /api/v1/public/official-proposals`
- `GET /api/v1/community/ideas`
- `GET /api/v1/community/ideas/{id}`
- `POST /api/v1/community/ideas`
- `POST /api/v1/community/ideas/{id}/support`
- `POST /api/v1/community/ideas/{id}/comments`
- `PATCH /api/v1/admin/ideas/{id}/review` (moderador/agente público/admin)

Documentação: `http://localhost:8000/docs`
