import streamlit as st
from query_cloud import answer

st.set_page_config(page_title="DocMind by Shlok", page_icon="🧠")
st.title("🧠 DocMind")
st.caption("by Shlok — Chat with your documents, powered by AI")

if "history" not in st.session_state:
    st.session_state.history = []

q = st.chat_input("Ask something about your docs...")
if q:
    with st.spinner("Thinking..."):
        resp, _ = answer(q)
    st.session_state.history.append((q, resp))

for q, resp in st.session_state.history:
    with st.chat_message("user"):
        st.write(q)
    with st.chat_message("assistant"):
        st.write(resp)