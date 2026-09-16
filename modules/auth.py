import json
import os
import time
from config import DATA_FILE, DEFAULT_DATA
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_DATA

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def check_first_run(data):
    student = data.get("student", {})
    
    # Eğer kayıtlı öğrenci yoksa kayıt ekranını çalıştır
    if not student.get("full_name") or not student.get("password"):
        while True:
            clear_screen()
            console.print(Panel("[bold cyan]HEDEF 2027 - ÖĞRENCİ KAYIT SİSTEMİ[/bold cyan]", expand=False))
            full_name = Prompt.ask("[bold yellow]Adınız Soyadınız[/bold yellow]").strip()
            school_num = Prompt.ask("[bold yellow]Okul Numaranız[/bold yellow]").strip()
            password = Prompt.ask("[bold yellow]Şifreniz[/bold yellow]", password=True).strip()
            
            console.print("\n[bold cyan]Lütfen bir gizli soru seçin:[/bold cyan]")
            console.print("  [1] İlk evcil hayvanınızın ismi neydi?")
            console.print("  [2] Çocukluk lakabınız neydi?")
            console.print("  [3] En sevdiğiniz öğretmen kimdi?")
            
            q_choice = Prompt.ask("Seçiminiz (1-3)", choices=["1", "2", "3"])
            questions_map = {
                "1": "İlk evcil hayvanınızın ismi neydi?",
                "2": "Çocukluk lakabınız neydi?",
                "3": "En sevdiğiniz öğretmen kimdi?"
            }
            selected_question = questions_map[q_choice]
            
            secret_answer = Prompt.ask(f"[bold yellow]Gizli Soru Cevabı ({selected_question})[/bold yellow]").strip().lower()
            
            if full_name and school_num and password and secret_answer:
                data["student"] = {
                    "full_name": full_name,
                    "school_number": school_num,
                    "password": password,
                    "secret_question": selected_question,
                    "secret_answer": secret_answer
                }
                save_data(data)
                console.print(f"\n[bold green][✔] Kayıt başarıyla tamamlandı. Hoş geldin, {full_name}![/bold green]")
                Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
                break
            else:
                console.print("\n[bold red][✘] Tüm alanları eksiksiz doldurmalısınız![/bold red]")
                Prompt.ask("\n[dim]Tekrar denemek için Enter'a basın...[/dim]")
    
    # Giriş / Şifre Sıfırlama Döngüsü
    while True:
        # Verileri her döngüde güncel okuyalım ki şifre değiştiğinde anında yansısın
        current_data = load_data()
        student = current_data.get("student", {})

        clear_screen()
        console.print(Panel("[bold cyan]HEDEF 2027 - ÖĞRENCİ GİRİŞİ[/bold cyan]", expand=False))
        console.print("  [bold cyan][1][/bold cyan] Giriş Yap")
        console.print("  [bold cyan][2][/bold cyan] Şifremi Unuttum / Sıfırla")
        console.print("  [bold red][0][/bold red] Çıkış\n")
        
        choice = Prompt.ask("Seçiminiz", choices=["0", "1", "2"])
        
        if choice == "0":
            exit()
        elif choice == "1":
            entered_pass = Prompt.ask("[bold yellow]Şifreniz[/bold yellow]", password=True).strip()
            if entered_pass == student.get("password"):
                console.print(f"\n[bold green]Giriş başarılı! Hoş geldin, {student.get('full_name')}.[/bold green]")
                time.sleep(1)
                break
            else:
                console.print("\n[bold red][✘] Hatalı şifre![/bold red]")
                Prompt.ask("\n[dim]Tekrar denemek için Enter'a basın...[/dim]")
        elif choice == "2":
            clear_screen()
            console.print(Panel("[bold cyan]ŞİFRE SIFIRLAMA MERKEZİ[/bold cyan]", expand=False))
            
            if not student.get("secret_question"):
                console.print("[red]Kayıtlı gizli soru bulunamadı![/red]")
                Prompt.ask("\n[dim]Geri dönmek için Enter'a basın...[/dim]")
                continue

            console.print(f"Kayıtlı Gizli Soru: [bold yellow]{student.get('secret_question')}[/bold yellow]")
            ans = Prompt.ask("Gizli Soru Cevabınız").strip().lower()
            
            if ans == student.get("secret_answer"):
                console.print("\n[bold green][✔] Cevap doğru! Yeni şifrenizi belirleyebilirsiniz.[/bold green]")
                new_pass = Prompt.ask("[bold yellow]Yeni Şifreniz[/bold yellow]", password=True).strip()
                if new_pass:
                    current_data["student"]["password"] = new_pass
                    save_data(current_data)
                    data["student"]["password"] = new_pass
                    console.print("\n[bold green][✔] Şifreniz başarıyla güncellendi! Yeni şifrenizle giriş yapabilirsiniz.[/bold green]")
                else:
                    console.print("\n[bold red][✘] Şifre boş olamaz, sıfırlama iptal edildi.[/bold red]")
            else:
                console.print("\n[bold red][✘] Gizli soru cevabı yanlış! Şifre sıfırlanamadı.[/bold red]")
            Prompt.ask("\n[dim]Devam etmek için Enter'a basın...[/dim]")
