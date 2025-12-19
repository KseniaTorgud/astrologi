from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from utils.user_manager import register_user, login_user
from utils.user_manager import get_user, update_birthday
from utils.zodiac import get_zodiac_sign
import json
import random
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "your_secret_key" 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CARDS_PATH = os.path.join(BASE_DIR, "data", "cards.json")

def zodiac_sign(day, month):
    zodiac = [
        ((3, 21), (4, 19), "Овен"),
        ((4, 20), (5, 20), "Телец"),
        ((5, 21), (6, 20), "Близнецы"),
        ((6, 21), (7, 22), "Рак"),
        ((7, 23), (8, 22), "Лев"),
        ((8, 23), (9, 22), "Дева"),
        ((9, 23), (10, 22), "Весы"),
        ((10, 23), (11, 21), "Скорпион"),
        ((11, 22), (12, 21), "Стрелец"),
        ((12, 22), (1, 19), "Козерог"),
        ((1, 20), (2, 18), "Водолей"),
        ((2, 19), (3, 20), "Рыбы")
    ]

    for start, end, sign in zodiac:
        (s_m, s_d), (e_m, e_d) = start, end
        if (month == s_m and day >= s_d) or (month == e_m and day <= e_d):
            return sign
    return None


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mode = request.form.get("mode")  
        username = request.form.get("username")
        password = request.form.get("password")

        if mode == "login":
            ok, msg = login_user(username, password)
            if ok:
                session["username"] = username
                return redirect(url_for("cabinet"))
            return render_template("auth.html", message=msg, mode="login")

        elif mode == "register":
            ok, msg = register_user(username, password)
            if ok:
                return render_template(
                    "auth.html",
                    message="Регистрация успешна ✨ Теперь войдите",
                    mode="login"
                )
            return render_template("auth.html", message=msg, mode="register")

    return render_template("auth.html", mode="login")

@app.route("/cabinet")
def cabinet():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("cabinet.html", username=session["username"])


@app.route("/tarot")
def tarot():
    if "username" not in session:
        return redirect(url_for("login"))

    base_dir = os.path.dirname(os.path.abspath(__file__))
    tarot_path = os.path.join(base_dir, "tarot.json")

    with open(tarot_path, "r", encoding="utf-8") as f:
        cards = json.load(f)

    card = random.choice(list(cards.values()))

    return render_template("tarot.html", card=card)

@app.route("/tarot-three")
def tarot_three():
    if "username" not in session:
        return redirect(url_for("login"))

    tarot_path = os.path.join(BASE_DIR, "tarot.json")
    with open(tarot_path, "r", encoding="utf-8") as f:
        cards = json.load(f)

    three_cards = random.sample(list(cards.values()), 3)
    return jsonify(three_cards)


from utils.ai import generate_daily_horoscope

@app.route("/horoscope", methods=["GET", "POST"])
def horoscope():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    user = get_user(username)

    if not user.get("birthday"):
        if request.method == "POST":
            birthday = request.form.get("birthday")
            date = datetime.strptime(birthday, "%Y-%m-%d")
            sign = get_zodiac_sign(date.month, date.day)
            update_birthday(username, birthday, sign)
            return redirect(url_for("horoscope"))
        return render_template("enter_birthday.html")

    zodiac = user["zodiac"]
    horoscope_text = generate_daily_horoscope(zodiac)
    current_date = datetime.now().strftime("%d.%m.%Y")

    return render_template(
        "horoscope.html",
        zodiac=zodiac,
        horoscope=horoscope_text,
        birthday=user["birthday"],
        current_date=current_date
    )


@app.route("/compatibility", methods=["GET", "POST"])
def compatibility():
    if "username" not in session:
        return redirect(url_for("login"))

    result_block = None
    header = None

    if request.method == "POST":
        name1 = request.form.get("name1")
        birthday1 = request.form.get("birthday1")
        name2 = request.form.get("name2")
        birthday2 = request.form.get("birthday2")

        if not (name1 and birthday1 and name2 and birthday2):
            return "Ошибка: заполнены не все поля", 400

        y_year, y_month, y_day = map(int, birthday1.split("-"))
        p_year, p_month, p_day = map(int, birthday2.split("-"))

        your_sign = zodiac_sign(y_day, y_month)
        partner_sign = zodiac_sign(p_day, p_month)

        with open("compatibility.json", "r", encoding="utf-8") as f:
            comp = json.load(f)

        result = comp.get(your_sign, {}).get(
            partner_sign,
            f"Совместимость {your_sign} + {partner_sign} не найдена."
        )

        header = f"{name1} ({your_sign}) ❤️ {name2} ({partner_sign})"
        result_block = f"{header}\n\n{result}"

        return render_template(
            "compatibility.html",
            result_block=result_block,
            result=result,
            header=header,
            show_result=True
        )

    return render_template("compatibility.html", show_result=False)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
