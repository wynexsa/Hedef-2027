import sys
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Modül importları
from modules.auth import load_data, save_data, authenticate_student, clear_screen
from modules.announcements import show_announcements
from modules.admin import admin_panel
from config import PASSWORD_TEACHER, PASSWORD_ADMIN

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

def show_student_notifications(data, current_student):
    clear_screen()
    console.print(Panel("[bold cyan]🔔 BİLDİRİMLERİM[/bold cyan]", expand=False))
    
    students = data.get("students", [])
    target_student = None
    for s in students:
        if s.get("school_number") == current_student.get("school_number"):
            target_student = s
            break
            
    if not target_student:
        console.print("[yellow]Öğrenci bilgisi bulunamadı.[/yellow]")
        Prompt.ask("\n[dim]Geri dönmek için Enter'a basın...[/dim]")
        return
        
    notifications = target_student.get("notifications", [])
    
    if not notifications:
        console.print("[yellow]Henüz size gelen yeni bir bildirim bulunmuyor.[/yellow]\n")
    else:
        has_unread = False
        for notif in notifications:
            if not notif.get("read", False):
                notif["read"] = True
                has_unread = True
                
        if has_unread:
            save_data(data)
            
        for idx, notif in enumerate(notifications, 1):
            console.print(f"[bold green]{idx}. [{notif.get('date')}] - Gönderen: {notif.get('sender')}[/bold green]")
            console.print(f"   💬 {notif.get('content')}\n")
            
    Prompt.ask("[dim]Geri dönmek için Enter'a basın...[/dim]")

def management_login_flow(data):
    clear_screen()
    console.print(Panel("[bold cyan]🔐 ÜST YETKİLİ GİRİŞ EKRANI[/bold cyan]", expand=False))
    
    password = Prompt.ask("[bold yellow]Yetkili Şifresi[/bold yellow]", password=True).strip()
    
    import time
    if password == PASSWORD_TEACHER:
        console.print("\n[bold green][✔] Öğretmen şifresi doğru! Panele yönlendiriliyorsunuz...[/bold green]")
        time.sleep(1)
        admin_panel(data, {"role": "teacher", "user": {"full_name": "Öğretmen"}})
    elif password == PASSWORD_ADMIN:
        console.print("\n[bold green][✔] Admin şifresi doğru! Panele yönlendiriliyorsunuz...[/bold green]")
        time.sleep(1)
        admin_panel(data, {"role": "admin", "user": {"full_name": "Admin"}})
    else:
        console.print("\n[bold red][✘] Hatalı şifre![/bold red]")
        Prompt.ask("\n[dim]Geri dönmek için Enter'a basın...[/dim]")

