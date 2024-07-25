import flet as ft
from sqlite_db.notes_db import init_note_db, get_notes, get_note_content, delete_note
from utilities import create_section, create_scrollable_section
from settings import settings_page
from sqlite_db.apikeys_db import init_setting_db
from notes import create_note_page

# Update the UI again after processing is complete
def create_delete_dialog(nid, on_delete_func, switch_page_func, page):
    def on_long_press():
        on_delete_func(nid, switch_page_func)
        page.close(delete_dlg)
        switch_page_func("home")

    delete_dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Delete Note"),
        content=ft.Text("Are you sure you want to delete this note?"),
        actions=[
            ft.TextButton("Cancel", on_click=lambda _: page.close(delete_dlg)),
            ft.TextButton("Delete", on_click=lambda _: on_long_press()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    return delete_dlg
def home_page(page, switch_page):
    notes = get_notes()
    # Add settings icon to home page
    settings_icon = ft.IconButton(icon=ft.icons.SETTINGS, on_click=lambda _: switch_page("settings"))
    # Navigation bar
    nav_bar = ft.Container(
        content=ft.Row([
            ft.Row([ft.Text("My Notes", style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)),settings_icon]),
            ft.IconButton(
                icon=ft.icons.ADD,
                on_click=lambda _: switch_page("create_note"),
                icon_color="#007AFF"
            )
        ], 
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=10,
        bgcolor="#F2F2F7"
    )

    # Note list
    note_list = ft.ListView(spacing=10, padding=20, auto_scroll=True)
    
    if len(notes) == 0:
        note_list.controls.append(
            ft.Container(
                content=ft.Text("No notes yet!\nTap + to create a new note", 
                                color="#8E8E93", text_align=ft.TextAlign.CENTER),
                alignment=ft.alignment.center,
                padding=20,
                width=page.window.width - 20,
                height=page.window.height - 100,
                border_radius=10,
                bgcolor="#F2F2F7",
            )
        )
    else:
        for note_id, title, file_name, result_json, timestamp in notes:
            note_title = title if len(title) <= 40 else title[:37] + '...'
            delete_dlg = create_delete_dialog(note_id, on_delete, switch_page, page)
            note_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(note_title, style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)),
                        ft.Text(timestamp, style=ft.TextStyle(size=14, color="#8E8E93")),
                    ]),
                    on_click=lambda _, nid=note_id: switch_page(f"note_{nid}"),
                    on_long_press=lambda _, dlg=delete_dlg: page.open(dlg),
                    ink=True,
                    padding=10,
                    border_radius=10,
                    bgcolor="#FFFFFF",
                    width=page.window.width - 40,
                )
            )

    return ft.Column([
        nav_bar,
        ft.Container(
            content=note_list,
            padding=10,
        ),
    ])



def on_delete(note_id, switch_page):
    delete_note(note_id)
    switch_page("home")


def note_page(note_id, page, switch_page):
    title, file_name, result,timestamp = get_note_content(note_id)
    note_title = title if len(title) <= 20 else title[:17] + '...'
    # Navigation bar
    nav_bar = ft.Container(
        content=ft.Row([
            ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                on_click=lambda _: switch_page("home"),
                icon_color="#007AFF"
            ),
            ft.Text(note_title, style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)),
        ], alignment=ft.MainAxisAlignment.START,width=page.window.width-20),
        padding=10,
        bgcolor="#F2F2F7"
    )

    # Content
    content = ft.ListView(
        spacing=20,
        padding=20,
        auto_scroll=True
    )

    content.controls.extend([
        ft.Container(
            content=ft.Column([
                ft.Text("File Information", style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)),
                ft.Text(f"File: {file_name}"),
                ft.Text(f"Generate Time: {timestamp}"),
                ft.Text(f"Execute time: {result['execute_time']}"),
            ]),
            padding=10,
            border_radius=10,
            bgcolor="#F2F2F7"
        ),
        create_section("Note", result['note'],page, copy=True),
        create_section("Summary", result['summary'],page,copy=True),
        create_scrollable_section("Transcript", result['text'],page,copy=True),
        create_section("Contributed by", result['source'],page),
        
    ])

    return ft.Column([
        nav_bar,
        ft.Container(
            content=content,
        ),
        ft.Container(
            content=ft.ElevatedButton("Back", on_click=lambda e: switch_page("home")),
            padding=20,
        ),
        
    ])

# Dynamic Page Management and Main Function
# Update the Page settings
def main(page: ft.Page):
    init_note_db()
    init_setting_db()
    page.bgcolor = "#FFFFFF"
    page.padding = 0
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#007AFF",
            on_primary="#FFFFFF",
            surface="#F2F2F7",
            on_surface="#000000"
        )
    )
    page.fonts = {
        "": "SF Pro Display"
    }
    pages_list = {
        "home": home_page,
        "create_note": create_note_page,
        "settings": settings_page,
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
    switch_page("home")

ft.app(target=main)