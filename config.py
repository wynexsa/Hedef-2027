import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "lgs_data.json")

# Şifreler
PASSWORD_ADMIN = "W1ndows_LinuX#2026"
PASSWORD_TEACHER = "OrucReis_8C!"

DEFAULT_DATA = {
    "student": {
        "full_name": "",
        "school_number": "",
        "password": "",
        "secret_question": "",
        "secret_answer": "",
        "notifications": []  
    },
    "announcements": [],
    "question_logs": {}
}
