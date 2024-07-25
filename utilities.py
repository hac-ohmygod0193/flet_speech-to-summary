import flet as ft
def create_button(text, on_click):
    return ft.ElevatedButton(
        text,
        on_click=on_click,
        style=ft.ButtonStyle(
            color="#FFFFFF",
            bgcolor="#007AFF",
            shape=ft.RoundedRectangleBorder(radius=10),
        )
    )

def create_info_section(title, info_list):
    return ft.Container(
        content=ft.Column([
            ft.Text(title, style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)),
            *[ft.Text(info) for info in info_list]
        ]),
        padding=10,
        border_radius=10,
        bgcolor="#F2F2F7"
    )
def create_section(title, content,page, copy=False):
    def copy_to_clipboard(e):
        page.set_clipboard(content)
        page.show_snack_bar(ft.SnackBar(ft.Text("Text copied to clipboard!")))
    if copy == False:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)),
                    ft.Markdown(content, selectable=True),
                ],
                width=page.window_width - 40,
            ),
            bgcolor="#F2F2F7",
            border_radius=10,
            padding=10,
        )
    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(title, style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)),
                        ft.IconButton(
                            icon=ft.icons.COPY,
                            on_click=copy_to_clipboard,
                        ),
                    ],
                ),
                ft.Container(
                    content=ft.Markdown(content, selectable=True),
                    bgcolor="#FFFFFF",
                    border_radius=10,
                    padding=10,
                ),
            ],
            width=page.window_width - 40,
        ),
        bgcolor="#F2F2F7",
        border_radius=10,
        padding=10,
    )
def create_scrollable_section(title, content,page ,copy=False):
    def copy_to_clipboard(e):
        page.set_clipboard(content)
        page.show_snack_bar(ft.SnackBar(ft.Text("Text copied to clipboard!")))
    if copy==False:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)),
                    ft.Container(
                        content=ft.Markdown(content,selectable=True),
                        bgcolor="#FFFFFF",
                        border_radius=10,
                        padding=10,
                    )
                ],
                scroll=ft.ScrollMode.ALWAYS,
                height=200,
                width=page.window_width - 40
            ),
            bgcolor="#F2F2F7",
            border_radius=10,
            padding=10,
        )
    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(title, style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)),
                        ft.IconButton(
                                icon=ft.icons.COPY,
                                on_click=copy_to_clipboard,
                            ),  
                    ],
                ),
                
                ft.Container(
                    content=ft.Markdown(content, selectable=True),
                    bgcolor="#FFFFFF",
                    border_radius=10,
                    padding=10,
                ),
                
            ],
            scroll=ft.ScrollMode.ALWAYS,
            height=200,
            width=page.window_width - 40
        ),
        bgcolor="#F2F2F7",
        border_radius=10,
        padding=10,
    )