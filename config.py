import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "lgs_data.json")

# Yetkilendirme Şifreleri
PASSWORD_TEACHER = "OrucReis_8C!"
PASSWORD_ADMIN = "W1ndows_LinuX#2026"

DEFAULT_DATA = {
    "student": {
        "full_name": "",
        "school_number": ""
    },
    "announcements": [
        {
            "id": 1,
            "date": "16.09.2026",
            "author": "Sistem",
            "title": "Hoş Geldiniz",
            "content": "Hedef 2027 LGS Takip Asistanı kullanıma hazırdır."
        }
    ],
    "question_logs": {},
    "schedule": {
        "Pazartesi": [
            {"time": "07:20 - 08:00", "lesson": "Türkçe", "teacher": "Büşra Özen"},
            {"time": "08:10 - 08:50", "lesson": "Türkçe", "teacher": "Büşra Özen"},
            {"time": "09:00 - 09:40", "lesson": "Matematik", "teacher": "Ahmet Yılmaz"},
            {"time": "09:50 - 10:30", "lesson": "Matematik", "teacher": "Ahmet Yılmaz"},
            {"time": "10:40 - 11:20", "lesson": "Fen Bilimleri", "teacher": "Mehmet Demir"},
            {"time": "11:30 - 12:10", "lesson": "Fen Bilimleri", "teacher": "Mehmet Demir"},
            {"time": "12:20 - 13:00", "lesson": "İngilizce", "teacher": "Ayşe Kaya"}
        ],
        "Salı": [
            {"time": "07:20 - 08:00", "lesson": "Matematik", "teacher": "Ahmet Yılmaz"},
            {"time": "08:10 - 08:50", "lesson": "Matematik", "teacher": "Ahmet Yılmaz"},
            {"time": "09:00 - 09:40", "lesson": "Türkçe", "teacher": "Büşra Özen"},
            {"time": "09:50 - 10:30", "lesson": "İnkılap Tarihi", "teacher": "Ayşenur Temel"},
            {"time": "10:40 - 11:20", "lesson": "İnkılap Tarihi", "teacher": "Ayşenur Temel"},
            {"time": "11:30 - 12:10", "lesson": "Din Kültürü", "teacher": "Hatice Akpınar"},
            {"time": "12:20 - 13:00", "lesson": "Din Kültürü", "teacher": "Hatice Akpınar"}
        ],
        "Çarşamba": [
            {"time": "07:20 - 08:00", "lesson": "Türkçe", "teacher": "Büşra Özen"},
            {"time": "08:10 - 08:50", "lesson": "Türkçe", "teacher": "Büşra Özen"},
            {"time": "09:00 - 09:40", "lesson": "Rehberlik", "teacher": "Şeymanur Güner"},
            {"time": "09:50 - 10:30", "lesson": "Türk Sosyal Hayatı", "teacher": "Ayşenur Temel"},
            {"time": "10:40 - 11:20", "lesson": "Din Kültürü", "teacher": "Hatice Akpınar"},
            {"time": "11:30 - 12:10", "lesson": "Boş / Etkinlik", "teacher": "-"},
            {"time": "12:20 - 13:00", "lesson": "Boş / Etkinlik", "teacher": "-"}
        ],
        "Perşembe": [
            {"time": "07:20 - 08:00", "lesson": "Fen Bilimleri", "teacher": "Mehmet Demir"},
            {"time": "08:10 - 08:50", "lesson": "Fen Bilimleri", "teacher": "Mehmet Demir"},
            {"time": "09:00 - 09:40", "lesson": "Matematik", "teacher": "Ahmet Yılmaz"},
            {"time": "09:50 - 10:30", "lesson": "İngilizce", "teacher": "Ayşe Kaya"},
            {"time": "10:40 - 11:20", "lesson": "İngilizce", "teacher": "Ayşe Kaya"},
            {"time": "11:30 - 12:10", "lesson": "Görsel Sanatlar", "teacher": "Zeynep Can"},
            {"time": "12:20 - 13:00", "lesson": "Müzik", "teacher": "Ali Şen"}
        ],
        "Cuma": [
            {"time": "07:20 - 08:00", "lesson": "İngilizce", "teacher": "Ayşe Kaya"},
            {"time": "08:10 - 08:50", "lesson": "İngilizce", "teacher": "Ayşe Kaya"},
            {"time": "09:00 - 09:40", "lesson": "Matematik", "teacher": "Ahmet Yılmaz"},
            {"time": "09:50 - 10:30", "lesson": "Fen Bilimleri", "teacher": "Mehmet Demir"},
            {"time": "10:40 - 11:20", "lesson": "Beden Eğitimi", "teacher": "Murat Polat"},
            {"time": "11:30 - 12:10", "lesson": "Beden Eğitimi", "teacher": "Murat Polat"},
            {"time": "12:20 - 13:00", "lesson": "Teknoloji Tasarım", "teacher": "Sibel Arslan"}
        ]
    }
}
