import streamlit as st
import os
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.rag import answer
st.set_page_config(page_title='HUL FieldAssist', page_icon='🧭', layout='wide')
st.markdown('''<style> .block-container{padding-top:2rem;max-width:1100px} .source{padding:.65rem;border:1px solid #ddd;border-radius:10px;margin:.35rem 0;font-size:.9rem} </style>''', unsafe_allow_html=True)

st.title('🧭 HUL FieldAssist')
st.caption('AI sales knowledge copilot • grounded in public HUL documents')

with st.sidebar:
    st.header('Field tools')
    st.write('**Ask HUL** — retrieve product, category, business and policy knowledge.')
    st.write('**Evidence-first** — answers are constrained to retrieved documents.')
    st.write('**Demo scope** — public HUL PDFs only; no confidential schemes or distributor margins.')
    st.divider(); st.markdown('**Try:**')
    examples=['Which Home Care brands target value-seeking consumers?','What is Surf Excel Smart Shots?','What are HUL’s FY2025-26 business segments?','What changed in Minimalist?','What is HUL’s latest reported turnover?']
    for e in examples:
        if st.button(e, use_container_width=True): st.session_state['question']=e

q=st.chat_input('Ask about HUL products, categories, strategy or public policies…') or st.session_state.pop('question',None)
if 'messages' not in st.session_state: st.session_state.messages=[]
for m in st.session_state.messages:
    with st.chat_message(m['role']): st.markdown(m['content'])

if q:
    st.session_state.messages.append({'role':'user','content':q})
    with st.chat_message('user'): st.markdown(q)
    with st.chat_message('assistant'):
        with st.spinner('Searching HUL documents...'):
            try:
                text, hits = answer(q, k=8)
            except Exception as e:
                text = f'Unable to answer right now.\n\n{e}'
                hits = []
                
        st.markdown(text)
        if hits:
            st.markdown('#### Sources')
            for h in hits[:5]:
                m=h['metadata']; st.markdown(f"<div class='source'><b>{h['sid']}</b> · {m['title']} · p.{m['page']} · <a href='{m['url']}' target='_blank'>official source</a></div>",unsafe_allow_html=True)
    st.session_state.messages.append({'role':'assistant','content':text})
