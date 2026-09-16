from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from modules.auth import load_data, save_data, clear_screen

console = Console()

def track_questions(data):
    while True:
        clear_screen()
        console.print(Panel("[bold cyan]✍️ SORU GÜNLÜĞÜ VE TAKİP[/bold cyan]", expand=False))
        
        console.print("  [bold cyan][1][/bold cyan] Bugün Soru Girişi Yap")
        console.print("  [bold cyan][2][/bold cyan] Geçmiş Soru Günlüklerini Görüntüle")
        console.print("  [bold red][0][/bold red] Geri Dön\n")
        
        choice = Prompt.ask("Seçiminiz", choices=["0", "1", "2"])
        
        if choice == "0":
            break
        elif choice == "1":
            clear_screen()
            console.print(Panel("[bold cyan]GÜNLÜK SORU GİRİŞİ[/bold cyan]", expand=False))
            
            date_str = datetime.now().strftime("%d.%m.%Y")
            lessons = ["Türkçe", "Matematik", "Fen Bilimleri", "İnkılap", "Din Kültürü", "İngilizce"]
            
            if "question_logs" not in data:
                data["question_logs"] = {}
            if date_str not in data["question_logs"]:
                data["question_logs"][date_str] = {}
                
            for lesson in lessons:
                count_str = Prompt.ask(f"[yellow]{lesson}[/yellow] dersinden çözülen soru sayısı", default="0")
                try:
                    count = int(count_str)
                except ValueError:
                    count = 0
                data["question_logs"][date_str][lesson] = data["question_logs"][date_str].get(lesson, 0) + count
                
            save_data(data)
            console.print("\n[bold green][✔] Soru günlüğün başarıyla kaydedildi![/bold green]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
            
        elif choice == "2":
            clear_screen()
            console.print(Panel("[bold cyan]📊 GEÇMİŞ SORU GÜNLÜKLERİ[/bold cyan]", expand=False))
            logs = data.get("question_logs", {})
            
            if not logs:
                console.print("[yellow]Henüz kaydedilmiş soru günlüğü bulunmuyor.[/yellow]")
            else:
                for date_k, l_data in logs.items():
                    console.print(f"[bold yellow]Tarih: {date_k}[/bold yellow]")
                    total_daily = 0
                    for les, count in l_data.items():
                        console.print(f"  • {les}: [cyan]{count}[/cyan] soru")
                        total_daily += count
                    console.print(f"  [bold green]Günlük Toplam:[/bold green] {total_daily} soru\n")
                    
            Prompt.ask("\n[dim]Geri dönmek için Enter'a basın...[/dim]")
