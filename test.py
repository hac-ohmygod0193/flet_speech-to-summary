import flet as ft
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
import pytube
import time
# Assuming Groq and other necessary functions are defined elsewhere
import google.generativeai as genai
from groq import Groq
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
    prompt_note = """Welcome, Video Summarizer! Your task is to distill the essence of a given YouTube video transcript into a concise summary. 
    Your summary should capture the key points and essential information, presented in bullet points, within a 250-word limit. 
    Let's dive into the provided transcript and extract the vital details for our audience."""
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
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-pro-latest"
    )

    audio_file = upload_to_gemini(filename)

    prompt_transcribe = "plain text transcribed from audio"
    prompt_summarize = '''Listen intently to the audio file. Provide a concise summary of the speaker's message.
    Go beyond just facts and identify any underlying emotions, intentions, or attitudes conveyed through tone, word choice, 
    Include timestamps for significant shifts or particularly impactful moments.
    Try to identify who the speaker is.'''
    prompt_note = """Welcome, Video Summarizer! Your task is to distill the essence of a given YouTube video transcript into a concise summary. 
    Your summary should capture the key points and essential information, presented in bullet points, within a 250-word limit. 
    Let's dive into the provided transcript and extract the vital details for our audience."""

    response_transcipt = model.generate_content([prompt_transcribe, audio_file],)
    time.sleep(2)
    response_summary = model.generate_content([prompt_summarize, audio_file],)
    time.sleep(2)
    response_note = model.generate_content([prompt_note, audio_file],)
    return response_transcipt.text, response_summary.text, response_note.text, "The summary was generated using Gemini."

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
import flet as ft
from flet import Page, Markdown, TextField, ElevatedButton, Text, Column
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Assuming you have these functions defined somewhere
# def transcribe_youtube_audio(url):
#     # your implementation here
#     return "Video Title", "Transcription text"

# def summarize_text(title, text, length):
#     # your implementation here
#     return "Summary text", "Source text"
def main(page: Page):
    page.title = "YouTube/Audio Transcription and Summarization"
    def select_audio_file():
        Tk().withdraw()  # Hide the Tkinter window
        file_path = askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        return file_path

    
    result_column = Column()

    def summarize(e):
        starttime = time.time()
        audio_file = select_audio_file()
        print(audio_file)
        file_name = audio_file
        result_column.controls.clear()
        video_title = os.path.basename(audio_file)
        loading_text = Text("Loading, please wait...")
        result_column.controls.append(loading_text)
        result_column.update()

        # Simulate loading
        try:
            text , summary , note, source = transcribe_and_summarize_file_with_gemini(file_name)
        except:
            print("Gemini failed")
            text = transcribe_file_with_groq(file_name)
            summary, note, source = summarize_text(video_title, text, 500)
        endtime = time.time()
        result_column.controls.clear()  # Clear loading message
        runtime = endtime - starttime
        hours = int(runtime // 3600)
        minutes = int((runtime % 3600) // 60)
        seconds = int(runtime % 60)
        result_column.controls.append(Text("Time taken: {} hours, {} minutes, {} seconds".format(hours, minutes, seconds)))
        result_column.controls.append(Markdown(f"# Title: {video_title}"))

        result_column.controls.append(Markdown(f"# Summary:\n{summary}",selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            on_tap_link=lambda e: page.launch_url(e.data)))
        result_column.controls.append(Markdown(f"# Note:\n{note}",selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            on_tap_link=lambda e: page.launch_url(e.data)))
        result_column.controls.append(Text(f"Source: {source}"))
        result_column.controls.append(Markdown(f"# Transcript:\n{text}"))
        
        result_column.update()
    summarize_button = ElevatedButton(text="Video Summarize", on_click=summarize)
    page.scroll = "auto"
    page.add(
        
        Column([
            summarize_button,
            result_column,
        ]
        )

    )

ft.app(target=main)
