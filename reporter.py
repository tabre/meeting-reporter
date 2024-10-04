from textwrap import dedent
from phi.assistant import Assistant
from phi.llm.anthropic import Claude
from phi.tools.serpapi_tools import SerpApiTools
from pytube import extract
import os
import json
from phi.tools.website import WebsiteTools
import streamlit as st
from phi.llm.openai import OpenAIChat
from youtube_transcript_api import YouTubeTranscriptApi

claude_api_key = st.secrets['claude_api_key']
serp_api_key = st.secrets['serp_api_key']


st.title("Meeting Reporter")
st.caption("Learn what happened in a Commission meeting")


def get_video_id(url):
    return extract.video_id(url)

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    full_transcript = " ".join([i['text'] for i in transcript])
    return full_transcript


if claude_api_key and serp_api_key:

    writer = Assistant(
        name="Writer",
        role="Writes high-quality articles about the content of a commission meeting based on the transcript",
        llm=Claude(
            model="claude-3-5-sonnet-20240620",
            api_key=claude_api_key,
        ),
        description=dedent(
            """\
            You are a senior writer for an award winning newspaper. Given a transcript of a commission meeting,
            your goal is to identify the important stories and write a high-quality headline and article about each one.
            """
        ),
        instructions=[
            "Given a transcript of a commission meeting, first identify the important stories and write a headline for each.",
            "Then write a high-quality print newspaper article to accompany each headline.",
            "The articles should be well-structured, informative, and engaging",
            "Never add content that doesn't have a reference or quote.",
            "Ensure you provide a nuanced and balanced opinion, quoting facts where possible. Don't add opinionated words like 'good' or 'bad'. Never use the word Conclusion in the final paragraph.",
            "Remember: you are writing for a newspaper, so the quality of the article is important. Never attribute a comment to someone without including the source.",
            "Focus on clarity, coherence, and overall quality. Never be opinionated. Don't make statements about something being good or bad.",
            "Do not include information or quotes that is not specifically relevant to this story.",
            "Never make up facts or plagiarize.",
        ],
        add_datetime_to_instructions=True,
        add_chat_history_to_prompt=True,
        num_history_messages=3,
        debug_mode=False
    )

    researcher = Assistant(
            name="Researcher",
            role="Research the names of the persons and locales for proper spelling and other relevant info.",
            llm=Claude(
                model="claude-3-5-sonnet-20240620",
                api_key=claude_api_key,
            ),
            description=dedent(
                """\
                You are a world-class researcher for a newspaper. Given headlines and news stories from a meeting, 
                generate a list of 3 search terms for names of those mentioned. Then search the web for each term, analyse the results
                and return the correct names. You need to look for accurate spelling of names, titles, and other items mentioned for accuracy.
            """
            ),
            instructions=[
                "Given a list of headlines and news stort drafts, first generate a list of 3 search terms related to that topic",
                "For each search term, `search_google` and analyze the results.",
                "From the results of all searches, return the 10 most relevant URLs to the topic.",
                "Review each of the search result pages.",
                "Return any context you find on each name so the editor can update the story with correct names",
                "Remember: you are writing for a newspaper, so the quality of the sources is important. Do not include not relevant quotes.",
            ],
            tools=[SerpApiTools(api_key=serp_api_key), WebsiteTools()],
            add_datetime_to_instructions=True,
            debug_mode=False
        )

    editor = Assistant(
        name="Editor",
        llm=Claude(
            model="claude-3-5-sonnet-20240620",
            api_key=claude_api_key,
        ),
        team=[writer, researcher],
        description="You are a senior newspaper editor. Given a list of headlines and articles, your goal is to proof and edit each high quality news article and headline",
        instructions=[
            "Given a transcript from a commission meeting give the transcript to the writer to write high-quality articles and headlines about the important items from the meeting.",
            "Then give the researcher the stories to research the names of the persons and locales for proper spelling and other relevant info.",
            "Edit, proofread, and refine each article to ensure they meet the high standards of a newspaper. Use the research provided by the researcher to spot errors and misspellings.",
            "The articles should be extremely articulate and well written and never be opinionated."
            "Focus on clarity, coherence, and overall quality. Never add information that wasn't in the transcript. Don't add opinions or directives.",
            "Ensure the article is engaging, informative, and objective (don't include opinions).",
            "Remember: you are the final gatekeeper before the article is published.",
            "Remove any subjective statements. Do not add policitcal opinions.",
        ],
        add_datetime_to_instructions=True,
        markdown=True,
        debug_mode=False
    )

    query = st.text_input("Paste the YouTube link for the meeting")

    if query:
        with st.spinner("Writing stories..."):
            video_id = get_video_id(query)
            t = get_transcript(video_id)
            response = editor.run(t, stream=False)
            st.write(response)