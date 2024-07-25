import flet as ft
from apikeys_db import load_api_keys
import time
# Assuming Groq and other necessary functions are defined elsewhere
import google.generativeai as genai
from groq import Groq

def setup_gemini():
    gemini_api_key, _ = load_api_keys()
    if gemini_api_key is None:
        raise ValueError("Gemini API key is not set.")
    genai.configure(api_key = gemini_api_key)
    #genai.configure(api_key="AIzaSyAG6tdV2IfRKkysCdyfvrOSqwYa4sdaAzc")
    print("API key set")
def setup_groq():
    _, groq_api_key = load_api_keys()
    #client = Groq(api_key='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',)
    if groq_api_key is None:
        raise ValueError("Groq API key is not set.")
    return Groq(api_key=groq_api_key)
def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file
def transcribe_file_with_groq(filename):
    client = setup_groq()
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()),
            model="whisper-large-v3",
            response_format="verbose_json",
        )
        print(transcription.text)
        return transcription.text
def summarize_text_with_groq(
    title, text, use_api=False, api_token=None, do_sample=False
):
    
    prompt_summarize = f'''Below is the video transcript to the audio file. Provide a concise summary of the speaker's message.
    ----------------------- \n
    video transcript:\n
    `{text}`\n 
    ----------------------- \n
    Go beyond just facts and identify any intentions, or attitudes conveyed through tone, word choice, 
    '''
    prompt_summarize = prompt_summarize.format(
        text=text
    )
    prompt_note = """Welcome, Video Summarizer! Your task is to distill the essence of a given video transcript into a concise summary. 
    ----------------------- \n
    video transcript:\n
    `{text}`\n 
    ----------------------- \n
    Your summary should capture the key points and essential information, presented in bullet points, within a 250-word limit. 
    Let's dive into the provided transcript and extract the vital details for our audience."""
    prompt_note = prompt_note.format(
        text=text
    )

    # Streamed completion
    client = setup_groq()
    chat_completion_summary = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt_summarize,
            }
        ],
       model="llama-3.1-70b-versatile",
    )
    time.sleep(2)
    chat_completion_note = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt_note,
            }
        ],
        model="llama-3.1-70b-versatile",
    )
    response_summary = chat_completion_summary.choices[0].message.content
    
    response_note= chat_completion_note.choices[0].message.content
    return response_summary, response_note , "The summary was generated using Llama3.1, , while the transcript was generated using Groq."

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
    Go beyond just facts and identify any underlying intentions, or attitudes conveyed through tone, word choice, 
    Include timestamps for significant shifts or particularly impactful moments.
    Try to identify who the speaker is.'''
    prompt_note = """Welcome, Video Summarizer! Your task is to distill the essence of a given YouTube video transcript into a concise note. 
    Your note should capture the key points and essential information, presented in bullet points, within a 250-word limit. 
    Let's dive into the provided transcript and extract the vital details for our audience."""

    
    response_summary = model.generate_content([prompt_summarize, audio_file],)
    print("Summary generated")
    time.sleep(2)
    response_note = model.generate_content([prompt_note, audio_file],)
    print("Note generated")
    return response_summary.text, response_note.text, "The summary was generated using Gemini, while the transcript was generated using Groq."

def summarize_audio(file_name, video_title):
    starttime = time.time()
    setup_gemini()
    # Simulate loading  
    response_transcipt = transcribe_file_with_groq(file_name)
    print("Transcript generated")
    time.sleep(2)
    try:
        summary , note, source = transcribe_and_summarize_file_with_gemini(file_name)
    except:
        print("Gemini failed")
        summary , note, source = summarize_text_with_groq(video_title, response_transcipt)
    endtime = time.time()
    duration = endtime - starttime
    hours = int(duration / 3600)
    minutes = int((duration % 3600) / 60)
    seconds = int((duration % 3600) % 60)
    execute_time = "{} hours, {} minutes, {} seconds".format(hours, minutes, seconds)
    result = {
        "text": response_transcipt,
        "summary": summary,
        "note": note,
        "source": source,
        "execute_time": execute_time,
    }
    return result