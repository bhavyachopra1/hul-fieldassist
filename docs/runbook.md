# Runbook

## 1. Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## 2. Configure
Add `OPENAI_API_KEY` to `.env`. Keep `.env` out of Git.

## 3. Download + index
```bash
python ingestion/ingest.py
```
This downloads the official HUL PDFs listed in `data/sources.yaml`, extracts page text, chunks it, embeds it and stores vectors in Chroma.

## 4. Start backend
```bash
uvicorn api.main:app --reload --port 8000
```

## 5. Start frontend
In a second terminal:
```bash
streamlit run app/main.py
```

## 6. Evaluate
```bash
python evaluation/run_eval.py
```

## 7. Test API
```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/ask -H 'Content-Type: application/json' -d '{"question":"What are HUL’s Home Care brands?"}'
```
