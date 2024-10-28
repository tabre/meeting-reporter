import requests

import streamlit as st

from pytube import extract

from phi.assistant import Assistant
from phi.llm.anthropic import Claude
from phi.llm.openai import OpenAIChat
from phi.tools.serpapi_tools import SerpApiTools
from phi.tools.website import WebsiteTools

from reporter_app_settings import ReporterAppSettings

LLM_CLASS = OpenAIChat
MODEL = "gpt-4o-mini"
LLM_API_KEY = st.secrets.api_keys.openai

# This was the original model used in this application
CLAUDE_MODEL = "claude-3-5-sonnet-20240620"  # Unused
CLAUDE_CLASS = Claude  # Unused

LANGUAGE_CODE = "en"


def get_transcript(video_id):
    response = requests.get(
        "https://codesoclear.replit.app/yt_transcript",
        params={"video_id": video_id, "lang": LANGUAGE_CODE},
        headers={'Authorization': f"Bearer {st.secrets.api_keys.transcript}"}
    )

    return response.json()


app_settings = ReporterAppSettings.parse_file("reporter_app_settings.json")

st.title(app_settings.title)
st.header(app_settings.header)
st.caption(app_settings.caption)

llm = LLM_CLASS(model=MODEL, api_key=LLM_API_KEY)

writer = Assistant.parse_file("assistants/writer.json")
writer.llm = llm

researcher = Assistant.parse_file("assistants/researcher.json")
researcher.llm = llm
researcher.tools = [
    SerpApiTools(api_key=st.secrets.api_keys.serp),
    WebsiteTools()
]

editor = Assistant.parse_file("assistants/editor.json")
editor.llm = llm
editor.team = [writer, researcher]

query = st.text_input(app_settings.query_input_label)

if query:
    with st.spinner(app_settings.spinner_message):
        transcript = get_transcript(extract.video_id(query))
        response = editor.run(transcript, stream=False)
        st.write(response)
