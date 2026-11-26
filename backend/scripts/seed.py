import asyncio
from sqlalchemy import select
from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.models import User, Official, Activity, Work, TransparencyDocument, Discussion, ProjectIdea, ProjectIdeaStatusHistory
from app.models.user import UserRole
from app.core.security import hash_password
from datetime import datetime, timezone

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with SessionLocal() as db:
        demo=await db.scalar(select(User).where(User.email.in_(['demo@utopy.example.com','demo@utopy.local'])))
        if demo:
            demo.email='demo@utopy.example.com'
        else:
            db.add(User(name='Usuário Demo',email='demo@utopy.example.com',password_hash=hash_password('Demo@123456'),role=UserRole.citizen))
        admin=await db.scalar(select(User).where(User.email.in_(['admin@utopy.example.com','admin@utopy.local'])))
        if admin:
            admin.email='admin@utopy.example.com'
        else:
            db.add(User(name='Administrador Utopy',email='admin@utopy.example.com',password_hash=hash_password('Admin@123456'),role=UserRole.admin))
        if not (await db.execute(select(Official))).first():
            db.add_all([
                Official(name='Prefeito(a) — Marina Almeida',role='Poder Executivo',party='Informação demonstrativa',projects=8,activities=34),
                Official(name='Vereador(a) — Rafael Costa',role='Câmara Municipal',party='Informação demonstrativa',projects=11,activities=27),
                Official(name='Vereador(a) — Camila Souza',role='Câmara Municipal',party='Informação demonstrativa',projects=7,activities=31),
                Official(name='Secretaria de Obras — Equipe técnica',role='Administração pública',party='Dados institucionais',projects=15,activities=42),
            ])
        if not (await db.execute(select(Work))).first():
            db.add_all([Work(name='Revitalização da Praça Central',area='Infraestrutura',progress=78,value=420000,deadline='dez/2026'),Work(name='Ampliação da UBS Jardim Novo',area='Saúde',progress=46,value=1200000,deadline='mar/2027'),Work(name='Modernização da Escola Municipal 12',area='Educação',progress=91,value=680000,deadline='nov/2026')])
        if not (await db.execute(select(Activity))).first():
            db.add_all([Activity(title='Proposta de revitalização de praça',description='Registrada no painel de propostas · status: em análise.'),Activity(title='Reunião da comissão de infraestrutura',description='Agenda e ata devem ser disponibilizadas nesta área.'),Activity(title='Consulta pública aberta',description='Período de contribuição da população em andamento.')])
        if not (await db.execute(select(TransparencyDocument))).first():
            db.add_all([TransparencyDocument(title='Relatório resumido da execução orçamentária',file_url='https://example.com/documento.pdf',year=2026,source='Portal oficial demonstrativo'),TransparencyDocument(title='Relatório de gestão fiscal',file_url='https://example.com/documento.pdf',year=2026,source='Portal oficial demonstrativo'),TransparencyDocument(title='Plano plurianual — resumo público',file_url='https://example.com/documento.pdf',year=2026,source='Portal oficial demonstrativo'),TransparencyDocument(title='Relatório de obras e contratos',file_url='https://example.com/documento.pdf',year=2026,source='Portal oficial demonstrativo')])
        if not (await db.execute(select(Discussion))).first():
            u=await db.scalar(select(User).where(User.email=='demo@utopy.example.com'))
            db.add_all([Discussion(title='Iluminação mais segura no entorno da escola municipal',category='Infraestrutura',author_id=u.id,excerpt='Os postes da rua lateral estão com iluminação insuficiente. Podemos mapear os pontos críticos e acompanhar uma solução?'),Discussion(title='Atendimento psicológico para adolescentes na rede pública',category='Saúde',author_id=u.id,excerpt='Uma proposta para ampliar o acolhimento e encaminhamento de adolescentes nas unidades básicas.'),Discussion(title='Biblioteca comunitária e reforço no contraturno',category='Educação',author_id=u.id,excerpt='Como transformar espaços públicos pouco utilizados em pontos de leitura e apoio aos estudantes?'),Discussion(title='Mais árvores e áreas de sombra nas praças',category='Meio ambiente',author_id=u.id,excerpt='Ideias para arborização urbana, manutenção e escolha de espécies adequadas ao município.')])
        if not (await db.execute(select(ProjectIdea))).first():
            u=await db.scalar(select(User).where(User.email=='demo@utopy.example.com'))
            db.add_all([ProjectIdea(title='Horta comunitária em terreno público ocioso',area='Meio ambiente',author_id=u.id,description='Criar uma horta comunitária com participação de moradores, escolas e associações locais.',status='Em análise comunitária'),ProjectIdea(title='Aplicativo para avisar sobre pontos de descarte irregular',area='Tecnologia',author_id=u.id,description='Canal simples para registrar localização, foto e categoria de descarte para encaminhamento aos serviços municipais.',status='Em análise comunitária'),ProjectIdea(title='Rota segura para estudantes',area='Mobilidade',author_id=u.id,description='Mapear trajetos escolares e propor melhorias de iluminação, calçadas, sinalização e travessias.',status='Ideia inicial')])
            await db.flush()
            ideas_seed=(await db.execute(select(ProjectIdea).order_by(ProjectIdea.id.desc()).limit(3))).scalars().all()
            for seeded in ideas_seed:
                db.add(ProjectIdeaStatusHistory(project_idea_id=seeded.id, actor_id=u.id, from_status=None, to_status=seeded.status, note='Registro inicial demonstrativo.'))
        await db.commit()
    print('Seed concluído. Demo: demo@utopy.example.com / Demo@123456 | Admin: admin@utopy.example.com / Admin@123456')
asyncio.run(main())
