from fastapi import FastAPI, Header, HTTPException, status
from dotenv import load_dotenv
import requests
import csv
import os

load_dotenv()

app = FastAPI(title="API Consulta CEP")

API_KEY = os.getenv("API_KEY")
ARQUIVO_CSV = "ceps_salvos.csv"


@app.get("/cep/{cep}", status_code=status.HTTP_200_OK)
def buscar_cep(cep: str, x_api_key: str = Header()):
    if not API_KEY or x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Chave inválida")

    cep = cep.replace("-", "").strip()
    if len(cep) != 8 or not cep.isdigit():
        raise HTTPException(status_code=400, detail="CEP deve ter 8 dígitos")

    try:
        resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=5)
        dados = resposta.json()
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="ViaCEP indisponível")

    if dados.get("erro"):
        raise HTTPException(status_code=404, detail="CEP não encontrado")

    cep_tratado = {
        "cep": dados.get("cep", ""),
        "bairro": dados.get("bairro", ""),
        "cidade": dados.get("localidade", ""),
        "estado": dados.get("uf", "")
    }

    arquivo_existe = os.path.exists(ARQUIVO_CSV)

    with open(ARQUIVO_CSV, "a", newline="", encoding="utf-8") as arquivo:
        campos = ["cep", "bairro", "cidade", "estado"]
        writer = csv.DictWriter(arquivo, fieldnames=campos)

        if not arquivo_existe:
            writer.writeheader()

        writer.writerow(cep_tratado)

    return cep_tratado
