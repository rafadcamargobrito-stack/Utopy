# Utopy — Plataforma Digital de Participação Cidadã e Transparência Pública

Aplicação full-stack com React + TypeScript no frontend e FastAPI + SQLAlchemy no backend.

## Funcionalidades

- Fórum comunitário com discussões e apoios;
- Laboratório de Projetos para ideias da população;
- comentários e apoios persistidos no banco;
- fluxo público de propostas: ideia → análise comunitária → análise técnica → decisão → execução → conclusão;
- justificativa pública para aprovação/rejeição;
- histórico de alterações de status;
- painel institucional com prefeito, vereadores, equipes e atividades;
- perfis de cidadão, moderador, agente público e administrador, com permissões validadas no backend;
- publicação de propostas e atividades institucionais por agentes públicos vinculados e gestão de perfis por administradores;
- obras públicas e transparência documental;
- autenticação e papéis de usuário.

## Frontend

```powershell
npm install
npm run dev
```

## Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload --port 8000
```

Abra o frontend em `http://localhost:5173` e a API em `http://localhost:8000/docs`.

## Hospedagem

- Frontend: GitHub Pages, publicado por `.github/workflows/deploy-pages.yml`.
- API: Render, configurado pelo `render.yaml`.
- Banco: PostgreSQL no Supabase. Use a URL de conexão PostgreSQL do Supabase como `DATABASE_URL` no serviço Render; credenciais ficam somente nas configurações do serviço, nunca no repositório.

Para publicar:

1. Crie um projeto PostgreSQL no Supabase e copie a URL de conexão apropriada para serviços externos.
2. No Render, crie um Blueprint a partir deste repositório. Informe a URL em `DATABASE_URL`; o Render gera `JWT_SECRET`.
3. Configure a variável de repositório `VITE_API_URL` no GitHub como `https://<servico-render>.onrender.com/api/v1`.
4. Em GitHub → Settings → Pages, selecione GitHub Actions como origem. Execute `Deploy Utopy to GitHub Pages` manualmente ou faça novo push em `main`.

O workflow do Pages não publica enquanto `VITE_API_URL` estiver ausente, para evitar um site com autenticação quebrada.

> Para produção, use PostgreSQL, HTTPS, secrets fora do repositório, rate limiting, logs/auditoria, backups e migrações versionadas.
