import streamlit as st
from query import answer

st.set_page_config(page_title="DocMind by Shlok", page_icon="🧠")
st.title("🧠 DocMind")
st.caption("by Shlok — Chat with your documents, powered by local AI")

if "history" not in st.session_state:
    st.session_state.history = []

q = st.chat_input("Ask something about your docs...")
if q:
    with st.spinner("Thinking..."):
        resp, sources = answer(q)
    st.session_state.history.append((q, resp, sources))

for q, resp, sources in st.session_state.history:
    with st.chat_message("user"):
        st.write(q)
    with st.chat_message("assistant"):
        st.write(resp)
        if sources:
            st.caption(f"📚 Sources: {', '.join(sources)}")