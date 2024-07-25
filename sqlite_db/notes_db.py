import sqlite3

import sqlite3
import json
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def init_note_db():
    conn = sqlite3.connect('notes_app.db')
    cursor = conn.cursor()
    # Create a table for storing notes with a result column
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        file_name TEXT,
        result TEXT,  -- This column will store the JSON serialized dictionary
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()
def create_note(title, file_name, result):
    conn = sqlite3.connect('notes_app.db')
    cursor = conn.cursor()
    result_json = json.dumps(result)  # Serialize the result dictionary to JSON
    cursor.execute('''
    INSERT INTO notes (title, file_name, result) VALUES (?, ?, ?)
    ''', (title, file_name, result_json))
    conn.commit()
    conn.close()

def get_notes():
    conn = sqlite3.connect('notes_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, file_name, result, timestamp FROM notes ORDER BY timestamp DESC')
    notes = cursor.fetchall()
    conn.close()
    return notes

def get_note_content(note_id):
    conn = sqlite3.connect('notes_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, file_name, result, timestamp FROM notes WHERE id = ?', (note_id,))
    note = cursor.fetchone()
    conn.close()
    if note:
        title, file_name, result_json, timestamp = note
        result = json.loads(result_json)  # Deserialize the JSON back to a dictionary
        return title, file_name, result, timestamp
    return None, None, None
def delete_note(note_id):
    conn = sqlite3.connect('notes_app.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()
