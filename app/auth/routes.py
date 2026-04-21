from flask import Blueprint, request, redirect
from app.supabase_client import supabase
from flask import render_template
from flask import redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, session, redirect
from app.supabase_client import supabase
import requests
from flask import request, jsonify

auth = Blueprint('auth', __name__)

@auth.route('/')
def auth_page():
    return render_template('auth.html')

@auth.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    hashed_password = generate_password_hash(password)
    
    supabase.table("users").insert({
        "username": username,
        "password": hashed_password
    }).execute()

    return redirect(url_for('auth.auth_page'))

@auth.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    result = supabase.table("users") \
        .select("*") \
        .eq("username", username) \
        .execute()

    if result.data:
        user = result.data[0]

        if check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect('/auth/dashboard')
        else:
            return "Password salah!"

    return "User tidak ditemukan!"

@auth.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')

    if not user_id:
        return redirect('/auth/login')

    # ambil chatbot berdasarkan user login
    response = supabase.table('chatbot')\
        .select('*')\
        .eq('user_id', user_id)\
        .execute()

    chatbots = response.data
    

    return render_template('dashboard.html', chatbots=chatbots)

@auth.route('/chat/<int:chatbot_id>')
def chat_page(chatbot_id):
    return render_template('chat.html', chatbot_id=chatbot_id)

@auth.route('/send-message', methods=['POST'])
def send_message():
    data = request.json

    message = data.get('message')
    chatbot_id = data.get('chatbot_id')

    # 🔥 URL webhook n8n kamu
    N8N_WEBHOOK = "https://ahmadtarom.app.n8n.cloud/webhook/9c84e37f-d7f0-4862-9709-be08bc289d9c"

    response = requests.post(N8N_WEBHOOK, json={
        "message": message,
        "chatbot_id": chatbot_id
    })

    result = response.json()

    return jsonify({
        "reply": result.get("reply", "Tidak ada respon")
    })