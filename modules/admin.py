from datetime import datetime
from config import PASSWORD_TEACHER, PASSWORD_ADMIN
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from modules.auth import clear_screen, save_data

console = Console()

def admin_panel(data):
    clear_screen()
    console.print(Panel("[bold cyan]🛠️ ÖĞRETMEN / ADMIN GİRİŞİ[/bold cyan]", expand=False))
    
    password = Prompt.ask("[bold yellow]Erişim Şifresi[/bold yellow]", password=True)
    
    role = None
    if password == PASSWORD_ADMIN:
        role = "ADMIN"
    elif password == PASSWORD_TEACHER:
        role = "TEACHER"
    else:
        console.print("\n[bold red][✘] Hatalı şifre! Erişim reddedildi.[/bold red]")
        Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
        return

    while True:
        clear_screen()
        console.print(Panel(f"[bold cyan]YÖNETİM PANELİ[/bold cyan] - Yetki: [bold green]{role}[/bold green]", expand=False))
        
        console.print("  [bold cyan]\[1][/bold cyan] Yeni Duyuru Ekle")
        if role == "ADMIN":
            console.print("  [bold cyan]\[2][/bold cyan] Tüm Duyuruları Temizle")
            console.print("  [bold cyan]\[3][/bold cyan] Öğrenci Bilgilerini Sıfırla")
        console.print("  [bold red]\[0][/bold red] Ana Menüye Dön\n")
        
        choices = ["0", "1"]
        if role == "ADMIN":
            choices.extend(["2", "3"])
            
        choice = Prompt.ask("Seçiminiz", choices=choices)
        
        if choice == "0":
            break
        elif choice == "1":
            title = Prompt.ask("Duyuru Başlığı").strip()
            content = Prompt.ask("Duyuru İçeriği").strip()
            author = "Öğretmen" if role == "TEACHER" else "Admin"
            date_str = datetime.now().strftime("%d.%m.%Y")
            
            new_ann = {
                "id": len(data.get("announcements", [])) + 1,
                "date": date_str,
                "author": author,
                "title": title,
                "content": content
            }
            if "announcements" not in data:
                data["announcements"] = []
            data["announcements"].append(new_ann)
            save_data(data)
            console.print("[bold green][✔] Duyuru başarıyla eklendi.[/bold green]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
            
        elif choice == "2" and role == "ADMIN":
            data["announcements"] = []
            save_data(data)
            console.print("[bold green][✔] Tüm duyurular silindi.[/bold green]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
            
        elif choice == "3" and role == "ADMIN":
            data["student"] = {"full_name": "", "school_number": ""}
            save_data(data)
            console.print("[bold green][✔] Öğrenci profili sıfırlandı. Yeniden başlatmada isim sorulacak.[/bold green]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
