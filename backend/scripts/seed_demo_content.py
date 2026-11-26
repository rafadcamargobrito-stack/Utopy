import asyncio
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select

from app.core.security import hash_password
from app.db.session import SessionLocal, engine
from app.models import (
    Activity,
    Discussion,
    DiscussionReply,
    Official,
    OfficialProposal,
    ProjectIdea,
    ProjectIdeaComment,
    ProjectIdeaStatusHistory,
    TransparencyDocument,
    User,
    Work,
)
from app.models.user import UserRole

DEMO_AUTHOR_EMAIL = "demo-content@utopy.example.invalid"
DEMO_AUTHOR_NAME = "Pessoa demonstrativa"
DEMO_DOCUMENTS_BASE_URL = "https://rafadcamargobrito-stack.github.io/Utopy/demonstrativos"

OFFICIALS = [
    {
        "name": "Prefeita fictícia — Marina Almeida",
        "role": "Poder Executivo (fictício)",
        "party": "Protótipo acadêmico · sem vínculo real",
    },
    {
        "name": "Vereador fictício — Rafael Costa",
        "role": "Câmara Municipal (fictícia)",
        "party": "Protótipo acadêmico · sem vínculo real",
    },
    {
        "name": "Secretaria fictícia de Obras — Equipe técnica",
        "role": "Administração pública (simulada)",
        "party": "Dados institucionais demonstrativos",
    },
]

DISCUSSIONS = [
    {
        "title": "Travessias mais seguras perto das escolas",
        "category": "Infraestrutura",
        "excerpt": "Discussão fictícia sobre faixas de pedestres, sinalização e acessibilidade nos trajetos escolares.",
        "replies": [
            "Sugestão demonstrativa: mapear os pontos de travessia em uma caminhada comunitária.",
            "Como exemplo, poderíamos avaliar iluminação e rampas nas esquinas próximas.",
        ],
    },
    {
        "title": "Horário ampliado de atendimento nas unidades de saúde",
        "category": "Saúde",
        "excerpt": "Tópico demonstrativo para conversar sobre horários, acolhimento e acesso às unidades básicas.",
        "replies": [
            "Ideia fictícia: consultar moradores sobre os horários de maior demanda.",
            "O protótipo poderia acompanhar uma proposta-piloto e seus indicadores.",
        ],
    },
    {
        "title": "Biblioteca comunitária aberta aos sábados",
        "category": "Educação",
        "excerpt": "Discussão acadêmica sobre leitura, atividades culturais e espaços comunitários nos fins de semana.",
        "replies": [
            "Uma parceria demonstrativa com voluntários poderia testar oficinas de leitura.",
            "Também seria interessante consultar estudantes e famílias do bairro.",
        ],
    },
    {
        "title": "Mais árvores e sombra nas praças do bairro",
        "category": "Meio ambiente",
        "excerpt": "Tópico fictício para planejar arborização, espécies adequadas e manutenção de áreas públicas.",
        "replies": [
            "Como exercício, moradores poderiam indicar locais com pouca sombra.",
            "O plano demonstrativo deve prever manutenção e espécies apropriadas.",
        ],
    },
]

IDEAS = [
    {
        "title": "Horta comunitária no Jardim das Flores",
        "area": "Meio ambiente",
        "description": "Proposta fictícia para transformar um espaço ocioso em horta comunitária com participação de moradores e escolas.",
        "status": "Ideia inicial",
        "technical_note": None,
        "decision_reason": None,
        "responsible_department": None,
        "estimated_cost": None,
        "history": [
            (None, "Ideia inicial", "Registro inicial fictício do protótipo acadêmico."),
        ],
        "comments": [
            "Comentário demonstrativo: uma oficina de compostagem poderia complementar a proposta.",
        ],
    },
    {
        "title": "Rota escolar segura no Bairro Horizonte",
        "area": "Mobilidade",
        "description": "Exemplo acadêmico de rota com calçadas acessíveis, travessias sinalizadas e melhor iluminação.",
        "status": "Em análise comunitária",
        "technical_note": None,
        "decision_reason": None,
        "responsible_department": None,
        "estimated_cost": None,
        "history": [
            (None, "Ideia inicial", "Proposta fictícia criada para demonstração."),
            ("Ideia inicial", "Em análise comunitária", "Etapa demonstrativa de escuta da comunidade."),
        ],
        "comments": [
            "Sugestão fictícia: incluir estudantes com deficiência na avaliação do trajeto.",
        ],
    },
    {
        "title": "Biblioteca aberta e oficinas aos fins de semana",
        "area": "Educação",
        "description": "Projeto simulado para oferecer leitura, reforço escolar e atividades culturais em espaço comunitário.",
        "status": "Em análise técnica",
        "technical_note": "Análise técnica demonstrativa; não corresponde a avaliação de órgão público.",
        "decision_reason": None,
        "responsible_department": "Equipe acadêmica fictícia",
        "estimated_cost": 28500,
        "history": [
            (None, "Ideia inicial", "Registro fictício para demonstrar o histórico da proposta."),
            ("Ideia inicial", "Em análise comunitária", "Consulta simulada à comunidade."),
            ("Em análise comunitária", "Em análise técnica", "Etapa técnica fictícia do protótipo."),
        ],
        "comments": [
            "Comentário demonstrativo: prever materiais acessíveis e atividades para diferentes faixas etárias.",
        ],
    },
    {
        "title": "Pontos de coleta seletiva em áreas de convivência",
        "area": "Meio ambiente",
        "description": "Ideia fictícia para testar pontos de coleta, comunicação visual e acompanhamento da destinação de recicláveis.",
        "status": "Em execução",
        "technical_note": "Registro inteiramente demonstrativo, sem execução real.",
        "decision_reason": "Aprovação fictícia usada apenas para apresentar o fluxo do protótipo.",
        "responsible_department": "Equipe acadêmica fictícia",
        "estimated_cost": 12400,
        "history": [
            (None, "Ideia inicial", "Registro fictício criado para demonstração."),
            ("Ideia inicial", "Em análise comunitária", "Consulta simulada."),
            ("Em análise comunitária", "Em análise técnica", "Avaliação técnica fictícia."),
            ("Em análise técnica", "Aprovada", "Decisão simulada para fins acadêmicos."),
            ("Aprovada", "Em execução", "Etapa de execução fictícia; nenhuma obra foi iniciada."),
        ],
        "comments": [
            "Comentário demonstrativo: a sinalização deve explicar quais materiais podem ser descartados.",
        ],
    },
]

