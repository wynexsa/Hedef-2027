import sys
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Modül importları
from modules.auth import load_data, check_first_run, clear_screen
from modules.announcements import show_announcements
from modules.tracker import track_questions
from modules.admin import admin_panel

console = Console()

LGS_DATE = datetime(2027, 6, 6, 9, 30, 0)

def get_countdown():
    now = datetime.now()
    remaining = LGS_DATE - now
    if remaining.total_seconds() <= 0:
        return "[bold red]LGS 2027 Başladı veya Sona Erdi![/bold red]"
    
    days = remaining.days
    hours, remainder = divmod(remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"[bold yellow]{days} gün {hours} saat {minutes} dakika {seconds} saniye[/bold yellow]"

def show_student_notifications(data):
    clear_screen()
    console.print(Panel("[bold cyan]🔔 BİLDİRİMLER VE ÖĞRETMEN ÖNERİLERİ[/bold cyan]", expand=False))
    
    student = data.get("student", {})
    notifications = student.get("notifications", [])
    
    if not notifications:
        console.print("[yellow]Henüz size gelen yeni bir bildirim veya öneri bulunmuyor.[/yellow]\n")
    else:
        for idx, notif in enumerate(notifications, 1):
            console.print(f"[bold green]{idx}. [{notif.get('date')}] - Gönderen: {notif.get('sender')}[/bold green]")
            console.print(f"   💬 {notif.get('content')}\n")
            
    Prompt.ask("[dim]Geri dönmek için Enter'a basın...[/dim]")

def main():
    data = load_data()
    check_first_run(data)
    
    while True:
        clear_screen()
        
        # Güncel veriyi her döngüde yenile ki bildirim anında görünsün
        data = load_data()
        student = data.get("student", {})
        notif_count = len(student.get("notifications", []))
        notif_badge = f" [red]({notif_count} Yeni)[/red]" if notif_count > 0 else ""
        
        welcome_msg = f"Hoş geldin, [bold cyan]{student.get('full_name', 'Öğrenci')}[/bold cyan] ({student.get('school_number', 'No Yok')}) | LGS 2027'ye Kalan: {get_countdown()}"
        console.print(Panel(welcome_msg, title="[bold green]HEDEF 2027 - LGS ASİSTANI[/bold green]", expand=False))
        
        # Ana Menü ([0-6])
        console.print("  [bold cyan][1][/bold cyan] 📢 Duyurular")
        console.print(f"  [bold cyan][2][/bold cyan] 🔔 Bildirimlerim ve Öneriler{notif_badge}")
        console.print("  [bold cyan][3][/bold cyan] ✍️ Soru Günlüğü ve Takip")
        console.print("  [bold cyan][4][/bold cyan] 🔗 LGS Faydalı Linkler")
        console.print("  [bold cyan][5][/bold cyan] 🔐 Yetkili Paneli (Öğretmen / Admin)")
        console.print("  [bold cyan][6][/bold cyan] 👤 Öğrenci Bilgilerimi Göster")
        console.print("  [bold red][0][/bold red] 🚪 Çıkış\n")
        
        choice = Prompt.ask("Seçiminiz", choices=["0", "1", "2", "3", "4", "5", "6"])
        
        if choice == "0":
            clear_screen()
            console.print("[bold yellow]Hedef 2027 Asistanı kapatılıyor. Başarılar dileriz![/bold yellow]")
            sys.exit()
        elif choice == "1":
            show_announcements(data)
        elif choice == "2":
            show_student_notifications(data)
        elif choice == "3":
            track_questions(data)
        elif choice == "4":
            clear_screen()
            console.print(Panel("[bold cyan]🔗 LGS FAYDALI LİNKLER[/bold cyan]", expand=False))
            console.print("  • [link=https://www.tongucakademi.com]Tonguç Akademi LGS Portalı[/link]")
            console.print("  • [link=https://www.meb.gov.tr]MEB Resmi Duyurular ve Örnek Sorular[/link]")
            console.print("  • [link=https://odsgm.meb.gov.tr]ÖDSGM Soru Destek Hizmetleri[/link]\n")
            Prompt.ask("[dim]Geri dönmek için Enter'a basın...[/dim]")
        elif choice == "5":
            admin_panel(data)
        elif choice == "6":
            clear_screen()
            console.print(Panel("[bold cyan]👤 ÖĞRENCİ PROFİL BİLGİLERİ[/bold cyan]", expand=False))
            console.print(f"  [bold]Ad Soyad:[/bold] {student.get('full_name')}")
            console.print(f"  [bold]Okul Numarası:[/bold] {student.get('school_number')}")
            console.print(f"  [bold]Gizli Soru:[/bold] {student.get('secret_question')}")
            Prompt.ask("\n[dim]Geri dönmek için Enter'a basın...[/dim]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nÇıkış yapıldı.")
        sys.exit()
