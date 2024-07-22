import flet as ft
from pages.home_screen import HomeScreen
def view_handler(page: ft.Page):
    return {
        '/': ft.View(
            route="/",
            controls=[
                HomeScreen(page)
            ]
        ),
    }