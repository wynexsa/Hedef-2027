from datetime import datetime
from config import PASSWORD_ADMIN, PASSWORD_TEACHER
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
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
        if password != PASSWORD_ADMIN:
            console.print("\n[bold red][✘] Hatalı admin şifresi![/bold red]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
            return
        run_admin_menu(data)

def show_registered_students(data):
    clear_screen()
    console.print(Panel("[bold cyan]👥 KAYITLI ÖĞRENCİ BİLGİLERİ[/bold cyan]", expand=False))
    
    student = data.get("student", {})
    full_name = student.get("full_name", "")
    school_number = student.get("school_number", "")
    
    if not full_name:
        console.print("[yellow]Sisteme henüz kayıt olmuş bir öğrenci bulunmuyor.[/yellow]\n")
    else:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Ad Soyad", width=25)
        table.add_column("Okul Numarası", width=15, justify="center")
        table.add_column("Durum", width=15, justify="center")
        
        table.add_row(full_name, school_number if school_number else "---", "[green]Aktif[/green]")
        console.print(table)
        console.print(f"\n[bold green]Toplam Kayıtlı Öğrenci Sayısı:[/bold green] 1")
    
    Prompt.ask("\n[dim]Geri dönmek için Enter'a basın...[/dim]")

def run_teacher_menu(data):
    while True:
        clear_screen()
        console.print(Panel("[bold cyan]ÖĞRETMEN YÖNETİM PANELİ[/bold cyan]", expand=False))
        console.print("  [bold cyan][1][/bold cyan] Duyuru Yayınla")
        console.print("  [bold cyan][2][/bold cyan] Kayıtlı Öğrenciyi Listele")
        console.print("  [bold cyan][3][/bold cyan] Öğrenci Soru Günlüklerini İncele")
        console.print("  [bold red][0][/bold red] Ana Menüye Dön\n")
        
        choice = Prompt.ask("Seçiminiz", choices=["0", "1", "2", "3"])
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
            show_registered_students(data)
        elif choice == "3":
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
        console.print("  [bold cyan][2][/bold cyan] Kayıtlı Öğrenciyi Listele")
        console.print("  [bold cyan][3][/bold cyan] Tüm Duyuruları Temizle")
        console.print("  [bold cyan][4][/bold cyan] Öğrenci Profilini Sıfırla")
        console.print("  [bold cyan][5][/bold cyan] Tüm Soru Günlüklerini Sıfırla")
        console.print("  [bold red][0][/bold red] Ana Menüye Dön\n")
        
        choice = Prompt.ask("Seçiminiz", choices=["0", "1", "2", "3", "4", "5"])
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
            show_registered_students(data)
        elif choice == "3":
            data["announcements"] = []
            save_data(data)
            console.print("[bold green][✔] Tüm duyurular silindi.[/bold green]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
        elif choice == "4":
            data["student"] = {
                "full_name": "",
                "school_number": "",
                "password": "",
                "secret_question": "",
                "secret_answer": ""
            }
            save_data(data)
            console.print("[bold green][✔] Öğrenci profili sıfırlandı.[/bold green]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
        elif choice == "5":
            data["question_logs"] = {}
            save_data(data)
            console.print("[bold green][✔] Tüm soru günlükleri temizlendi.[/bold green]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
