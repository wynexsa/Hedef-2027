from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from modules.auth import clear_screen

console = Console()

EXAM_CONFIG = [
    ("Türkçe", 20),
    ("Matematik", 20),
    ("Fen Bilimleri", 20),
    ("T.C. İnkılap Tarihi", 10),
    ("Din Kültürü", 10),
    ("Yabancı Dil (İngilizce)", 10)
]

def calculate_nets():
    clear_screen()
    console.print(Panel("[bold cyan]⚡ HIZLI DENEME NET HESAPLAYICI (LGS)[/bold cyan]", expand=False))
    console.print("[dim]Formül: Net = Doğru - (Yanlış / 3)[/dim]\n")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Ders", width=24)
    table.add_column("Doğru", justify="right", width=8)
    table.add_column("Yanlış", justify="right", width=8)
    table.add_column("Boş", justify="right", width=8)
    table.add_column("Net", justify="right", width=10, style="bold green")

    total_net = 0.0
    total_correct = 0
    total_wrong = 0
    total_empty = 0

    for lesson, max_q in EXAM_CONFIG:
        console.print(f"[bold yellow]--- {lesson} (Toplam {max_q} Soru) ---[/bold yellow]")
        
        while True:
            try:
                c = int(Prompt.ask("  Doğru sayısı", default="0"))
                w = int(Prompt.ask("  Yanlış sayısı", default="0"))
                if c < 0 or w < 0 or (c + w) > max_q:
                    console.print(f"  [bold red]Hata: Doğru + Yanlış en fazla {max_q} olabilir![/bold red]")
                    continue
                break
            except ValueError:
                console.print("  [bold red]Lütfen geçerli bir sayı girin.[/bold red]")

        e = max_q - (c + w)
        net = max(0.0, c - (w / 3.0))
        
        total_correct += c
        total_wrong += w
        total_empty += e
        total_net += net

        table.add_row(lesson, str(c), str(w), str(e), f"{net:.2f}")

    clear_screen()
    console.print(Panel("[bold cyan]DENEME SINAVI SONUÇ HARİTASI[/bold cyan]", expand=False))
    console.print(table)
    
    console.print(f"\n[bold white]Toplam Doğru:[/bold white] {total_correct} | [bold white]Toplam Yanlış:[/bold white] {total_wrong} | [bold white]Toplam Boş:[/bold white] {total_empty}")
    console.print(f"[bold cyan]TOPLAM LGS NETİ:[/bold cyan] [bold green]{total_net:.2f} / 90.00[/bold green]")

    Prompt.ask("\n[dim]Ana menüye dönmek için Enter'a basın...[/dim]")
