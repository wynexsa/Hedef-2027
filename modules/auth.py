import json
import os
from config import DATA_FILE, DEFAULT_DATA
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_DATA

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def check_first_run(data):
    if not data["student"]["full_name"]:
        clear_screen()
        console.print(Panel("[bold cyan]HEDEF 2027 - ÖĞRENCİ KAYDI[/bold cyan]", expand=False))
        full_name = Prompt.ask("[bold yellow]Adınız Soyadınız[/bold yellow]").strip()
        school_num = Prompt.ask("[bold yellow]Okul Numaranız[/bold yellow]").strip()
        
        data["student"]["full_name"] = full_name
        data["student"]["school_number"] = school_num
        save_data(data)
        
        console.print(f"\n[bold green][✔] Kayıt tamamlandı. Hoş geldin, {full_name}![/bold green]")
        Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
