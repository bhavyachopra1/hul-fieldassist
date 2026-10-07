import json,sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.rag import answer

qs=json.loads(Path(__file__).with_name('questions.json').read_text())
out=[]
for q in qs:
    try:
        a,h=answer(q['question']); out.append({'id':q['id'],'question':q['question'],'answer':a,'sources':[x['metadata'] for x in h[:5]]})
    except Exception as e: out.append({'id':q['id'],'question':q['question'],'error':str(e)})
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2))
print('Wrote evaluation/results.json')
