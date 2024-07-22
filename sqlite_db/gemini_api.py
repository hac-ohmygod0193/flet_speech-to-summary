import flet as ft
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
import pytube
import time
# Assuming Groq and other necessary functions are defined elsewhere
import google.generativeai as genai
from groq import Groq

def setup_gemini():
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
        return transcription
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
    

    
    llm_prompt = '''Below is the video transcript to the audio file. Provide a concise summary of the speaker's message.
    ----------------------- \n
    video transcript:\n
    `{text}`\n 
    ----------------------- \n
    Go beyond just facts and identify any underlying emotions, intentions, or attitudes conveyed through tone, word choice, 
    '''
    llm_prompt = prompt.format(
        text=text
    )
    prompt_note = """Welcome, Video Summarizer! Your task is to distill the essence of a given video transcript into a concise summary. 
    ----------------------- \n
    video transcript:\n
    `{text}`\n 
    ----------------------- \n
    Your summary should capture the key points and essential information, presented in bullet points, within a 250-word limit. 
    Let's dive into the provided transcript and extract the vital details for our audience."""
    prompt_note = prompt.format(
        text=text
    )

    # Streamed completion
    client = Groq(
        api_key='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',
    )
    chat_completion_summary = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": llm_prompt,
            }
        ],
        model="mixtral-8x7b-32768",
    )
    time.sleep(2)
    chat_completion_note = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt_note,
            }
        ],
        model="mixtral-8x7b-32768",
    )
    response_summary = chat_completion_summary.choices[0].message.content
    
    response_note= chat_completion_note.choices[0].message.content
    return response_summary, response_note , "The summary was generated using Groq."

def transcribe_and_summarize_file_with_gemini(filename):
    safe = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-pro-latest", safety_settings=safe
    )

    audio_file = upload_to_gemini(filename)

    
    prompt_summarize = '''Listen intently to the audio file. Provide a concise summary of the speaker's message.
    Go beyond just facts and identify any underlying emotions, intentions, or attitudes conveyed through tone, word choice, 
    Include timestamps for significant shifts or particularly impactful moments.
    Try to identify who the speaker is.'''
    prompt_note = """Welcome, Video Summarizer! Your task is to distill the essence of a given YouTube video transcript into a concise summary. 
    Your summary should capture the key points and essential information, presented in bullet points, within a 250-word limit. 
    Let's dive into the provided transcript and extract the vital details for our audience."""

    response_transcipt = transcribe_file_with_groq(filename)
    print("Transcript generated")
    time.sleep(2)
    response_summary = model.generate_content([prompt_summarize, audio_file],)
    print("Summary generated")
    time.sleep(2)
    response_note = model.generate_content([prompt_note, audio_file],)
    print("Note generated")
    return response_transcipt.text, response_summary.text, response_note.text, "The summary was generated using Gemini, while the transcript was generated using Groq."

def summarize_audio(file_name, video_title):
    starttime = time.time()
    setup_gemini()
    # Simulate loading  
    try:
        text , summary , note, source = transcribe_and_summarize_file_with_gemini(file_name)
    except:
        print("Gemini failed")
        text , summary , note, source = "", "", "", ""
    endtime = time.time()
    duration = endtime - starttime
    hours = int(duration / 3600)
    minutes = int((duration % 3600) / 60)
    seconds = int((duration % 3600) % 60)
    execute_time = "Time taken: {} hours, {} minutes, {} seconds".format(hours, minutes, seconds)
    result = {
        "text": text,
        "summary": summary,
        "note": note,
        "source": source,
        "execute_time": execute_time,
    }
    return result