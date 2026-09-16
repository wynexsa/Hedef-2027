from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from modules.auth import clear_screen, save_data

console = Console()

LESSONS = ["Türkçe", "Matematik", "Fen Bilimleri", "İnkılap Tarihi", "Din Kültürü", "İngilizce"]

def log_questions(data):
    clear_screen()
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    console.print(Panel("[bold cyan]✍️ GÜNLÜK SORU ÇÖZÜM GÜNLÜĞÜ[/bold cyan]", expand=False))
    console.print(f"[yellow]Tarih: {datetime.now().strftime('%d.%m.%Y')}[/yellow]\n")

    current_logs = data.get("question_logs", {}).get(today_str, {})
    new_logs = {}
    day_total = 0

    for lesson in LESSONS:
        old_val = current_logs.get(lesson, 0)
        inp = Prompt.ask(f"[bold white]{lesson}[/bold white] (Mevcut: {old_val}) -> Çözülen Soru", default=str(old_val))
        try:
            val = int(inp)
            val = max(0, val)
        except ValueError:
            val = old_val
        new_logs[lesson] = val
        day_total += val

    if "question_logs" not in data:
        data["question_logs"] = {}
    data["question_logs"][today_str] = new_logs
    save_data(data)

    console.print(f"\n[bold green][✔] Veriler kaydedildi! Bugün toplam {day_total} soru çözdün.[/bold green]")
    Prompt.ask("\n[dim]Ana menüye dönmek için Enter'a basın...[/dim]")
