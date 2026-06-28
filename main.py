import flet as ft
# Import the AI logic from your previous file without modification
from jarvis import ask_ai

def main(page: ft.Page):
    page.title = "Jarvis System UI"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.START

    chat_view = ft.ListView(expand=True, spacing=10)
    user_input = ft.TextField(hint_text="Enter your command for Jarvis...", expand=True)

    def send_message(e):
        if not user_input.value:
            return
        
        query = user_input.value
        # Display user query on screen
        chat_view.controls.append(ft.Text(f"You: {query}", color=ft.colors.BLUE_200))
        user_input.value = ""
        page.update()
        
        # Call Jarvis logic from jarvis.py
        try:
            response = ask_ai(query)
            chat_view.controls.append(ft.Text(f"Jarvis: {response}", color=ft.colors.GREEN_200))
        except Exception as ex:
            chat_view.controls.append(ft.Text(f"System Error: {str(ex)}", color=ft.colors.RED_400))
            
        page.update()

    send_btn = ft.ElevatedButton("Send", on_click=send_message)

    page.add(
        ft.Text("Jarvis AI System", size=30, weight="bold"),
        chat_view,
        ft.Row([user_input, send_btn])
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER)


