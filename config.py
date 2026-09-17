import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "lgs_data.json")

# Şifre Tanımlamaları
PASSWORD_TEACHER = "OrucReis_8C!"
PASSWORD_ADMIN = "W1ndows_LinuX#2026"

DEFAULT_DATA = {
    "students": [],     
    "teachers": [],      
    "announcements": [], 
    "question_logs": {}  
