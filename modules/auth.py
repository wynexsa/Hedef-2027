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

def authenticate_user(data):
    """
    Sisteme ilk girişte veya açılışta çalışır. 
    Öğrenci/Öğretmen kayıt yönetimi ve giriş işlemlerini yönetir.
    """
    while True:
        clear_screen()
        console.print(Panel("[bold cyan]HEDEF 2027 - GİRİŞ VE KAYIT SİSTEMİ[/bold cyan]", expand=False))
        
        students = data.get("students", [])
        teachers = data.get("teachers", [])
        
        # Eğer hiç kayıtlı kullanıcı yoksa önce kayıt olmaya yönlendir
        if not students and not teachers:
            console.print("[yellow]Sistemde kayıtlı kullanıcı bulunamadı. Lütfen ilk kaydı oluşturun.[/yellow]\n")
            console.print("  [bold cyan][1][/bold cyan] Öğrenci Kaydı Ol")
            console.print("  [bold cyan][2][/bold cyan] Öğretmen Kaydı Ol")
            console.print("  [bold red][0][/bold red] Çıkış\n")
            
            choice = Prompt.ask("Seçiminiz", choices=["0", "1", "2"])
            if choice == "0":
                exit()
            elif choice == "1":
                register_student(data)
                continue
            elif choice == "2":
                register_teacher(data)
                continue

        console.print("  [bold cyan][1][/bold cyan] Öğrenci Girişi")
        console.print("  [bold cyan][2][/bold cyan] Öğretmen Girişi")
        console.print("  [bold cyan][3][/bold cyan] Yeni Öğrenci Kaydı Ol")
        console.print("  [bold cyan][4][/bold cyan] Yeni Öğretmen Kaydı Ol")
        console.print("  [bold cyan][5][/bold cyan] Şifremi Unuttum (Öğrenci)")
        console.print("  [bold red][0][/bold red] Çıkış\n")
        
        choice = Prompt.ask("Seçiminiz", choices=["0", "1", "2", "3", "4", "5"])
        
        if choice == "0":
            exit()
        elif choice == "1":
            # Öğrenci Girişi
            if not students:
                console.print("\n[bold red][✘] Kayıtlı öğrenci bulunmuyor![/bold red]")
                time.sleep(1)
                continue
            
            school_num = Prompt.ask("[bold yellow]Okul Numaranız[/bold yellow]").strip()
            password = Prompt.ask("[bold yellow]Şifreniz[/bold yellow]", password=True).strip()
            
            found_student = None
            for s in students:
                if s.get("school_number") == school_num and s.get("password") == password:
                    found_student = s
                    break
            
            if found_student:
                console.print(f"\n[bold green]Giriş başarılı! Hoş geldin, {found_student.get('full_name')}.[/bold green]")
                time.sleep(1)
                return {"role": "student", "user": found_student}
            else:
                console.print("\n[bold red][✘] Hatalı okul numarası veya şifre![/bold red]")
                Prompt.ask("\n[dim]Tekrar denemek için Enter'a basın...[/dim]")
                
        elif choice == "2":
            # Öğretmen Girişi
            if not teachers:
                console.print("\n[bold red][✘] Kayıtlı öğretmen bulunmuyor. Lütfen önce öğretmen kaydı oluşturun![/bold red]")
                time.sleep(1)
                continue
            
            username = Prompt.ask("[bold yellow]Öğretmen Kullanıcı Adı / Adı[/bold yellow]").strip()
            password = Prompt.ask("[bold yellow]Şifreniz[/bold yellow]", password=True).strip()
            
            found_teacher = None
            for t in teachers:
                if t.get("username") == username and t.get("password") == password:
                    found_teacher = t
                    break
            
            if found_teacher:
                console.print(f"\n[bold green]Giriş başarılı! Hoş geldiniz, {found_teacher.get('full_name')} Öğretmenim.[/bold green]")
                time.sleep(1)
                return {"role": "teacher", "user": found_teacher}
            else:
                console.print("\n[bold red][✘] Hatalı kullanıcı adı veya şifre![/bold red]")
                Prompt.ask("\n[dim]Tekrar denemek için Enter'a basın...[/dim]")
                
        elif choice == "3":
            register_student(data)
        elif choice == "4":
            register_teacher(data)
        elif choice == "5":
            student_forgot_password(data)

