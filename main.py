import flet as ft
import requests
import sqlite3

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
    page.title = "Jarvis System"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    chat_view = ft.ListView(expand=True, spacing=10)
    user_input = ft.TextField(hint_text="Ask Jarvis...", expand=True)

    def send_message(e):
        if not user_input.value:
            return
        
        query = user_input.value
        chat_view.controls.append(ft.Text(f"You: {query}", color=ft.colors.BLUE_200))
        user_input.value = ""
        page.update()
        
        response = ask_ai(query)
        chat_view.controls.append(ft.Text(f"Jarvis: {response}", color=ft.colors.GREEN_200))
        page.update()

    send_btn = ft.IconButton(ft.icons.SEND, on_click=send_message)

    page.add(
        ft.Text("Jarvis AI", size=25, weight="bold"),
        chat_view,
        ft.Row([user_input, send_btn])
    )

ft.app(target=main)
