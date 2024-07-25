import flet as ft
from apikeys_db import load_api_keys, save_keys

gemini_md = """
## Gemini API Key Setup: \n 
To get your Gemini API key, visit: \n
[https://ai.google.dev/gemini-api/docs/api-key](https://ai.google.dev/gemini-api/docs/api-key) \n 
Follow the instructions to create and retrieve your API key.
"""

groq_md = """
## Groq API Key Setup: \n

To get your Groq API key, visit: \n
[https://console.groq.com/docs/quickstart#create-an-api-key](https://console.groq.com/docs/quickstart#create-an-api-key) \n
Follow the quickstart guide to create your API key.
"""

def settings_page(page, switch_page):
    page.scroll = "auto"
    # Navigation bar
    nav_bar = ft.Container(
        content=ft.Row([
            ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                on_click=lambda _: switch_page("home"),
                icon_color="#007AFF"
            ),
            ft.Text("API Key Settings", style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)),
        ], alignment=ft.MainAxisAlignment.START),
        padding=10,
        bgcolor="#F2F2F7"
    )
    
    _gemini_api_key, _groq_api_key = load_api_keys()
    
    # Create input fields for API keys
    gemini_api_key = ft.TextField(label='Gemini API Key', width=min(page.window.width - 20,300), value=_gemini_api_key)
    groq_api_key = ft.TextField(label='Groq API Key', width=min(page.window.width - 20,300), value=_groq_api_key)

    # API key saved dialog
    def handle_close(e):
        save_api_keys(e)
        page.close(dlg_modal)
        switch_page("home")

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("API Keys Saved"),
        content=ft.Text("Make sure you type the correct API keys for the services."),
        actions=[
            ft.TextButton("Save", on_click=handle_close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    def save_api_keys(e):
        GEMINI_API_KEY = gemini_api_key.value
        GROQ_API_KEY = groq_api_key.value
        save_keys(GEMINI_API_KEY, GROQ_API_KEY)
        page.update()

    
    # Create info boxes for API key setup using Markdown
    gemini_info = ft.Container(
        content=ft.Markdown(
            gemini_md,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            on_tap_link=lambda e: page.launch_url(e.data),
        ),
        padding=10,
        border_radius=10,
        bgcolor="#E3F2FD",
        width = page.window.width - 20,
    )

    groq_info = ft.Container(
        content=ft.Markdown(
            groq_md,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            on_tap_link=lambda e: page.launch_url(e.data),
        ),
        padding=10,
        border_radius=10,
        bgcolor="#E3F2FD",
        width = page.window.width - 20,
    )

    # Content
    content = ft.Column(
        controls=[
            gemini_info,
            ft.Container(height=20),  # Spacer
            gemini_api_key,
            ft.Container(height=20),  # Spacer
            groq_info,
            ft.Container(height=20),  # Spacer
            groq_api_key,
            ft.Container(height=20),  # Spacer
            ft.ElevatedButton(
                text='Save API Keys',
                on_click=lambda e: page.open(dlg_modal),
                style=ft.ButtonStyle(
                    color="#FFFFFF",
                    bgcolor="#007AFF",
                    shape=ft.RoundedRectangleBorder(radius=10),
                )
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=10,
    )
    
    return ft.Column([
        nav_bar,
        ft.Container(
            content=content,
            padding=20,
        )
    ])