def edit_student_profile(data, current_student):
    while True:
        clear_screen()
        console.print(Panel("[bold cyan]👤 PROFİL BİLGİLERİ VE DÜZENLEME[/bold cyan]", expand=False))
        console.print(f"  [bold]Ad Soyad:[/bold] {current_student.get('full_name')} [dim](Değiştirilemez)[/dim]")
        console.print(f"  [bold]Okul Numarası:[/bold] {current_student.get('school_number')} [dim](Değiştirilemez)[/dim]")
        console.print(f"  [bold]Gizli Soru:[/bold] {current_student.get('secret_question')}")
        console.print("-" * 50)
        console.print("  [bold cyan][1][/bold cyan] Şifremi Değiştir")
        console.print("  [bold cyan][2][/bold cyan] Gizli Soru ve Cevabını Değiştir")
        console.print("  [bold red][0][/bold red] Geri Dön\n")
        
        choice = Prompt.ask("Seçiminiz", choices=["0", "1", "2"])
        
        if choice == "0":
            break
        elif choice == "1":
            old_pass = Prompt.ask("[bold yellow]Mevcut Şifreniz[/bold yellow]", password=True).strip()
            if old_pass == current_student.get("password"):
                new_pass = Prompt.ask("[bold yellow]Yeni Şifreniz[/bold yellow]", password=True).strip()
                if new_pass:
                    current_student["password"] = new_pass
                    save_data(data)
                    console.print("\n[bold green][✔] Şifreniz başarıyla güncellendi![/bold green]")
                else:
                    console.print("\n[bold red][✘] Şifre boş olamaz![/bold red]")
            else:
                console.print("\n[bold red][✘] Mevcut şifrenizi hatalı girdiniz![/bold red]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
        elif choice == "2":
            password_check = Prompt.ask("[bold yellow]İşlem için mevcut şifrenizi girin[/bold yellow]", password=True).strip()
            if password_check == current_student.get("password"):
                console.print("\n[bold cyan]Yeni Gizli Soru Seçin:[/bold cyan]")
                console.print("  [1] İlk evcil hayvanınızın ismi neydi?")
                console.print("  [2] Çocukluk lakabınız neydi?")
                console.print("  [3] En sevdiğiniz öğretmen kimdi?")
                q_choice = Prompt.ask("Seçiminiz (1-3)", choices=["1", "2", "3"])
                questions_map = {
                    "1": "İlk evcil hayvanınızın ismi neydi?",
                    "2": "Çocukluk lakabınız neydi?",
                    "3": "En sevdiğiniz öğretmen kimdi?"
                }
                current_student["secret_question"] = questions_map[q_choice]
                new_ans = Prompt.ask("[bold yellow]Yeni Gizli Soru Cevabı[/bold yellow]").strip().lower()
                current_student["secret_answer"] = new_ans
                save_data(data)
                console.print("\n[bold green][✔] Gizli soru ve cevabınız güncellendi![/bold green]")
            else:
                console.print("\n[bold red][✘] Hatalı şifre![/bold red]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")

def main():
    while True:
        data = load_data()
        
        current_student_raw = authenticate_student(data)
        if not current_student_raw:
            continue
            
        while True:
            clear_screen()
            data = load_data()
            
            current_student = None
            for s in data.get("students", []):
                if s.get("school_number") == current_student_raw.get("school_number"):
                    current_student = s
                    break
            if not current_student:
                break
                
            notif_count = sum(1 for n in current_student.get("notifications", []) if not n.get("read", False))
            notif_badge = f" [red]({notif_count} Okunmamış)[/red]" if notif_count > 0 else ""
            
            welcome_msg = f"Hoş geldin, [bold cyan]{current_student.get('full_name')}[/bold cyan] (No: {current_student.get('school_number')}) | LGS 2027'ye Kalan: {get_countdown()}"
            console.print(Panel(welcome_msg, title="[bold green]HEDEF 2027 - LGS ASİSTANI[/bold green]", expand=False))
            
            # İstediğin gibi sadeleştirilmiş ve güncellenmiş menü
            console.print("  [bold cyan][1][/bold cyan] 📢 Duyurular")
            console.print(f"  [bold cyan][2][/bold cyan] 🔔 Bildirimlerim{notif_badge}")
            console.print("  [bold cyan][3][/bold cyan] 🔗 LGS Faydalı Linkler")
            console.print("  [bold cyan][4][/bold cyan] 🔐 Üst Yetkili Erişimi")
            console.print("  [bold cyan][5][/bold cyan] 👤 Profil Bilgilerimi Göster / Düzenle")
            console.print("  [bold red][0][/bold red] 🚪 Oturumu Kapat / Çıkış\n")
            
            choice = Prompt.ask("Seçiminiz", choices=["0", "1", "2", "3", "4", "5"])
            
            if choice == "0":
                break 
            elif choice == "1":
                show_announcements(data)
            elif choice == "2":
                show_student_notifications(data, current_student)
            elif choice == "3":
                clear_screen()
                console.print(Panel("[bold cyan]🔗 LGS FAYDALI LİNKLER[/bold cyan]", expand=False))
                console.print("  • Resmi Kaynak & Örnek Sorular: [link=https://odsgm.meb.gov.tr]https://odsgm.meb.gov.tr[/link]")
                console.print("  • MEB Duyurular Portalı: [link=https://www.meb.gov.tr]https://www.meb.gov.tr[/link]")
                console.print("  • TRT Çevrim İçi Eğitim & LGS: [link=https://www.trteba.gov.tr]https://www.trteba.gov.tr[/link]")
                console.print("  • Rehberlik ve Soru Çözüm Videoları: [link=https://www.youtube.com/@tongucakademi]YouTube Tonguç Akademi[/link]\n")
                Prompt.ask("[dim]Geri dönmek için Enter'a basın...[/dim]")
            elif choice == "4":
                management_login_flow(data)
            elif choice == "5":
                edit_student_profile(data, current_student)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nÇıkış yapıldı.")
        sys.exit()
