from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from ingestion.ingest import clean

def test_clean_collapses_whitespace():
    assert clean(' a\n\n b   c ') == 'a b c'
