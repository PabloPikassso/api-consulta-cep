from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
import requests
import csv
import os


app = FastAPI(title="API Consulta CEP")

# Na Vercel o disco é somente leitura, exceto /tmp
ARQUIVO_CSV = "/tmp/ceps_salvos.csv" if os.getenv("VERCEL") else "ceps_salvos.csv"


@app.get("/", include_in_schema=False)
def raiz():
    return RedirectResponse("/docs")


@app.get("/cep/{cep}", status_code=status.HTTP_200_OK)
def buscar_cep(cep: str):
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

    try:
        arquivo_existe = os.path.exists(ARQUIVO_CSV)

        with open(ARQUIVO_CSV, "a", newline="", encoding="utf-8") as arquivo:
            campos = ["cep", "bairro", "cidade", "estado"]
            writer = csv.DictWriter(arquivo, fieldnames=campos)

            if not arquivo_existe:
                writer.writeheader()

            writer.writerow(cep_tratado)
    except OSError:
        pass  # salvar o CSV é opcional; não derruba a consulta

    return cep_tratado
