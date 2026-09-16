import sys
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Modül importları
from modules.auth import load_data, save_data, authenticate_user, clear_screen
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

def show_student_notifications(data, current_student):
    clear_screen()
    console.print(Panel("[bold cyan]🔔 BİLDİRİMLERİM[/bold cyan]", expand=False))
    
    # Güncel öğrenci verisini listeden bulalım
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
        # Bildirimleri listele ve okundu olarak işaretle (yeni mesaj oluşturmadan statü güncellenir)
        has_unread = False
        for notif in notifications:
            if not notif.get("read", False):
                notif["read"] = True
                has_unread =ophagy = True
                
        if has_unread:
            save_data(data) # Okundu işaretlemelerini kaydet
            
        for idx, notif in enumerate(notifications, 1):
            console.print(f"[bold green]{idx}. [{notif.get('date')}] - Gönderen: {notif.get('sender')}[/bold green]")
            console.print(f"   💬 {notif.get('content')}\n")
            
    Prompt.ask("[dim]Geri dönmek için Enter'a basın...[/dim]")

def main():
    while True:
        data = load_data()
        
        # Giriş / Kayıt Ekranı Yönlendirmesi
        auth_result = authenticate_user(data)
        role = auth_result.get("role")
        user = auth_result.get("user")
        
        if role == "teacher":
            # Öğretmen doğrudan öğretmen paneline girer
            admin_panel(data, {"role": "teacher", "user": user})
        elif role == "student":
            # Öğrenci ana menüsüne girer
            while True:
                clear_screen()
                data = load_data()
                
                # Güncel öğrenci verisini çek (Bildirim sayısını taze tutmak için)
                current_student = None
                for s in data.get("students", []):
                    if s.get("school_number") == user.get("school_number"):
                        current_student = s
                        break
                if not current_student:
                    break
                    
                notif_count = sum(1 for n in current_student.get("notifications", []) if not n.get("read", False))
                notif_badge = f" [red]({notif_count} Okunmamış)[/red]" if notif_count > 0 else ""
                
                welcome_msg = f"Hoş geldin, [bold cyan]{current_student.get('full_name')}[/bold cyan] (No: {current_student.get('school_number')}) | LGS 2027'ye Kalan: {get_countdown()}"
                console.print(Panel(welcome_msg, title="[bold green]HEDEF 2027 - LGS ASİSTANI[/bold green]", expand=False))
                
                # Sadeleştirilmiş Menü (Sadece "Bildirimlerim")
                console.print("  [bold cyan][1][/bold cyan] 📢 Duyurular")
                console.print(f"  [bold cyan][2][/bold cyan] 🔔 Bildirimlerim{notif_badge}")
                console.print("  [bold cyan][3][/bold cyan] ✍️ Soru Günlüğü ve Takip")
                console.print("  [bold cyan][4][/bold cyan] 🔗 LGS Faydalı Linkler")
                console.print("  [bold cyan][5][/bold cyan] 👤 Profil Bilgilerimi Göster")
                console.print("  [bold red][0][/bold red] 🚪 Oturumu Kapat / Çıkış\n")
                
                choice = Prompt.ask("Seçiminiz", choices=["0", "1", "2", "3", "4", "5"])
                
                if choice == "0":
                    break # Ana giriş ekranına geri döner
                elif choice == "1":
                    show_announcements(data)
                elif choice == "2":
                    show_student_notifications(data, current_student)
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
                    clear_screen()
                    console.print(Panel("[bold cyan]👤 ÖĞRENCİ PROFİL BİLGİLERİ[/bold cyan]", expand=False))
                    console.print(f"  [bold]Ad Soyad:[/bold] {current_student.get('full_name')}")
                    console.print(f"  [bold]Okul Numarası:[/bold] {current_student.get('school_number')}")
                    console.print(f"  [bold]Gizli Soru:[/bold] {current_student.get('secret_question')}")
                    Prompt.ask("\n[dim]Geri dönmek için Enter'a basın...[/dim]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nÇıkış yapıldı.")
        sys.exit()
