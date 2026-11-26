export type Category = 'Infraestrutura'|'Saúde'|'Educação'|'Meio ambiente';
export type Discussion = {id:number,title:string,category:Category,author:string,time:string,replies:number,supports:number,excerpt:string};
export type ProjectIdea = {id:number,title:string,area:string,author:string,description:string,supports:number,status:string};
export const discussions: Discussion[] = [
 {id:1,title:'Iluminação mais segura no entorno da escola municipal',category:'Infraestrutura',author:'Mariana S.',time:'há 2h',replies:18,supports:42,excerpt:'Os postes da rua lateral estão com iluminação insuficiente. Podemos mapear os pontos críticos e acompanhar uma solução?'},
 {id:2,title:'Atendimento psicológico para adolescentes na rede pública',category:'Saúde',author:'João V.',time:'há 5h',replies:12,supports:31,excerpt:'Uma proposta para ampliar o acolhimento e encaminhamento de adolescentes nas unidades básicas.'},
 {id:3,title:'Biblioteca comunitária e reforço no contraturno',category:'Educação',author:'Ana P.',time:'ontem',replies:26,supports:67,excerpt:'Como transformar espaços públicos pouco utilizados em pontos de leitura e apoio aos estudantes?'},
 {id:4,title:'Mais árvores e áreas de sombra nas praças',category:'Meio ambiente',author:'Carlos M.',time:'ontem',replies:9,supports:54,excerpt:'Ideias para arborização urbana, manutenção e escolha de espécies adequadas ao município.'}
];
export const projectIdeas: ProjectIdea[] = [
 {id:1,title:'Horta comunitária em terreno público ocioso',area:'Meio ambiente',author:'Beatriz R.',description:'Criar uma horta comunitária com participação de moradores, escolas e associações locais.',supports:86,status:'Em análise comunitária'},
 {id:2,title:'Aplicativo para avisar sobre pontos de descarte irregular',area:'Tecnologia',author:'Lucas F.',description:'Canal simples para registrar localização, foto e categoria de descarte para encaminhamento aos serviços municipais.',supports:71,status:'Em análise comunitária'},
 {id:3,title:'Rota segura para estudantes',area:'Mobilidade',author:'Marcos A.',description:'Mapear trajetos escolares e propor melhorias de iluminação, calçadas, sinalização e travessias.',supports:63,status:'Ideia inicial'}
];
export const works = [
 {name:'Revitalização da Praça Central',area:'Infraestrutura',progress:78,value:'R$ 420 mil',deadline:'dez/2026'},
 {name:'Ampliação da UBS Jardim Novo',area:'Saúde',progress:46,value:'R$ 1,2 mi',deadline:'mar/2027'},
 {name:'Modernização da Escola Municipal 12',area:'Educação',progress:91,value:'R$ 680 mil',deadline:'nov/2026'}
];
export const officials = [
 {name:'Prefeito(a) — Marina Almeida',role:'Poder Executivo',party:'Informação demonstrativa',projects:8,meetings:34,updated:'18 nov 2026'},
 {name:'Vereador(a) — Rafael Costa',role:'Câmara Municipal',party:'Informação demonstrativa',projects:11,meetings:27,updated:'17 nov 2026'},
 {name:'Vereador(a) — Camila Souza',role:'Câmara Municipal',party:'Informação demonstrativa',projects:7,meetings:31,updated:'16 nov 2026'},
 {name:'Secretaria de Obras — Equipe técnica',role:'Administração pública',party:'Dados institucionais',projects:15,meetings:42,updated:'18 nov 2026'}
];
