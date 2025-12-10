from flask import Blueprint, render_template, jsonify, request
import json
import random
import os

tarot_bp = Blueprint('tarot', __name__, template_folder='templates')

# Загружаем карты из JSON
def load_cards():
    file_path = os.path.join(os.path.dirname(__file__), 'cards.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@tarot_bp.route('/tarot')
def tarot_page():
    return render_template('tarot.html')

# API: вытянуть случайную карту
@tarot_bp.route('/tarot/draw', methods=['GET'])
def draw_card():
    cards = load_cards()
    card = random.choice(cards)
    return jsonify(card)
