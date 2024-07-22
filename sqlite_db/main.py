from sqlite_database import *
import flet as ft
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from gemini_api import summarize_audio

# Update the UI again after processing is complete

# Define Page Components
def main_page(page, switch_page):
    notes = get_notes()
    note_list = ft.Column()
    note_list.controls.append(ft.Text("My notes", style="headlineMedium", color="black"),)
    if len(notes) == 0:
        note_list.controls.append(ft.Container(
            content=ft.Text("No notes.. yet!\nTap New Note below to start", color="white"),
            alignment=ft.alignment.center,
            padding=20,
            width=300,
            height=200,
            border_radius=10,
            bgcolor=ft.colors.GREY_900,
        ))
        note_list.controls.append(ft.Container(height=30),)
        note_list.controls.append(ft.IconButton(icon=ft.icons.ADD, on_click=lambda e: switch_page("create_note")),)
    else:
        note_list.controls.append(ft.Column([
            ft.Text("My notes", style="headlineMedium", color="black"),
            ft.Container(height=30),
            ft.IconButton(icon=ft.icons.ADD, on_click=lambda e: switch_page("create_note")),
        ]))
        for note_id, title, flie_name, result_json, timestamp in notes:
            note_list.controls.append(ft.Row([
                ft.Text(f"{title} ({timestamp})"),
                ft.ElevatedButton("View", on_click=lambda e, nid=note_id: switch_page(f"note_{nid}")),
                ft.ElevatedButton("Delete", on_click=lambda e, nid=note_id: on_delete(nid, switch_page))
            ]))
    

    return ft.Container(content=note_list)
def on_delete(note_id, switch_page):
    delete_note(note_id)
    switch_page("main")

def create_note_page(page, switch_page):
    title_input = ft.TextField(label="Title")
    file_path = [""]
    file_name = [""]
    result_column = ft.Column()
    buttons = ft.Column()
    
    Result = [{
        "text": "Sample text",
        "summary": "Sample summary",
        "note": "Sample note",
        "source": "Sample source",
        "execute_time": "Sample execute time",
    }]
    is_generating = False
    def select_audio_file(e):
        file_path[0] = ""
        file_name[0] = ""
        Tk().withdraw()  # Hide the Tkinter window
        file_path[0] = askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        
        if file_path[0]:
            file_name[0] = os.path.basename(file_path[0])
            result_column.controls.clear()
            result_column.update()
            result_column.controls.append(ft.Text(f"Selected File: {file_name[0]}"))
            result_column.update()  # Ensure the UI updates to show the selected file

            buttons.controls.clear()
            buttons.controls.append(ft.Column([
                ft.ElevatedButton("Reselect file", on_click=select_audio_file),
                ft.ElevatedButton("Generate Note", on_click=generate_Note,disabled=False,),
                ft.ElevatedButton("Save", on_click=on_save,disabled=False),
                ft.ElevatedButton("Back", on_click=lambda e: switch_page("main")),
            ]))
            buttons.update()

    
    def generate_Note(e):
        loading_text = ft.Text("Loading, please wait...")
        result_column.controls.clear()
        result_column.controls.append(loading_text)
        result_column.update()

        buttons.controls.clear()
        buttons.update()

        result = summarize_audio(file_path[0],file_name[0])
        result_column.controls.clear()
        result_column.controls.append(ft.Text(f"Selected File: {file_name[0]}"))
        result_column.controls.append(ft.Text(f"Execute time: {result['execute_time']}"))
        
        result_column.controls.append(ft.Markdown(f"# Generated by:\n{result['source']}")) 
        result_column.controls.append(ft.Markdown(f"# Note:\n{result['note']}")) 
        result_column.controls.append(ft.Markdown(f"# Summary:\n{result['summary']}")) 
        result_column.controls.append(ft.Markdown(f"# Transcript:\n{result['text']}"))
        result_column.update()
        
        Result[0] = result
        print(f"Execute time: {result['execute_time']}")
        buttons.controls.clear()
        buttons.controls.append(ft.Column([
            ft.ElevatedButton("Save", on_click=on_save),
            ft.ElevatedButton("Back", on_click=lambda e: switch_page("main")),
        ]))
        buttons.update()
    def on_save(e):
        if title_input.value:
            create_note(title_input.value, file_name[0], Result[0])
        else:
            create_note(f"Generate Note from {file_name[0]}", file_name[0], Result[0])
        switch_page("main")

    buttons.controls.append(ft.Column([
        ft.ElevatedButton("Select file", on_click=select_audio_file),
        ft.ElevatedButton("Generate Note", on_click=generate_Note,disabled=True),
        ft.ElevatedButton("Save", on_click=on_save,disabled=True),
        ft.ElevatedButton("Back", on_click=lambda e: switch_page("main")),
    ]))
    return ft.Column([
        ft.Text("Create New Note"),
        title_input,
        result_column,
        buttons,
    ])

def note_page(note_id, page, switch_page):
    title, file_name, result = get_note_content(note_id)
    result_column = ft.Column()
    result_column.controls.append(ft.Text(f"Selected File: {file_name}"))
    result_column.controls.append(ft.Text(f"Execute time: {result['execute_time']}"))
    # Wrap each Markdown widget in a ScrollView to make it scrollable
    result_column.controls.append(ft.Markdown(f"# Generated by:\n{result['source']}")) 
    result_column.controls.append(ft.Markdown(f"# Note:\n{result['note']}")) 
    result_column.controls.append(ft.Markdown(f"# Summary:\n{result['summary']}")) 
    result_column.controls.append(ft.Markdown(f"# Transcript:\n{result['text']}"))
    return ft.Column([
        ft.Text(f"Title: {title}"),
        ft.Text(f"File Name: {file_name}"),
        result_column,
        ft.ElevatedButton("Back", on_click=lambda e: switch_page("main")),
    ])

# Dynamic Page Management and Main Function
def main(page: ft.Page):
    page.dark_mode = True
    page.display = "flex"
    pages_list = {
        "main": main_page,
        "create_note": create_note_page,
    }

    def switch_page(page_name):
        page.controls.clear()
        if page_name.startswith("note_"):
            note_id = int(page_name.split("_")[1])
            page.controls.append(note_page(note_id, page, switch_page))
        else:
            page.controls.append(pages_list[page_name](page, switch_page))
        page.update()
    page.scroll = "auto"
    switch_page("main")

ft.app(target=main)