import flet as ft
import requests
import sqlite3
import subprocess

# Database setup
conn = sqlite3.connect("memory.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS memory (query TEXT, response TEXT)")
conn.commit()

# API Configuration
API_KEY = "GROQ_KEY_PLACEHOLDER"
URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_ai(q):
    try:
        cursor.execute("SELECT query, response FROM memory")
        rows = cursor.fetchall()
        messages = [{"role": "system", "content": "You are Jarvis, an advanced AI assistant."}]
        for row in reversed(rows[-5:]):
            messages.append({"role": "user", "content": row[0]})
            messages.append({"role": "assistant", "content": row[1]})
        messages.append({"role": "user", "content": q})
        
        headers = {"Authorization": f"Bearer {API_KEY}"}
        data = {"model": "llama-3.1-8b-instant", "messages": messages}
        
        response = requests.post(URL, headers=headers, json=data)
        response.raise_for_status()
        ans = response.json()["choices"][0]["message"]["content"]
        
        cursor.execute("INSERT INTO memory (query, response) VALUES (?, ?)", (q, ans))
        conn.commit()
        return ans
    except Exception as e:
        return f"System Error: {str(e)}"

def main(page: ft.Page):
    page.title = "Jarvis AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    chat_list = ft.ListView(expand=True, spacing=10)
    input_field = ft.TextField(hint_text="Ask Jarvis...", expand=True)

    def send_message(e):
        if not input_field.value:
            return
        
        user_text = input_field.value
        chat_list.controls.append(ft.Text(f"You: {user_text}", color=ft.colors.WHITE))
        input_field.value = ""
        page.update()

        ai_response = ask_ai(user_text)
        chat_list.controls.append(ft.Text(f"Jarvis: {ai_response}", color=ft.colors.BLUE_200))
        page.update()

    page.add(
        chat_list,
        ft.Row([input_field, ft.IconButton(ft.icons.SEND, on_click=send_message)])
    )

ft.app(target=main)

