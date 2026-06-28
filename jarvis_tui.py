from rich.console import Console
from rich.panel import Panel
from jarvis import ask_ai # تأكد أن ملف jarvis.py موجود في نفس المجلد

console = Console()

console.print(Panel("[bold green]Jarvis Core System Online[/bold green]"))

while True:
    query = console.input("[bold blue]You:[/bold blue] ")
    if query.lower() in ["exit", "quit"]:
        break
    
    with console.status("[bold yellow]Jarvis is thinking...[/bold yellow]"):
        response = ask_ai(query)
    
    console.print(Panel(response, title="[bold green]Jarvis[/bold green]", border_style="green"))