def register_student(data):
    while True:
        clear_screen()
        console.print(Panel("[bold cyan]HEDEF 2027 - ÖĞRENCİ KAYIT SİSTEMİ[/bold cyan]", expand=False))
        full_name = Prompt.ask("[bold yellow]Adınız Soyadınız[/bold yellow]").strip()
        school_num = Prompt.ask("[bold yellow]Okul Numaranız[/bold yellow]").strip()
        
        # Numara çakışması kontrolü
        if any(s.get("school_number") == school_num for s in data.get("students", [])):
            console.print("\n[bold red][✘] Bu okul numarası ile zaten bir kayıt var![/bold red]")
            Prompt.ask("\n[dim]Tekrar denemek için Enter'a basın...[/dim]")
            return

        password = Prompt.ask("[bold yellow]Şifreniz[/bold yellow]", password=True).strip()
        
        console.print("\n[bold cyan]Lütfen bir gizli soru seçin (Şifre sıfırlamak için):[/bold cyan]")
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
        secret_answer = Prompt.ask(f"[bold yellow]Gizli Soru Cevabı[/bold yellow]").strip().lower()
        
        if full_name and school_num and password and secret_answer:
            new_student = {
                "full_name": full_name,
                "school_number": school_num,
                "password": password,
                "secret_question": selected_question,
                "secret_answer": secret_answer,
                "notifications": []
            }
            if "students" not in data:
                data["students"] = []
            data["students"].append(new_student)
            save_data(data)
            console.print(f"\n[bold green][✔] Öğrenci kaydı başarıyla tamamlandı. Hoş geldin, {full_name}![/bold green]")
            Prompt.ask("\n[dim]Giriş ekranına dönmek için Enter'a basın...[/dim]")
            break
        else:
            console.print("\n[bold red][✘] Tüm alanları eksiksiz doldurmalısınız![/bold red]")
            Prompt.ask("\n[dim]Tekrar denemek için Enter'a basın...[/dim]")

def register_teacher(data):
    while True:
        clear_screen()
        console.print(Panel("[bold cyan]HEDEF 2027 - ÖĞRETMEN KAYIT SİSTEMİ[/bold cyan]", expand=False))
        full_name = Prompt.ask("[bold yellow]Ad Soyad (Örn: Ayşenur Temel)[/bold yellow]").strip()
        username = Prompt.ask("[bold yellow]Kullanıcı Adınız (Giriş için)[/bold yellow]").strip()
        
        if any(t.get("username") == username for t in data.get("teachers", [])):
            console.print("\n[bold red][✘] Bu kullanıcı adı zaten kullanımda![/bold red]")
            Prompt.ask("\n[dim]Tekrar denemek için Enter'a basın...[/dim]")
            return

        password = Prompt.ask("[bold yellow]Şifreniz[/bold yellow]", password=True).strip()
        
        if full_name and username and password:
            new_teacher = {
                "full_name": full_name,
                "username": username,
                "password": password
            }
            if "teachers" not in data:
                data["teachers"] = []
            data["teachers"].append(new_teacher)
            save_data(data)
            console.print(f"\n[bold green][✔] Öğretmen kaydı başarıyla tamamlandı. Hoş geldiniz, {full_name}![/bold green]")
            Prompt.ask("\n[dim]Giriş ekranına dönmek için Enter'a basın...[/dim]")
            break
        else:
            console.print("\n[bold red][✘] Tüm alanları eksiksiz doldurmalısınız![/bold red]")
            Prompt.ask("\n[dim]Tekrar denemek için Enter'a basın...[/dim]")

def student_forgot_password(data):
    clear_screen()
    console.print(Panel("[bold cyan]ŞİFRE SIFIRLAMA MERKEZİ[/bold cyan]", expand=False))
    school_num = Prompt.ask("[bold yellow]Okul Numaranız[/bold yellow]").strip()
    
    students = data.get("students", [])
    target_student = None
    for s in students:
        if s.get("school_number") == school_num:
            target_student = s
            break
            
    if not target_student:
        console.print("\n[bold red][✘] Bu okul numarasına ait kayıtlı öğrenci bulunamadı![/bold red]")
        Prompt.ask("\n[dim]Geri dönmek için Enter'a basın...[/dim]")
        return
        
    console.print(f"Gizli Soru: [bold yellow]{target_student.get('secret_question')}[/bold yellow]")
    ans = Prompt.ask("Gizli Soru Cevabınız").strip().lower()
    
    if ans == target_student.get("secret_answer"):
        console.print("\n[bold green][✔] Cevap doğru! Yeni şifrenizi belirleyebilirsiniz.[/bold green]")
        new_pass = Prompt.ask("[bold yellow]Yeni Şifreniz[/bold yellow]", password=True).strip()
        if new_pass:
            target_student["password"] = new_pass
            save_data(data)
            console.print("\n[bold green][✔] Şifreniz başarıyla güncellendi! Yeni şifrenizle giriş yapabilirsiniz.[/bold green]")
        else:
            console.print("\n[bold red][✘] Şifre boş olamaz![/bold red]")
    else:
        console.print("\n[bold red][✘] Gizli soru cevabı yanlış! Şifre sıfırlanamadı.[/bold red]")
    Prompt.ask("\n[dim]Geri dönmek için Enter'a basın...[/dim]")
