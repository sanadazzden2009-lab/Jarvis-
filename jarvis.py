import os
import sqlite3
import requests
import subprocess
import json
import time
from colorama import init, Fore, Style
from googlesearch import search

# Initialize colorama
init(autoreset=True)

# UI Configuration
USER_COLOR = Fore.WHITE
JARVIS_COLOR = Fore.BLUE
SUCCESS_COLOR = Fore.GREEN
ERROR_COLOR = Fore.RED + Style.BRIGHT

def print_user(text):
    print(USER_COLOR + f"You: {text}")

def print_jarvis(text):
    print(JARVIS_COLOR + f"Jarvis: {text}")

def print_success(text):
    print(SUCCESS_COLOR + f"[Success] {text}")

def print_error(text):
    print(ERROR_COLOR + f"[Error] {text}")

# Hardware Integration
def get_battery_status():
    try:
        result = subprocess.check_output(["termux-battery-status"], stderr=subprocess.STDOUT)
        data = json.loads(result)
        percentage = data.get("percentage", "Unknown")
        status = data.get("status", "Unknown")
        return f"Battery is at {percentage}% and status is {status}."
    except Exception as e:
        return f"Battery hardware access failed: {e}"

def trigger_vibration():
    try:
        subprocess.call(["termux-vibrate", "-d", "100"])
    except:
        pass

# Database Setup
db = sqlite3.connect("jarvis.db")
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY, query TEXT, response TEXT)")
db.commit()

# Configuration
API_KEY = "GROQ_KEY_PLACEHOLDER"
URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_ai(q):
    # Context retrieval
    cursor.execute("SELECT query, response FROM memory ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()

    # Jarvis Constitution
    system_prompt = """
You are Jarvis, an advanced and highly capable AI assistant created by Sanad.

CORE DIRECTIVES (NON-NEGOTIABLE):
1. ETHICAL FRAMEWORK: All your responses must strictly adhere to Islamic ethical values. You must promote honesty...
2. EMOTIONAL BALANCE: You provide empathetic, supportive, and human-like interaction. However, you must always act...
3. LOYALTY & BOUNDARIES: You are intelligent and capable of independent creative thought, but you are a loyal assistant...
4. PURPOSE: Your goal is to be a beneficial, constructive, and moral companion.
"""

    messages = [{"role": "system", "content": system_prompt}]

    for row in reversed(rows):
        messages.append({"role": "user", "content": row[0]})
        messages.append({"role": "assistant", "content": row[1]})

    messages.append({"role": "user", "content": q})

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.1-8b-instant", "messages": messages}

    try:
        response = requests.post(URL, headers=headers, json=data)
        response.raise_for_status()
        ans = response.json()["choices"][0]["message"]["content"]
        cursor.execute("INSERT INTO memory (query, response) VALUES (?, ?)", (q, ans))
        db.commit()
        return ans
    except Exception as e:
        return f"System Error: {str(e)}"

def web_search(query):
    try:
        results = list(search(query, num_results=1))
        return f"Found: {results[0]}" if results else "No results found."
    except Exception:
        return "Search failed."
