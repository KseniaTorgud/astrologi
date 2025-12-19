import os
import openai
import json
from datetime import datetime
from openai import OpenAI

#env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
#if os.path.exists(env_path):
##    with open(env_path, "r", encoding="utf-8") as f:
#        for line in f:
#            if "=" in line and not line.startswith("#"):
#                key, value = line.strip().split("=", 1)
#                os.environ[key] = value

#openai.api_key = "ваш ключ"
#client = OpenAI(api_key=openai.api_key)

"""
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

HORO_PATH = os.path.join(DATA_DIR, "horo.json")


def _load_horo_data():
    if os.path.exists(HORO_PATH):
        with open(HORO_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
def _save_horo_data(data):
    with open(HORO_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
"""
"""
def generate_daily_horoscope(zodiac_sign: str) -> str:
    "Генерирует гороскоп на сегодня."
    "Если гороскоп уже есть в horo.json — возвращает его без вызова ИИ."
    zodiac_sign = zodiac_sign.lower()
    today = datetime.now().strftime("%Y-%m-%d")

    data = _load_horo_data()

    if today not in data:
        data[today] = {}
    if zodiac_sign in data[today]:
        return data[today][zodiac_sign]
    prompt = (
        f"Напиши позитивный, мотивирующий и точный гороскоп для знака {zodiac_sign} "
        f"на сегодня ({today}). 2–3 коротких абзаца. "
        f"Без упоминания других знаков. На русском языке."
    )

    try:
        response = client.responses.create(
            model="gpt-5.2",
            input=[
                {"role": "system", "content": "Ты профессиональный астролог."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_output_tokens=300
        )

        text = response.output_text.strip()
        data[today][zodiac_sign] = text
        _save_horo_data(data)
        return text

    except Exception as e:
        print("Ошибка при генерации гороскопа:", e)
        return "Сегодня гороскоп недоступен. Попробуйте позже."
"""

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
HOROSCOPES_PATH = os.path.join(DATA_DIR, "horoscopes.json")
def generate_daily_horoscope(zodiac_sign: str) -> str:

    zodiac_sign = zodiac_sign.lower()
    if not os.path.exists(HOROSCOPES_PATH):
        return "Файл с гороскопами не найден."
    with open(HOROSCOPES_PATH, "r", encoding="utf-8") as f:
        horoscopes = json.load(f)

    return horoscopes.get(
        zodiac_sign,
        "Гороскоп для этого знака пока не добавлен."
    )
