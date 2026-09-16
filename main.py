import sys
import time
from datetime import datetime
from config import DATA_FILE
from modules.auth import load_data, check_first_run, clear_screen
from modules.schedule import show_schedule
from modules.tracker import log_questions
from modules.announcements import show_announcements, show_links
from modules.admin import admin_panel
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def calculate_lgs_countdown():
    target_date = datetime(2027, 6, 6, 9, 30)
    now = datetime.now()
    diff = target_date - now
    if diff.days < 0:
        return "Sınav Dönemi Tamamlandı"
    days = diff.days
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60
    seconds = diff.seconds % 60
    return f"{days} Gün {hours} Saat {minutes} Dakika {seconds} Saniye"

def main():
    data = load_data()
    check_first_run(data)
    
    while True:
        clear_screen()
        student = data.get("student", {})
        student_name = student.get("full_name", "Belirtilmedi")
        student_no = student.get("school_number", "---")
        
        now = datetime.now()
        days_tr = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        day_str = days_tr[now.weekday()]
        date_str = now.strftime("%d.%m.%Y - %H:%M:%S")
        
        header_text = (
            f"[bold white]👤 Öğrenci:[/bold white] {student_name} (No: {student_no})\n"
            f"[bold white]📅 Tarih / Saat:[/bold white] {date_str} {day_str}\n"
            f"[bold white]⏳ LGS'ye Kalan Süre:[/bold white] {calculate_lgs_countdown()}"
        )
        
        console.print(Panel(header_text, title="[bold cyan]HEDEF 2027 v1.0 | Oruç Reis Ortaokulu 8-C[/bold cyan]", expand=False))
        
        menu = (
            "\n"
            "  [bold cyan][1][/bold cyan] 📋 Günlük Ders Programı\n"
            "  [bold cyan][2][/bold cyan] ✍️ Günlük Soru Çözüm Günlüğü\n"
            "  [bold cyan][3][/bold cyan] 🔗 Faydalı LGS Linkleri\n"
            "  [bold cyan][4][/bold cyan] 🔐 Öğretmen / Admin Girişi\n"
            "  [bold cyan][5][/bold cyan] 📢 Sınıf Duyuruları\n"
            "  [bold red][0][/bold red] 🚪 Çıkış\n"
        )
        console.print(menu)
        
        choice = Prompt.ask("[bold yellow]Seçiminiz (0-5)[/bold yellow]", choices=["0", "1", "2", "3", "4", "5"])
        
        if choice == "0":
            clear_screen()
            console.print("[bold green]İyi çalışmalar! LGS yolunda başarılar dileriz...[/bold green]\n")
            sys.exit(0)
        elif choice == "1":
            show_schedule(data)
        elif choice == "2":
            log_questions(data)
        elif choice == "3":
            show_links()
        elif choice == "4":
            admin_panel(data)
        elif choice == "5":
            show_announcements(data)

if __name__ == "__main__":
    main()
