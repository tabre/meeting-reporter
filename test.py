import streamlit as st

from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat

LLM_CLASS = OpenAIChat
MODEL = "gpt-4o-mini"
LLM_API_KEY = st.secrets.api_keys.openai

LANGUAGE_CODE = "en"

st.title("TEST")
st.header("Streamlit test app")
st.caption("Enter a query")

llm = LLM_CLASS(model=MODEL, api_key=LLM_API_KEY)

assistant = Assistant.parse_file("assistants/test_assistant.json")
assistant.llm = llm

query = st.text_input("Place query here")

if query:
    with st.spinner("Working on it"):
        response = assistant.run(query, stream=False)
        st.write(response)
