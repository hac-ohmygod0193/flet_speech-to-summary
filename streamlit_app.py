import streamlit as st
# -*- coding: utf-8 -*-
import datetime
import time
import pytube
# Dependencies
import os, re
from pathlib import Path
from pytube import YouTube
import os
from groq import Groq
from langdetect import detect
from mutagen.mp3 import MP3
from mutagen.mp3 import HeaderNotFoundError

def get_youtube_title(url):
    yt = YouTube(str(url))
    return yt.title
# get the transcript from YouTube
def get_yt_transcript(url):
    text = ""
    vid_id = pytube.extract.video_id(url)
    temp = YouTubeTranscriptApi.get_transcript(vid_id)
    for t in temp:
        text += t["text"] + " "
    return text
def transcribe_file_with_groq(filename):

    client = Groq(api_key='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',)

    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()),
            model="whisper-large-v3",
            response_format="verbose_json",
        )
        print(transcription.text)
        return transcription.text



def transcribe_youtube_audio(url,  file_name = None):
    "Download the audio from a YouTube video"
    target_path = "./"

    yt = YouTube(url)
    video_title = yt.title
    video = yt.streams.filter(only_audio=True).first()
    text = ""
    # get the transcript from YouTube if available
    try:
        text = get_yt_transcript(url)
    except:
        pass
    print("Text:", text)
    if text == "":
        out_file = video.download(output_path=target_path)

        file_name = video_title + '.mp3'
        os.rename(out_file, file_name)

        print("target path = " + (file_name))
        print("mp3 has been successfully downloaded.")
        text = transcribe_file_with_groq(file_name)
    return video_title, text
def summarize_text(
    title, text, words, use_api=False, api_token=None, do_sample=False
):
    # Detect the language of the text
    language = detect(text)

    # Print the detected language
    print("Detected Language:", language)
    # Automatic selection of provider
    prompt = f"""
    As an AI tasked with summarizing a video, your objective is to distill the key insights without introducing new information. You should aim to capture the essence of the video in a concise manner. 
    The video you are summarizing is a lecture on the topic of {title} in {language}. 
    Your task is to summarize the lecture in {words} words with bullet notes. 
    ----------------------- \n
    TITLE: `{title}`\n
    TEXT:\n
    `{text}`\n 
    ----------------------- \n
    SUMMARY:\n
    """
    llm_prompt = prompt.format(
        title=title,text=text,words=words,language=language
    )
    # Streamed completion
    client = Groq(
        api_key='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',
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": llm_prompt,
            }
        ],
        model="mixtral-8x7b-32768",
    )
    response = chat_completion.choices[0].message.content
        
    return response, "The summary was generated using Groq."


st.title("YouTube Transcription and Summarization")
url = st.text_input("Enter YouTube URL:")
button = st.button("Video Summarize")
if button:
    print("START")
    with st.spinner():
        video_title, text = transcribe_youtube_audio(url)
        summary, source = summarize_text(video_title, text, 500)
        st.write("Title:", video_title)
        st.write("Summary:\n", summary)
        st.write("Transcript:\n", text)
