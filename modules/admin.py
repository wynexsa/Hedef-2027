from datetime import datetime
from config import ADMIN_PASSWORD, PASSWORD_TEACHER
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from modules.auth import clear_screen, save_data

console = Console()

def admin_panel(data):
    clear_screen()
    console.print(Panel("[bold cyan]🔐 YETKİLİ GİRİŞ EKRANI[/bold cyan]", expand=False))
    
    console.print("  [bold cyan][1][/bold cyan] Öğretmen Girişi")
    console.print("  [bold cyan][2][/bold cyan] Admin Girişi")
    console.print("  [bold red][0][/bold red] Geri Dön\n")
    
    choice = Prompt.ask("Seçiminiz", choices=["0", "1", "2"])
    
    if choice == "0":
        return
    elif choice == "1":
        password = Prompt.ask("[bold yellow]Öğretmen Şifresi[/bold yellow]", password=True)
        if password != PASSWORD_TEACHER:
            console.print("\n[bold red][✘] Hatalı öğretmen şifresi![/bold red]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
            return
        run_teacher_menu(data)
    elif choice == "2":
        password = Prompt.ask("[bold yellow]Admin Şifresi[/bold yellow]", password=True)
        if password != ADMIN_PASSWORD:
            console.print("\n[bold red][✘] Hatalı admin şifresi![/bold red]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
            return
        run_admin_menu(data)

def run_teacher_menu(data):
    while True:
        clear_screen()
        console.print(Panel("[bold cyan]öğretmen YÖNETİM PANELİ[/bold cyan]", expand=False))
        console.print("  [bold cyan][1][/bold cyan] Duyuru Yayınla")
        console.print("  [bold cyan][2][/bold cyan] Öğrenci Soru Günlüklerini İncele")
        console.print("  [bold red][0][/bold red] Ana Menüye Dön\n")
        
        choice = Prompt.ask("Seçiminiz", choices=["0", "1", "2"])
        if choice == "0":
            break
        elif choice == "1":
            title = Prompt.ask("Duyuru Başlığı").strip()
            content = Prompt.ask("Duyuru İçeriği").strip()
            date_str = datetime.now().strftime("%d.%m.%Y")
            
            new_ann = {
                "id": len(data.get("announcements", [])) + 1,
                "date": date_str,
                "author": "Öğretmen",
                "title": title,
                "content": content
            }
            if "announcements" not in data:
                data["announcements"] = []
            data["announcements"].append(new_ann)
            save_data(data)
            console.print("[bold green][✔] Duyuru başarıyla yayınlandı.[/bold green]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
        elif choice == "2":
            clear_screen()
            console.print(Panel("[bold cyan]ÖĞRENCİ SORU GÜNLÜKLERİ[/bold cyan]", expand=False))
            logs = data.get("question_logs", {})
            if not logs:
                console.print("[yellow]Henüz kaydedilmiş soru günlüğü bulunmuyor.[/yellow]")
            else:
                for date_k, l_data in logs.items():
                    console.print(f"[bold yellow]Tarih: {date_k}[/bold yellow]")
                    for les, count in l_data.items():
                        console.print(f"  - {les}: {count} soru")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")

def run_admin_menu(data):
    while True:
        clear_screen()
        console.print(Panel("[bold cyan]👑 TAM YETKİLİ ADMIN PANELİ[/bold cyan]", expand=False))
        console.print("  [bold cyan][1][/bold cyan] Duyuru Ekle")
        console.print("  [bold cyan][2][/bold cyan] Tüm Duyuruları Temizle")
        console.print("  [bold cyan][3][/bold cyan] Öğrenci Profilini Sıfırla")
        console.print("  [bold cyan][4][/bold cyan] Tüm Soru Günlüklerini Sıfırla")
        console.print("  [bold red][0][/bold red] Ana Menüye Dön\n")
        
        choice = Prompt.ask("Seçiminiz", choices=["0", "1", "2", "3", "4"])
        if choice == "0":
            break
        elif choice == "1":
            title = Prompt.ask("Duyuru Başlığı").strip()
            content = Prompt.ask("Duyuru İçeriği").strip()
            date_str = datetime.now().strftime("%d.%m.%Y")
            
            new_ann = {
                "id": len(data.get("announcements", [])) + 1,
                "date": date_str,
                "author": "Admin",
                "title": title,
                "content": content
            }
            if "announcements" not in data:
                data["announcements"] = []
            data["announcements"].append(new_ann)
            save_data(data)
            console.print("[bold green][✔] Duyuru başarıyla eklendi.[/bold green]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
        elif choice == "2":
            data["announcements"] = []
            save_data(data)
            console.print("[bold green][✔] Tüm duyurular silindi.[/bold green]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
        elif choice == "3":
            data["student"] = {"full_name": "", "school_number": ""}
            save_data(data)
            console.print("[bold green][✔] Öğrenci profili sıfırlandı.[/bold green]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
        elif choice == "4":
            data["question_logs"] = {}
            save_data(data)
            console.print("[bold green][✔] Tüm soru günlükleri temizlendi.[/bold green]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
