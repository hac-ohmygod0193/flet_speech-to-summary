import flet as ft
import sqlite3

def init_setting_db():
    # Create the SQLite database and table
    conn = sqlite3.connect('settings.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS api_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gemini_api_key TEXT,
        groq_api_key TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Load API keys from database
def load_api_keys():
    conn = sqlite3.connect('settings.db')
    cursor = conn.cursor()
    cursor.execute('SELECT gemini_api_key, groq_api_key FROM api_keys WHERE id=1')
    keys = cursor.fetchone()
    
    if keys:
        GEMINI_API_KEY = keys[0]
        GROQ_API_KEY = keys[1]
        conn.close()
        return GEMINI_API_KEY, GROQ_API_KEY
    else:
        conn.close()
        return None, None
    
    
def save_keys(gemini_api_key, groq_api_key):
    #print("Gemini API Key: ", gemini_api_key)
    #print("Groq API Key: ", groq_api_key)
    conn = sqlite3.connect('settings.db')
    c = conn.cursor()
    c.execute('DELETE FROM api_keys WHERE id=1')
    c.execute('INSERT INTO api_keys (id, gemini_api_key, groq_api_key) VALUES (1, ?, ?)', (gemini_api_key, groq_api_key))
    conn.commit()
