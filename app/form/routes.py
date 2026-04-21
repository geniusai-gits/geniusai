from flask import Blueprint, render_template, request, redirect, url_for
from app.supabase_client import supabase
import requests

form_bp = Blueprint('form', __name__)

@form_bp.route('/')
def form_page():
    return render_template('form_buat.html')


@form_bp.route('/submit', methods=['POST'])
def submit_form():
    # =========================
    # 1. Ambil data dari form
    # =========================
    nama_chatbot = request.form.get('nama_chatbot')
    nama_usaha = request.form.get('nama_usaha')
    deskripsi_usaha = request.form.get('deskripsi_usaha')
    alur_usaha = request.form.get('alur_usaha')
    tujuan_chatbot = request.form.get('tujuan_chatbot')
    persona = request.form.get('persona')
    batasan_behavior = request.form.get('batasan_behavior')

    file = request.files.get('file_knowledge')
    file_name = file.filename if file else None

    # =========================
    # 2. Insert ke tabel chatbot
    # =========================
    chatbot_res = supabase.table('chatbot').insert({
        "nama_chatbot": nama_chatbot,
        "user_id": 1  # sementara hardcode (nanti kita ambil dari login)
    }).execute()

    chatbot_id = chatbot_res.data[0]['chatbot_id']

    # =========================
    # 3. Insert ke form_chatbot
    # =========================
    supabase.table('form_chatbot').insert({
        "nama_usaha": nama_usaha,
        "deskripsi_usaha": deskripsi_usaha,
        "alur_usaha": alur_usaha,
        "tujuan_chatbot": tujuan_chatbot,
        "persona": persona,
        "batasan_behavior": batasan_behavior,
        "file_knowledge": file_name,
        "id_chatbot": chatbot_id
    }).execute()

    # =========================
    # 4. Kirim ke n8n
    # =========================
    webhook_url = "https://ahmadtarom.app.n8n.cloud/webhook/53d52cb1-ba91-488e-ab49-ec2552705f7a"

    payload = {
        "nama_chatbot": nama_chatbot,
        "nama_usaha": nama_usaha,
        "deskripsi_usaha": deskripsi_usaha,
        "alur_usaha": alur_usaha,
        "tujuan_chatbot": tujuan_chatbot,
        "persona": persona,
        "batasan_behavior": batasan_behavior
    }

    try:
        requests.post(webhook_url, json=payload)
    except:
        print("Gagal kirim ke n8n")

    return redirect('/auth/dashboard')