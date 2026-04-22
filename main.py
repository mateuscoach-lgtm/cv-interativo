from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Configuração de CORS para permitir acesso do seu site no Netlify
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite qualquer origem, incluindo seu site no Netlify
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

class Experiencia(BaseModel):
    id: str
    empresa: str
    periodo: str
    skills: List[str]

class Resultado(BaseModel):
    nome: str
    relacionados: List[str]

class CV(BaseModel):
    nome: str
    titulo: str
    experiencias: List[Experiencia]
    resultados: List[Resultado]

# Dados do Currículo
cv_data = {
    "nome": "Mateus Renato",
    "titulo": "Gestão | Dados | Performance e Resultados",
    "experiencias": [
        {
            "id": "house",
            "empresa": "House One Burgers e Espetos",
            "periodo": "2023 - 2026",
            "skills": ["Gestão", "KPI", "Excel", "Processos", "Estratégia"]
        },
        {
            "id": "original",
            "empresa": "Banco Original",
            "periodo": "2019 - 2023",
            "skills": ["Gestão", "Excel", "Análise de Dados", "Vendas", "KPI"]
        },
        {
            "id": "bradesco_pf",
            "empresa": "Bradesco PF",
            "periodo": "2010 - 2014",
            "skills": ["Gestão", "Relacionamento", "Performance"]
        },
        {
            "id": "bradesco_pj",
            "empresa": "Bradesco PJ",
            "periodo": "2014 - 2018",
            "skills": ["Gestão", "Financeiro", "Liderança"]
        }
    ],
    "resultados": [
        {"nome": "Faturamento médio de R$ 70 mil/mês", "relacionados": ["house"]},
        {"nome": "Aumento da margem via otimização de cardápio", "relacionados": ["house"]},
        {"nome": "Expansão de carteira de 0 → +2000 clientes", "relacionados": ["original"]},
        {"nome": "Atuação com clientes PF, PJ e alta renda", "relacionados": ["original"]},
        {"nome": "LL de R$ 58 mil → R$ 70 mil", "relacionados": ["bradesco_pf"]},
        {"nome": "Redução de base com aumento de rentabilidade", "relacionados": ["bradesco_pf"]},
        {"nome": "Gestão de equipe de até 12 pessoas", "relacionados": ["bradesco_pj"]},
        {"nome": "Atuação como gerente geral substituto", "relacionados": ["bradesco_pj"]}
    ]
}

@app.get("/")
def home():
    return {"status": "API Online", "endpoint": "/cv"}

@app.get("/cv", response_model=CV)
def get_cv():
    return cv_data

@app.post("/cv/track-click")
def track_click(data: dict):
    print(f"Clique registrado: {data}")
    return {"status": "ok"}
