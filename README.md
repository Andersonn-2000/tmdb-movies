Estrutura do Projeto

tmdb-movies/
├── cortex/
│   └── src/
│       ├── client.py       # Cliente HTTP para a API do TMDB
│       ├── service.py      # Lógica de negócio e orquestração das requisições
│       ├── processor.py    # Processamento e normalização dos dados dos filmes
│       └── exporter.py     # Exportação dos dados para CSV via pandas
├── main.py                 # Ponto de entrada da aplicação
├── pyproject.toml          # Configuração do projeto e dependências
├── uv.lock                 # Lockfile gerado pelo UV
├── .python-version         # Versão do Python fixada (3.12)
└── .gitignore

Pré-requisitos

Python 3.12+
UV como gerenciador de pacotes e ambiente virtual
Uma chave de API válida do TMDB

Instalando o UV

Caso ainda não tenha o UV instalado, execute:

curl -LsSf https://astral.sh/uv/install.sh | sh

Instalação e Configuração
1. Clone o repositório

git clone git@github.com:Andersonn-2000/tmdb-movies.git
cd tmdb-movies

2. Instale as dependências

uv sync

Isso instalará todas as dependências listadas no pyproject.toml de forma determinística, respeitando o uv.lock, e criará um ambiente virtual

Variáveis de Ambiente

Crie um arquivo .env na raiz do projeto com a sua chave de API do TMDB:

API_KEY=sua_chave_api

Como Usar

Com o ambiente ativado e o .env configurado, execute o script principal:

uv run main.py

Arquitetura
O projeto segue uma arquitetura em camadas, com separação clara de responsabilidades:

- TMDBClient — cortex/src/client.py
Camada de comunicação com a API. Responsável por:

- Gerenciar a sessão HTTP via requests.Session
Montar e executar requisições GET autenticadas com a API_KEY
Aplicar um delay configurável entre requisições (delay=0.02s por padrão) para evitar rate limiting

- TMDBService — cortex/src/service.py
Camada de serviço e orquestração. Responsável por:

Buscar filmes populares com suporte a paginação
Obter detalhes completos de cada filme individualmente
Paralelizar as requisições de detalhes usando ThreadPoolExecutor (10 workers por padrão)

- MovieProcessor — cortex/src/processor.py
Camada de processamento. Responsável por:

Normalizar e filtrar os campos relevantes de cada filme
Retornar uma lista de dicionários com os campos: title, genres, original_language, release_date, revenue, runtime e status

- CSVExporter — cortex/src/exporter.py
Camada de exportação. Responsável por:

Criar os diretórios necessários automaticamente
Converter os dados para um DataFrame pandas
Salvar o resultado como CSV em cortex/data/raw/movies_tmdb.csv

Saída Gerada
Após a execução, o dataset será salvo em:

cortex/data/raw/movies_tmdb.csv

O CSV contém as seguintes colunas:
ColunaDescriçãotitleTítulo do filmegenresGêneros separados por vírgulaoriginal_languageIdioma originalrelease_dateData de lançamentorevenueReceita de bilheteriaruntimeDuração em minutosstatusStatus do filme (ex: Released)

Dependências
PacoteVersão mínimaUsopandas>=3.0.2Manipulação e exportação dos dadosrequests>=2.33.1Requisições HTTP para a API do TMDBpython-dotenv>=1.2.2Carregamento das variáveis de ambiente