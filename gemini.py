# Dependencies
import os, re
from pathlib import Path
import pytube
from pytube import YouTube
import os
from groq import Groq
import time
import google.generativeai as genai

genai.configure(api_key="AIzaSyAG6tdV2IfRKkysCdyfvrOSqwYa4sdaAzc")
print("API key set")
def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file
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
def summarize_text(
    title, text, words, use_api=False, api_token=None, do_sample=False
):

    # Automatic selection of provider
    prompt = f"""
    As an AI tasked with summarizing a video, your objective is to distill the key insights without introducing new information. You should aim to capture the essence of the video in a concise manner. 
    The video you are summarizing is a lecture on the topic of {title}. 
    Your task is to summarize the lecture in {words} words with bullet notes. 
    ----------------------- \n
    TITLE: `{title}`\n
    TEXT:\n
    `{text}`\n 
    ----------------------- \n
    SUMMARY:\n
    """
    

    llm_prompt = prompt.format(
        title=title,text=text,words=words
    )
    llm_prompt = '''Listen intently to the audio file. Provide a concise summary of the speaker's message.
    Go beyond just facts and identify any underlying emotions, intentions, or attitudes conveyed through tone, word choice, 
    Include timestamps for significant shifts or particularly impactful moments.
    Try to identify who the speaker is.'''
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

def transcribe_and_summarize_file_with_gemini(filename):
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-pro-latest"
    )

    audio_file = upload_to_gemini(filename)

    prompt = '''Listen intently to the audio file. Provide a concise summary of the speaker's message.
    Go beyond just facts and identify any underlying emotions, intentions, or attitudes conveyed through tone, word choice, 
    Include timestamps for significant shifts or particularly impactful moments.
    Try to identify who the speaker is.'''

    response = model.generate_content([prompt, audio_file],)
    return response.text, "The summary was generated using Gemini."

def transcribe_youtube_audio(url,  file_name = None,use_gemini=False):
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
    summary = "" , ""
    if text == "":
        out_file = video.download(output_path=target_path)

        file_name = video_title+'.mp3'
        os.rename(out_file, file_name)

        print("target path = " + (file_name))
        print("mp3 has been successfully downloaded.")
        try:
            summary = transcribe_and_summarize_file_with_gemini(file_name)
        except:
            print("Gemini failed")
            text = transcribe_file_with_groq(file_name)
            summary = summarize_text(video_title, text, 500)
    return summary

#upload_to_gemini('audio.mp3', mime_type='audio/mpeg')


starttime = time.time()
print("Enter the URL of the YouTube video or the direct path of the audio file to be transcribed")
#file = str(input())
#file = 'https://www.youtube.com/watch?v=eraWvfD_Ihg'
file = 'https://www.youtube.com/watch?v=orDKvo8h71o'
summary = transcribe_youtube_audio(file)
endtime = time.time()
print(summary[0])
print(summary[1])
duration = endtime - starttime
hours = int(duration / 3600)
minutes = int((duration % 3600) / 60)
seconds = int((duration % 3600) % 60)
print("Time taken: {} hours, {} minutes, {} seconds".format(hours, minutes, seconds))
