import requests
import os
import time
import json
GEMINI_API_KEY = "AIzaSyC1AvNP415NBGejTmM97P9uvgNXbWb53iQ"
GROQ_API_KEY = "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"
FILES = ["一小時略懂 AI｜GPT、Sora、Diffusion model、類器官智慧OI、圖靈測試、人工智慧史.mp3"]
MIME_TYPES = ["audio/mpeg"]

file_uris = []
def upload_to_gemini(API_KEY, file, mime_type="audio/mpeg"):
    # Upload files
    file_size = os.path.getsize(file)
    print(file_size)
    with open(file, 'rb') as f:
        upload_response = requests.post(
            f"https://generativelanguage.googleapis.com/upload/v1beta/files?key={API_KEY}",
            headers={
                "X-Goog-Upload-Command": "start, upload, finalize",
                "X-Goog-Upload-Header-Content-Length": str(file_size),
                "X-Goog-Upload-Header-Content-Type": mime_type,
                "Content-Type": mime_type,
            },
            json={'file': {'display_name': file}},
            data=f.read()
        )

    if upload_response.status_code == 200:
        file_uris.append(upload_response.json()['file']['uri'])
    else:
        print(f"File upload failed: {upload_response.text}")
    result = upload_response.json()['file']
    print(f"Uploaded file '{file}' as: {result['uri']}")
    return result['uri']
def generate_content(API_KEY, file_uri, prompt):
    # Generate content
    generate_content_response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={API_KEY}",
        headers={
            "Content-Type": "application/json",
        },
        json={
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "fileData": {
                                "fileUri": file_uri,
                                "mimeType": "audio/mpeg"
                            }
                        }
                    ]
                },
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "safetySettings": [
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
        }
    )
    summary = ""
    if generate_content_response.status_code == 200:
        print(f"Generate content response: {generate_content_response.text}")
        summary = generate_content_response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        print(f"Generate content failed: {generate_content_response.text}")
        summary = generate_content_response.text
    return summary

# API key and URL
def transcribe_audio(file, API_KEY):
    url = "https://api.groq.com/openai/v1/audio/transcriptions"

    # Form data
    files = {
        'file': open(file, 'rb')
    }
    data = {
        'model': 'whisper-large-v3',
        'response_format': 'verbose_json'
    }
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    # Make the POST request
    response = requests.post(url, headers=headers, files=files, data=data)

    # Write the response to a file
    with open('./transcription.json', 'w') as f:
        f.write(response.text)
    
    transcription = ""
    if response.status_code == 200:
        print('Transcription saved to transcription.json')
        transcription = response.json()['text']
    else:
        print(f"Transcription failed: {response.text}")
    
    return transcription

def groq_generate_content(prompt, API_KEY):
    url = "https://api.groq.com/openai/v1/chat/completions"

    # JSON payload
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "llama-3.1-70b-versatile",
        "temperature": 1,
    }

    # Headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    result = ""
    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        # Print the response
        result = response.json()['choices'][0]['message']['content']
    else:
        print(f"Request failed: {response.text}")
    
    return result

for file, mime_type in zip(FILES, MIME_TYPES):
    print("Uploading file...")
    transcription = transcribe_audio(file, GROQ_API_KEY)
    prompt_summarize = f'''Below is the video transcript to the audio file. Provide a concise summary of the speaker's message.
    ----------------------- \n
    video transcript:\n
    `{transcription}`\n 
    ----------------------- \n
    Go beyond just facts and identify any intentions, or attitudes conveyed through tone, word choice, 
    '''
    print("Generating content...")
    time.sleep(2)
    result = groq_generate_content(prompt_summarize, GROQ_API_KEY)
    print(result)
    """
    file_uri = upload_to_gemini(GEMINI_API_KEY, file, mime_type)
    time.sleep(2)
    print("Generating content...")
    prompt_summarize = '''Listen intently to the audio file. Provide a concise summary of the speaker's message.
    Go beyond just facts and identify any underlying intentions, or attitudes conveyed through tone, word choice, 
    Include timestamps for significant shifts or particularly impactful moments.
    Try to identify who the speaker is.'''
    _ = generate_content(GEMINI_API_KEY, file_uri, prompt_summarize)
    """
    