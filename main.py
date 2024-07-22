import flet as ft
from view_pages import view_handler

def main(page: ft.Page):
    page.title = "My Notes App"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def route_change(route):
        print(page.route)
        page.views.clear()
        page.views.append(view_handler(page)[page.route])
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
