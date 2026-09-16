import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "lgs_data.json")

# Sistem Admin Şifresi
PASSWORD_ADMIN = "W1ndows_LinuX#2026"

DEFAULT_DATA = {
    "students": [],      # Birden fazla öğrencinin tutulacağı liste
    "teachers": [],      # Kayıt olan öğretmenlerin tutulacağı liste
    "announcements": [],
    "question_logs": {}
}