WORKS = [
    {
        "name": "Demonstração: revitalização da Praça das Acácias",
        "area": "Infraestrutura",
        "progress": 35,
        "value": 420000,
        "deadline": "dez/2026",
    },
    {
        "name": "Demonstração: melhorias na UBS Jardim das Flores",
        "area": "Saúde",
        "progress": 60,
        "value": 780000,
        "deadline": "mar/2027",
    },
    {
        "name": "Demonstração: acessibilidade na Escola Horizonte",
        "area": "Educação",
        "progress": 82,
        "value": 265000,
        "deadline": "nov/2026",
    },
    {
        "name": "Demonstração: parque linear do Córrego Azul",
        "area": "Meio ambiente",
        "progress": 12,
        "value": 950000,
        "deadline": "jun/2027",
    },
]

DOCUMENTS = [
    {
        "title": "Orçamento fictício — receita, despesas e investimentos",
        "file_name": "orcamento-ficticio-2026.csv",
        "year": 2026,
    },
    {
        "title": "Plano fictício de obras e prazos",
        "file_name": "plano-obras-ficticio-2026.csv",
        "year": 2026,
    },
    {
        "title": "Metas públicas fictícias do protótipo",
        "file_name": "metas-publicas-ficticias-2026.csv",
        "year": 2026,
    },
]

OFFICIAL_PROPOSALS = [
    {
        "official_name": OFFICIALS[0]["name"],
        "title": "Demonstração: melhorar a iluminação no entorno escolar",
        "area": "Infraestrutura",
        "description": "Proposta institucional fictícia para demonstrar cadastro, autoria e acompanhamento público.",
    },
    {
        "official_name": OFFICIALS[1]["name"],
        "title": "Demonstração: oficinas de leitura comunitária",
        "area": "Educação",
        "description": "Exemplo acadêmico de proposta; não representa compromisso de agente público real.",
    },
    {
        "official_name": OFFICIALS[2]["name"],
        "title": "Demonstração: manutenção participativa das praças",
        "area": "Meio ambiente",
        "description": "Registro inteiramente fictício para ilustrar a área de gestão pública do protótipo.",
    },
]

ACTIVITIES = [
    {
        "official_name": OFFICIALS[0]["name"],
        "title": "Demonstração: reunião pública de bairro",
        "description": "Atividade fictícia do protótipo acadêmico; não houve reunião real.",
    },
    {
        "official_name": OFFICIALS[0]["name"],
        "title": "Demonstração: consulta sobre travessias escolares",
        "description": "Registro simulado para apresentar uma consulta pública e seu acompanhamento.",
    },
    {
        "official_name": OFFICIALS[1]["name"],
        "title": "Demonstração: agenda da comissão de educação",
        "description": "Atividade fictícia, sem vínculo com uma comissão ou autoridade real.",
    },
    {
        "official_name": OFFICIALS[2]["name"],
        "title": "Demonstração: visita técnica à praça",
        "description": "Registro acadêmico simulado; nenhuma visita técnica foi realizada.",
    },
]


