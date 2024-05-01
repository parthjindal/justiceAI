from openai import OpenAI
import streamlit as st
import os

st.title("Justice AI")
client = OpenAI(api_key=st.secrets["openai_api_key"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a legal AI assistant that will be used by legal and non-legal professionals for any kind of legal, compliance and regulatory questions. Help them with their queries."}]


# Define default questions and create buttons for them
default_questions = [
    "How to register my startup in US Delaware C Corp?",
    "How to sue a competitor company for using my trademarked logo?",
    "Hit and Run case fall into which section of IPC?",

]

default_ques = False

for question in default_questions:
    if st.button(question):
        default_ques = True
        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "system", "content": "You are a legal AI assistant that will be used by legal and non-legal professionals for any kind of legal, compliance and regulatory questions. Help them with their queries."}]



        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append(
            {"role": "assistant", "content": response})

if not default_ques:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
