# TrainSight - Safra

Sistema de processamento de planilhas de treinamento (Gupy/SupplyGo) com métricas e visualizações.

## Requisitos

- Python 3.12+
- Docker (opcional, apenas para API)

## Instalação

```bash
pip install -r requirements.txt
```

## Rodar o Frontend (Streamlit)

```bash
streamlit run app.py
```

Acesse: http://localhost:8501

## Rodar a API (FastAPI)

### Localmente

```bash
uvicorn main:app --reload --port 8000
```

### Com Docker

```bash
docker-compose up
```

Acesse:
- API: http://localhost:8000
- Documentação (Swagger): http://localhost:8000/docs

## Estrutura

- `app.py` - Frontend Streamlit
- `main.py` - API FastAPI
- `metrics.py` - Cálculo de métricas
- `theme.py` - Tema visual do frontend
