from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from modules.auth import clear_screen

console = Console()

def show_announcements(data):
    clear_screen()
    console.print(Panel("[bold cyan]📢 SINIF DUYURULARI[/bold cyan]", expand=False))
    
    announcements = data.get("announcements", [])
    
    if not announcements:
        console.print("[yellow]Henüz yayınlanmış bir duyuru bulunmuyor.[/yellow]")
    else:
        for item in reversed(announcements):
            title = item.get("title", "Duyuru")
            date = item.get("date", "")
            author = item.get("author", "Yönetim")
            content = item.get("content", "")
            
            card = f"[bold yellow]{title}[/bold yellow]  [dim]({date} - {author})[/dim]\n\n{content}"
            console.print(Panel(card, expand=False))

    Prompt.ask("\n[dim]Ana menüye dönmek için Enter'a basın...[/dim]")

def show_links():
    clear_screen()
    console.print(Panel("[bold cyan]🔗 FAYDALI LGS LİNKLERİ[/bold cyan]", expand=False))
    
    links = [
        ("MEB ÖDS (Örnek Sorular)", "https://ods.meb.gov.tr"),
        ("MEB LGS Ana Sayfası", "https://www.meb.gov.tr"),
        ("EBA (Eğitim Bilişim Ağı)", "https://www.eba.gov.tr"),
        ("OGM Materyal", "https://ogmmateryal.eba.gov.tr")
    ]
    
    for idx, (name, url) in enumerate(links, 1):
        console.print(f"  [bold cyan]\[{idx}][/bold cyan] [bold white]{name}:[/bold white] [underline blue]{url}[/underline blue]")
        
    Prompt.ask("\n[dim]Ana menüye dönmek için Enter'a basın...[/dim]")
