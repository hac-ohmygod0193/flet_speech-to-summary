import flet as ft

class HomeScreen(ft.UserControl):
    def __init__(self , page):
        super().__init__()
        self.page = page
    def build(self):
        self.new_note_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("New Note"),
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.UPLOAD_FILE),
                        title=ft.Text("Upload audio"),
                        on_click=lambda _: print("Upload audio clicked"),
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
            actions=[ft.TextButton("Cancel", on_click=self.close_dialog)],
        )

        return ft.Column(
            [
                ft.Text("My notes", style=ft.TextThemeStyle.HEADLINE_MEDIUM, color=ft.colors.WHITE),
                ft.Text("No notes.. yet!\nTap New Note below to start", color=ft.colors.WHITE70),
                ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_note),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
            
        

    def add_note(self, e):
        self.page.overlay.append(self.new_note_dialog)
        self.new_note_dialog.open = True
        self.page.update()

    def close_dialog(self, e):
        self.new_note_dialog.open = False
        self.page.update()
