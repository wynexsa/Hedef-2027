import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "lgs_data.json")

# Şifreler
PASSWORD_ADMIN = "W1ndows_LinuX#2026"
PASSWORD_TEACHER = "OrucReis_8C!"

DEFAULT_DATA = {
    "student": {
        "full_name": "",
        "school_number": ""
    },
    "announcements": [],
    "question_logs": {},
    "schedule": {
        "Pazartesi": [
            {"time": "07:20 - 08:50", "lesson": "İnkılap", "teacher": "Ayşenur Temel"},
            {"time": "09:00 - 10:30", "lesson": "Görgütü-8", "teacher": "İlknur Kırmızı"},
            {"time": "10:40 - 12:10", "lesson": "Matematik", "teacher": "Rumeysa Kan"},
            {"time": "12:20 - 13:00", "lesson": "Fen Bilimleri", "teacher": "Şeymanur Güner"}
        ],
        "Salı": [
            {"time": "07:20 - 08:50", "lesson": "Türkçe 2", "teacher": "Büşra Özen"},
            {"time": "09:00 - 10:30", "lesson": "Matematik", "teacher": "Rumeysa Kan"},
            {"time": "10:40 - 12:10", "lesson": "Fen Bilimleri", "teacher": "Şeymanur Güner"},
            {"time": "12:20 - 13:00", "lesson": "Beden Eğitimi", "teacher": "Uğur Yağız Bozkurt"}
        ],
        "Çarşamba": [
            {"time": "07:20 - 08:50", "lesson": "Türkçe 2", "teacher": "Büşra Özen"},
            {"time": "09:00 - 09:40", "lesson": "Rehberlik", "teacher": "Şeymanur Güner"},
            {"time": "09:50 - 11:20", "lesson": "Türk Sosyal H.A", "teacher": "Ayşenur Temel"},
            {"time": "11:30 - 13:00", "lesson": "Din Kültürü", "teacher": "Hatice Akpınar"}
        ],
        "Perşembe": [
            {"time": "07:20 - 08:50", "lesson": "İngilizce 2", "teacher": "Kevser Temel"},
            {"time": "09:00 - 10:30", "lesson": "Türkçe 2", "teacher": "Büşra Özen"},
            {"time": "10:40 - 11:20", "lesson": "Müzik", "teacher": "İlknur Kırmızı"},
            {"time": "11:30 - 13:00", "lesson": "Peyg. Hayatı-8", "teacher": "Hatice Akpınar"}
        ],
        "Cuma": [
            {"time": "07:20 - 08:50", "lesson": "İngilizce 2", "teacher": "Kevser Temel"},
            {"time": "09:00 - 10:30", "lesson": "Teknoloji Tasarım", "teacher": "İlker Mermer"},
            {"time": "10:40 - 12:10", "lesson": "Matematik", "teacher": "Rumeysa Kan"},
            {"time": "12:20 - 13:00", "lesson": "Görsel", "teacher": "Semahat Yabalak"}
        ]
    }
}
