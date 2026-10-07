from __future__ import annotations
import argparse, hashlib, re
from pathlib import Path
import yaml, requests
from pypdf import PdfReader
from dotenv import load_dotenv
import os

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env')


def clean(text: str) -> str:
    text = re.sub(r'\s+', ' ', text or '').strip()
    return text


def download_sources(force=False):
    sources = yaml.safe_load((ROOT/'data/sources.yaml').read_text())['sources']
    raw = ROOT/'data/raw'; raw.mkdir(parents=True, exist_ok=True)
    for s in sources:
        path = raw/f"{s['id']}.pdf"
        if path.exists() and not force:
            continue
        r = requests.get(s['url'], timeout=60, headers={'User-Agent':'HUL-FieldAssist/1.0'})
        r.raise_for_status(); path.write_bytes(r.content)
        print(f"Downloaded {s['id']} ({len(r.content)/1e6:.1f} MB)")


def chunk_pages(pdf_path: Path, source: dict, chunk_words=260, overlap=50):
    reader = PdfReader(str(pdf_path)); rows=[]
    for pno, page in enumerate(reader.pages, start=1):
        text = clean(page.extract_text() or '')
        if not text: continue
        words = text.split()
        start = 0
        while start < len(words):
            end = min(start + chunk_words, len(words))
            chunk = ' '.join(words[start:end])
            if len(chunk) >= 80:
                key = f"{source['id']}:{pno}:{start}"
                rows.append({
                    'id': hashlib.sha1(key.encode()).hexdigest(),
                    'text': chunk,
                    'metadata': {
                        'source_id': source['id'], 'title': source['title'],
                        'year': source['year'], 'type': source['type'],
                        'page': pno, 'url': source['url']
                    }
                })
            if end == len(words): break
            start = end - overlap
    return rows


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--skip-download', action='store_true')
    ap.add_argument('--force-download', action='store_true')
    args=ap.parse_args()
    if not args.skip_download: download_sources(args.force_download)
    sources=yaml.safe_load((ROOT/'data/sources.yaml').read_text())['sources']
    docs=[]
    for s in sources:
        p=ROOT/'data/raw'/f"{s['id']}.pdf"
        if not p.exists():
            print(f"Missing {p}; run without --skip-download")
            continue
        docs.extend(chunk_pages(p,s))
    if not docs: raise SystemExit('No PDFs found.')
    import chromadb
    from openai import OpenAI
    client=OpenAI()
    texts=[d['text'] for d in docs]
    batch=100; embeddings=[]
    for i in range(0,len(texts),batch):
        res=client.embeddings.create(model=os.getenv('OPENAI_EMBED_MODEL','text-embedding-3-small'), input=texts[i:i+batch])
        embeddings.extend([x.embedding for x in res.data])
        print(f"Embedded {min(i+batch,len(texts))}/{len(texts)}")
    chroma=chromadb.PersistentClient(path=str(ROOT/os.getenv('CHROMA_PATH','.chroma')))
    name=os.getenv('COLLECTION_NAME','hul_fieldassist')
    try: chroma.delete_collection(name)
    except Exception: pass
    col=chroma.create_collection(name=name, metadata={'hnsw:space':'cosine'})
    for i in range(0,len(docs),batch):
        part=docs[i:i+batch]
        col.add(ids=[d['id'] for d in part], documents=[d['text'] for d in part], metadatas=[d['metadata'] for d in part], embeddings=embeddings[i:i+batch])
    (ROOT/'data/processed').mkdir(exist_ok=True)
    (ROOT/'data/processed/index_stats.txt').write_text(f"chunks={len(docs)}\ndocuments={len(set(d['metadata']['source_id'] for d in docs))}\n")
    print(f'Indexed {len(docs)} chunks from {len(sources)} sources.')

if __name__=='__main__': main()
