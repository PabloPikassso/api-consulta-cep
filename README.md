# API Consulta CEP

API REST em **Python + FastAPI** que consulta endereços pela API pública [ViaCEP](https://viacep.com.br), trata os dados recebidos e salva cada consulta em um arquivo CSV.

## Funcionalidades

- Consumo da API pública ViaCEP
- Tratamento dos dados (CEP, bairro, cidade, estado)
- Autenticação simples por API Key (header `x-api-key`)
- Validação do CEP e tratamento de CEP inexistente
- Armazenamento das consultas em `ceps_salvos.csv`
- Documentação automática com Swagger

## Tecnologias

Python · FastAPI · Uvicorn · Requests · python-dotenv · CSV

## Como executar

```bash
pip install -r requirements.txt
cp .env.example .env    # defina sua chave em API_KEY
uvicorn main:app --reload
```

Abra a documentação em `http://127.0.0.1:8000/docs`.

## Uso

`GET /cep/{cep}` com o header `x-api-key: <sua chave>`

```bash
curl -H "x-api-key: sua-chave" http://127.0.0.1:8000/cep/85807585
```

```json
{
  "cep": "85807-585",
  "bairro": "Coqueiral",
  "cidade": "Cascavel",
  "estado": "PR"
}
```

## Códigos HTTP

| Código | Significado |
|---|---|
| 200 | Consulta realizada com sucesso |
| 400 | CEP com formato inválido |
| 403 | Chave da API inválida |
| 404 | CEP não encontrado |
| 502 | ViaCEP indisponível |
