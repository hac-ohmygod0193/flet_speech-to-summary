import warnings

# Suppress specific DeprecationWarnings related to google._upb._message
warnings.filterwarnings("ignore", category=DeprecationWarning, 
                        message="Type google._upb._message.* uses PyType_Spec with a metaclass that has custom tp_new")

import flet as ft
from flet import Page, Markdown, TextField, ElevatedButton, Text, Column
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

def create_new_page(page: ft.Page):
    def on_dialog_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB

            def audio_page(page: ft.Page):
                page.title = "Audio File Details"
                page.add(
                    ft.Column([
                        ft.Text(f"Audio File: {file_name}", size=20, weight="bold"),
                        ft.Text(f"File Size: {file_size:.2f} MB"),
                        ft.Text(f"File Path: {file_path}"),
                        ft.ElevatedButton(
                            "Close",
                            on_click=lambda _: page.window_close()
                        )
                    ])
                )

            ft.app(target=audio_page, view=ft.FLET_APP)

    file_picker = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)
    page.update()
    file_picker.pick_files(allowed_extensions=["mp3", "wav", "ogg"])
def main(page: ft.Page):
    page.title = "My Notes"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def add_note(e):
        page.dialog = new_note_dialog
        new_note_dialog.open = True
        page.update()
    def close_dialog(page):
        page.dialog.open = False
        page.update()
    new_note_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("New Note"),
        content=ft.Column(
            [
                ft.ListTile(
                    leading=ft.Icon(ft.icons.UPLOAD_FILE),
                    title=ft.Text("Upload audio"),
                    on_click=lambda _: create_new_page(page),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.MIC),
                    title=ft.Text("Record audio"),
                    on_click=lambda _: print("Record audio clicked"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.LINK),
                    title=ft.Text("Use YouTube video"),
                    on_click=lambda _: print("Use YouTube video clicked"),
                ),
            ]
        ),
        actions=[
            ft.TextButton("Cancel", on_click=lambda _: close_dialog(page))
        ],
    )


    page.add(
        ft.Column(
            [
                ft.Text("My notes", style=ft.TextThemeStyle.HEADLINE_MEDIUM, color=ft.colors.WHITE),
                ft.Text("No notes.. yet!\nTap New Note below to start", color=ft.colors.WHITE70),
                ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_note),
                ft.Text("New Note"),  # Added line
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
