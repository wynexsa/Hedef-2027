from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from modules.auth import clear_screen

console = Console()

DAYS_TR = {
    0: "Pazartesi", 1: "Salı", 2: "Çarşamba",
    3: "Perşembe", 4: "Cuma", 5: "Cumartesi", 6: "Pazar"
}

def show_schedule(data):
    clear_screen()
    today_idx = datetime.now().weekday()
    today_name = DAYS_TR.get(today_idx, "Pazartesi")
    
    if today_name in ["Cumartesi", "Pazar"]:
        selected_day = "Pazartesi"
        subtitle = f"Bugün {today_name} (Hafta Sonu). Pazartesi Programı Gösteriliyor:"
    else:
        selected_day = today_name
        subtitle = f"Bugün {selected_day}:"

    console.print(Panel(f"[bold cyan]GÜNLÜK DERS PROGRAMI (Oruç Reis Ortaokulu 8-C)[/bold cyan]\n[yellow]{subtitle}[/yellow]", expand=False))

    schedule_list = data.get("schedule", {}).get(selected_day, [])
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Ders", style="dim", width=8, justify="center")
    table.add_column("Saat Aralığı", width=18, justify="center")
    table.add_column("Ders Adı", width=22)
    table.add_column("Öğretmen", width=20)

    for idx, item in enumerate(schedule_list, 1):
        table.add_row(
            f"{idx}. Ders",
            item.get("time", "-"),
            item.get("lesson", "-"),
            item.get("teacher", "-")
        )

    console.print(table)
    console.print("\n[bold green]Çıkış Saati: 13:00[/bold green]")
    Prompt.ask("\n[dim]Ana menüye dönmek için Enter'a basın...[/dim]")
