from pathlib import Path
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.rag import answer

app=FastAPI(title='HUL FieldAssist API', version='1.0.0')
class AskRequest(BaseModel):
    question:str
    top_k:int=8

@app.get('/health')
def health(): return {'status':'ok','service':'hul-fieldassist'}

@app.post('/ask')
def ask(req:AskRequest):
    try:
        text,hits=answer(req.question, req.top_k)
        return {'answer':text,'sources':[{'id':h['sid'],**h['metadata']} for h in hits]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
