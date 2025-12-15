import streamlit as st
from  faq import ingest_faq_data, faq_chain
from pathlib import Path
from router import router
from sql import sql_chain
from smalltalk import talk



faqs_path = Path(__file__).parent /"resources/faq_data.csv"
ingest_faq_data(faqs_path)


def ask(query):
    route = router(query).name
    if route == 'faq':
        return faq_chain(query)
    elif route == 'sql':
        return sql_chain(query)
    elif route == 'smalltalk':
        return talk(query)
    else:
        return "I don't know"

st.title("E-commerce Chatbot")
query = st.chat_input("write your query")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if query:
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})
    response = ask(query)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})