from flask import Blueprint, request, redirect
from app.supabase_client import supabase
from flask import render_template
from flask import redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

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
            return "Login berhasil!"
        else:
            return "Password salah!"

    return "User tidak ditemukan!"