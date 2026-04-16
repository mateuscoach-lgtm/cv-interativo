from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CV_DATA = {
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
        {"nome": "Atuação em clientes PF, PJ e alta renda", "relacionados": ["original"]},
        {"nome": "LL de R$ 58 mil → R$ 70 mil", "relacionados": ["bradesco_pf"]},
        {"nome": "Redução de base com aumento de rentabilidade", "relacionados": ["bradesco_pf"]},
        {"nome": "Gestão de equipe de até 12 pessoas", "relacionados": ["bradesco_pj"]},
        {"nome": "Atuação como gerente geral substituto", "relacionados": ["bradesco_pj"]}
    ]
}

# tracking simples
def salvar_tracking(dado):
    arquivo = "tracking.json"

    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            dados = json.load(f)
    else:
        dados = []

    dados.append(dado)

    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)

@app.get("/cv")
async def get_cv(request: Request, id: str = "anonimo"):
    salvar_tracking({
        "tipo": "visita",
        "empresa": id,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": request.client.host
    })
    return CV_DATA

@app.post("/track-click")
async def track_click(data: dict):
    salvar_tracking({
        "tipo": "click",
        "empresa": data.get("empresa", "anonimo"),
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return {"ok": True}

@app.get("/tracking")
async def tracking():
    if os.path.exists("tracking.json"):
        with open("tracking.json", "r") as f:
            return json.load(f)
    return []