async def seed_demo_content() -> None:
    async with SessionLocal() as db:
        async with db.begin():
            author = await db.scalar(select(User).where(User.email == DEMO_AUTHOR_EMAIL))
            if author is None:
                author = User(
                    name=DEMO_AUTHOR_NAME,
                    email=DEMO_AUTHOR_EMAIL,
                    password_hash=hash_password(secrets.token_urlsafe(48)),
                    role=UserRole.citizen,
                )
                db.add(author)
                await db.flush()

            officials_by_name = {
                official.name: official
                for official in (await db.scalars(select(Official))).all()
            }
            for data in OFFICIALS:
                if data["name"] not in officials_by_name:
                    official = Official(**data)
                    db.add(official)
                    officials_by_name[data["name"]] = official
            await db.flush()

            existing_work_names = set((await db.scalars(select(Work.name))).all())
            for data in WORKS:
                if data["name"] not in existing_work_names:
                    db.add(Work(**data))

            existing_document_titles = set(
                (await db.scalars(select(TransparencyDocument.title))).all()
            )
            for data in DOCUMENTS:
                if data["title"] not in existing_document_titles:
                    db.add(
                        TransparencyDocument(
                            title=data["title"],
                            file_url=f'{DEMO_DOCUMENTS_BASE_URL}/{data["file_name"]}',
                            year=data["year"],
                            source="Dados fictícios — protótipo acadêmico",
                        )
                    )

            discussions_by_title = {
                discussion.title: discussion
                for discussion in (await db.scalars(select(Discussion))).all()
            }
            for data in DISCUSSIONS:
                if data["title"] not in discussions_by_title:
                    discussion = Discussion(
                        title=data["title"],
                        category=data["category"],
                        excerpt=data["excerpt"],
                        author_id=author.id,
                    )
                    db.add(discussion)
                    discussions_by_title[data["title"]] = discussion
            await db.flush()

            for data in DISCUSSIONS:
                discussion = discussions_by_title[data["title"]]
                existing_replies = set(
                    (
                        await db.scalars(
                            select(DiscussionReply.body).where(
                                DiscussionReply.discussion_id == discussion.id
                            )
                        )
                    ).all()
                )
                for body in data["replies"]:
                    if body not in existing_replies:
                        db.add(
                            DiscussionReply(
                                discussion_id=discussion.id,
                                author_id=author.id,
                                body=body,
                            )
                        )

            ideas_by_title = {
                idea.title: idea
                for idea in (await db.scalars(select(ProjectIdea))).all()
            }
            for data in IDEAS:
                if data["title"] in ideas_by_title:
                    continue
                idea = ProjectIdea(
                    title=data["title"],
                    area=data["area"],
                    description=data["description"],
                    author_id=author.id,
                    status=data["status"],
                    technical_note=data["technical_note"],
                    decision_reason=data["decision_reason"],
                    responsible_department=data["responsible_department"],
                    estimated_cost=data["estimated_cost"],
                )
                db.add(idea)
                ideas_by_title[data["title"]] = idea
                await db.flush()

                history_length = len(data["history"])
                for index, (from_status, to_status, note) in enumerate(data["history"]):
                    db.add(
                        ProjectIdeaStatusHistory(
                            project_idea_id=idea.id,
                            actor_id=author.id,
                            from_status=from_status,
                            to_status=to_status,
                            note=note,
                            created_at=datetime.now(timezone.utc)
                            - timedelta(days=history_length - index),
                        )
                    )
                for body in data["comments"]:
                    db.add(
                        ProjectIdeaComment(
                            project_idea_id=idea.id,
                            author_id=author.id,
                            body=body,
                        )
                    )

            existing_proposal_titles = set(
                (await db.scalars(select(OfficialProposal.title))).all()
            )
            for data in OFFICIAL_PROPOSALS:
                if data["title"] in existing_proposal_titles:
                    continue
                official = officials_by_name[data["official_name"]]
                db.add(
                    OfficialProposal(
                        official_id=official.id,
                        title=data["title"],
                        area=data["area"],
                        description=data["description"],
                        status="Apresentada (fictícia)",
                    )
                )

            existing_activity_titles = set(
                (await db.scalars(select(Activity.title))).all()
            )
            for data in ACTIVITIES:
                if data["title"] in existing_activity_titles:
                    continue
                official = officials_by_name[data["official_name"]]
                db.add(
                    Activity(
                        official_id=official.id,
                        title=data["title"],
                        description=data["description"],
                    )
                )

            for data in OFFICIALS:
                official = officials_by_name[data["name"]]
                proposal_count = await db.scalar(
                    select(func.count())
                    .select_from(OfficialProposal)
                    .where(OfficialProposal.official_id == official.id)
                )
                activity_count = await db.scalar(
                    select(func.count())
                    .select_from(Activity)
                    .where(Activity.official_id == official.id)
                )
                official.projects = max(official.projects, int(proposal_count or 0))
                official.activities = max(official.activities, int(activity_count or 0))

    await engine.dispose()


async def main() -> None:
    await seed_demo_content()
    print("Conteúdo demonstrativo fictício verificado e publicado no banco.")


if __name__ == "__main__":
    asyncio.run(main())
