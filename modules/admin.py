from datetime import datetime
from config import PASSWORD_ADMIN
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from modules.auth import clear_screen, save_data

console = Console()

def admin_panel(data, current_user):
    # Eğer giren kişi öğretmense öğretmen menüsü, adminse admin menüsü açılır
    role = current_user.get("role")
    
    if role == "teacher":
        run_teacher_menu(data, current_user)
    elif role == "admin":
        run_admin_menu(data)

def send_student_recommendation(data, sender_name):
    clear_screen()
    console.print(Panel("[bold cyan]📚 ÖĞRENCİYE KİTAP / ÖNERİ GÖNDER[/bold cyan]", expand=False))
    
    students = data.get("students", [])
    if not students:
        console.print("[yellow]Sisteme kayıtlı öğrenci bulunmuyor.[/yellow]")
        Prompt.ask("\n[dim]Geri dönmek için Enter'a basın...[/dim]")
        return
    
    console.print("[bold]Kayıtlı Öğrenciler:[/bold]\n")
    for idx, s in enumerate(students, 1):
        console.print(f"  [{idx}] {s.get('full_name')} (No: {s.get('school_number')})")
    console.print("  [0] İptal / Geri Dön\n")
    
    choice_str = Prompt.ask("Öneri göndermek istediğiniz öğrencinin numarasını seçin")
    try:
        choice = int(choice_str)
        if choice == 0:
            return
        target_student = students[choice - 1]
    except (ValueError, IndexError):
        console.print("\n[bold red][✘] Geçersiz seçim![/bold red]")
        Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
        return
    
    message = Prompt.ask(f"\n[bold yellow]{target_student.get('full_name')} adlı öğrenciye öneri/bildirim metni[/bold yellow]").strip()
    if message:
        if "notifications" not in target_student:
            target_student["notifications"] = []
        
        date_str = datetime.now().strftime("%d.%m.%Y %H:%M")
        new_notif = {
            "id": int(datetime.now().timestamp()),
            "date": date_str,
            "sender": f"Öğretmen ({sender_name})",
            "content": message,
            "read": False  # Okundu bilgisi başlangıçta False
        }
        target_student["notifications"].append(new_notif)
        save_data(data)
        console.print(f"\n[bold green][✔] Öneri başarıyla {target_student.get('full_name')} adlı öğrenciye gönderildi![/bold green]")
    else:
        console.print("\n[bold red][✘] Mesaj boş olamaz![/bold red]")
    
    Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")

def show_registered_students(data):
    clear_screen()
    console.print(Panel("[bold cyan]👥 KAYITLI ÖĞRENCİ LİSTESİ VE OKUNDU DURUMLARI[/bold cyan]", expand=False))
    
    students = data.get("students", [])
    if not students:
        console.print("[yellow]Sisteme henüz kayıt olmuş bir öğrenci bulunmuyor.[/yellow]\n")
    else:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Ad Soyad", width=22)
        table.add_column("Okul No", width=12, justify="center")
        table.add_column("Bildirim Durumu", width=25, justify="center")
        
        for s in students:
            notifs = s.get("notifications", [])
            total_n = len(notifs)
            unread_n = sum(1 for n in notifs if not n.get("read", False))
            
            if total_n == 0:
                status_str = "[dim]Bildirim yok[/dim]"
            elif unread_n == 0:
                status_str = "[bold green]Tümü Okundu (✔✔)[/bold green]"
            else:
                status_str = f"[bold yellow]{unread_n} okunmamış var[/bold yellow]"
                
            table.add_row(s.get("full_name"), s.get("school_number"), status_str)
            
        console.print(table)
        console.print(f"\n[bold green]Toplam Kayıtlı Öğrenci Sayısı:[/bold green] {len(students)}")
    
    Prompt.ask("\n[dim]Geri dönmek için Enter'a basın...[/dim]")

def run_teacher_menu(data, teacher_user):
    teacher_name = teacher_user.get("full_name", "Öğretmen")
    while True:
        clear_screen()
        console.print(Panel(f"[bold cyan]ÖĞRETMEN YÖNETİM PANELİ ({teacher_name})[/bold cyan]", expand=False))
        console.print("  [bold cyan][1][/bold cyan] Duyuru Yayınla")
        console.print("  [bold cyan][2][/bold cyan] Kayıtlı Öğrencileri Listele ve Okundu Takibi Yap")
        console.print("  [bold cyan][3][/bold cyan] Öğrenciye Kitap / Öneri Gönder")
        console.print("  [bold cyan][4][/bold cyan] Öğrenci Soru Günlüklerini İncele")
        console.print("  [bold red][0][/bold red] Oturumu Kapat / Ana Menüye Dön\n")
        
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
                "author": f"Öğretmen ({teacher_name})",
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
            send_student_recommendation(data, teacher_name)
        elif choice == "4":
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
        console.print("  [bold cyan][1][/bold cyan] Kayıtlı Öğrencileri Listele")
        console.print("  [bold cyan][2][/bold cyan] Tüm Duyuruları Temizle")
        console.print("  [bold cyan][3][/bold cyan] Tüm Öğrenci Listesini Sıfırla")
        console.print("  [bold red][0][/bold red] Oturumu Kapat / Ana Menüye Dön\n")
        
        choice = Prompt.ask("Seçiminiz", choices=["0", "1", "2", "3"])
        if choice == "0":
            break
        elif choice == "1":
            show_registered_students(data)
        elif choice == "2":
            data["announcements"] = []
            save_data(data)
            console.print("[bold green][✔] Tüm duyurular silindi.[/bold green]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
        elif choice == "3":
            confirm = Prompt.ask("Tüm öğrenciler silinecek! Emin misiniz? (E/H)", choices=["E", "H", "e", "h"])
            if confirm.lower() == "e":
                data["students"] = []
                save_data(data)
                console.print("[bold green][✔] Öğrenci listesi sıfırlandı.[/bold green]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
