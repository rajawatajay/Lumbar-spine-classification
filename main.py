from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import pymysql as sql
import uuid
import os,json
import pathlib
import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import numpy as np
# import cv2
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing.image import load_img, img_to_array
import google.generativeai as ai

from dotenv import load_dotenv
import joblib

load_dotenv()

app = Flask(__name__)
app.secret_key = "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"
ai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# model_path = "C:\\Users\\ajay0\\Desktop\\Lumbar_spine\\Lumbar.pkl"
# model, saved_version = joblib.load(model_path)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def conn():
    db = sql.connect(host='localhost', user='root',
                     password='', database='bcc', port=3307)
    cur = db.cursor()
    return db, cur

# Password validation
def passkey(password):
    lower = 0
    upper = 0
    special = 0
    digit = 0

    for char in password:
        if char.isdigit():
            digit += 1
        elif char.isupper():
            upper += 1
        elif char.islower():
            lower += 1
        elif not char.isidentifier():
            special += 1

    if lower >= 1 and upper >= 1 and digit >= 1 and special >= 1 and len(password) >= 8:
        return True
    else:
        return False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
google_secret = json.load(open(client_secrets_file))
GOOGLE_CLIENT_ID = google_secret["installed"]["client_id"]
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:5000/callback"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/services/')
def services():
    return render_template('services.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db, cur = conn()
        cur.execute(f'SELECT * FROM p_details WHERE email = "{email.strip()}" AND password = "{password.strip()}"')
        user = cur.fetchone()
        print()
        cur.close()
        print(user)
        if user:
            session['user'] = user
            return redirect(url_for('index'))
        else:
            flash('Invalid login credentials')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/login/google')
def login_google():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)
    # return google.authorize(callback=url_for('authorized', _external=True))

@app.route("/callback")
def callback():
    try:
        flow.fetch_token(authorization_response=request.url)

        if not session["state"] == request.args.get("state"):
            abort(500)  # State does not match!
    
        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID
        )

        email = id_info.get("email")
        first_name = id_info.get("given_name")
        last_name = id_info.get("family_name")
        print(email, first_name, last_name)
        # Check if user exists in the database
        db, cur = conn()
        cur.execute("SELECT * FROM p_details WHERE email = %s", (email,))
        user = cur.fetchone()
        print(user)
        if not user:
            # Insert new user
            p_ID = str(uuid.uuid4())
            cur.execute(
                "INSERT INTO p_details (p_ID, Firstname, Lastname, email, phone, address, city, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (p_ID, first_name, last_name, email, None, None, None, None)
            )
            # db.commit()
            cur.execute(
            'SELECT * FROM p_details WHERE email = %s;', (email))
            user = cur.fetchone()
            db.commit()
            print(user)
            print("User created successfully via Google OAuth!")
            flash("Account created successfully via Google OAuth!")
        else:

            flash("Logged in successfully via Google OAuth!")

        session["google_id"] = id_info.get("sub")
        session["user"] = user

        cur.close()
        db.close()

        return redirect(url_for('index'))

    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        print(str(e))
        return redirect(url_for("login"))

@app.route('/submit-form', methods=['POST'])
def submit_form():
    db, cur = conn()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        try:
            cur.execute('INSERT INTO contact_messages (name, email, subject, message) VALUES (%s, %s, %s, %s)',
                        (name, email, subject, message))
            db.commit()
            flash('Message sent successfully!')
            return redirect(url_for('contact'))
        except Exception as e:
            flash(f'Error sending message: {str(e)}')
            db.rollback()  # Rollback in case of error
            return redirect(url_for('contact'))
        finally:
            cur.close()
            db.close()
    flash('Invalid details. Try Again')
    return render_template('contact.html')

lumbar_spine_specialist_system_message = """ You are a lumbar spine specialist AI assistant. Provide accurate, empathetic support to patients, caregivers, and medical professionals.

Skills and Services:
Medical Information: Offer accurate info on lumbar spine conditions, diagnosis, treatment options, and latest research.

Emotional Support: Provide empathetic support and mental health resources for chronic back pain management.

Patient Guidance: Help patients understand their spine condition, treatment plans, and rehabilitation exercises.

Caregiver Support: Guide caregivers in supporting patients with mobility issues and managing daily activities.

Professional Collaboration: Share research, treatment protocols and spine care best practices with medical professionals.

Communication Approach:
If someone ask you name tell them your name is Ubai.

All your responses should be small and short and to the point.

Be clear, accurate, and compassionate.

Offer proactive assistance with tips and resources.

Respect privacy and follow medical ethics.

TERMINATE """


@app.route('/chatbot/', methods=['GET', 'POST'])
def chatbot():
    if request.method == "POST":
        model_chat = ai.GenerativeModel("gemini-1.5-flash", system_instruction=lumbar_spine_specialist_system_message)
        chat = model_chat.start_chat()
        message = request.form.get("message")
        if message:
            print(message)
            if message.lower() == "exit, bye":
                flash("Chat Ended")
                return redirect(url_for('chatbot'))
            response = chat.send_message(message)
            print(response.text)
            if 'messages' not in session:
                session['messages'] = []
            session['messages'].append({'user': message, 'bot': response.text})
            session.modified = True
            return redirect(url_for('chatbot'))
        else:
            flash("No message provided")
            return redirect(url_for('chatbot'))
    messages = session.get('messages', [])
    return render_template('chatbot.html', messages=messages)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    db, cur = conn()
    if request.method == 'POST':    
        Firstname = request.form.get('first_name')
        Lastname = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        password = request.form.get('password')
        cur.execute('UPDATE p_details SET Firstname = %s, Lastname = %s, email = %s, phone = %s, address = %s, city = %s, password = %s WHERE p_ID = %s',
                    (Firstname, Lastname, email, phone, address, city, password, session['user'][0]))
        db.commit()
        
        # Update session details
        cur.execute('SELECT * FROM p_details WHERE p_ID = %s', (session['user'][0],))
        user = cur.fetchone()
        session['user'] = user
        cur.close()
        db.close()
        flash('Profile Updated Successfully!')
        return redirect(url_for('dashboard'))
    flash('Invalid details. Try Again')
    return render_template('update_profile.html')
    

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("index"))

@app.route('/p_register', methods=['POST', 'GET'])
def p_register():
    p_ID = str(uuid.uuid4())
    Firstname = request.form.get('Firstname')
    Lastname = request.form.get('Lastname')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    city = request.form.get('city')
    password = request.form.get('password')

    db, cur = conn()
    if passkey(password):
        cur.execute('INSERT INTO p_details (p_ID, Firstname, Lastname, email, phone, address, city, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                    (p_ID, Firstname, Lastname, email, phone, address, city, password))
        db.commit()
        flash('Account Created Successfully!')
        return redirect(url_for('index'))
    else:
        flash('Invalid details. Try Again')
        return redirect(url_for('login'))

import random

import random

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            try:
                # Save uploaded file temporarily (optional for show)
                uploads_folder = os.path.join(os.path.dirname(__file__), 'uploads')
                if not os.path.exists(uploads_folder):
                    os.makedirs(uploads_folder)
                file_path = os.path.join(uploads_folder, file.filename)
                file.save(file_path)

                # ✨ Simulated prediction
                spine_diseases = [
                    'Normal Spine',
                    'Herniated Disc',
                    'Spondylolisthesis',
                    'Degenerative Disc Disease',
                    'Spinal Stenosis',
                    'Sciatica',
                    'Lumbar Strain',
                    'Facet Joint Syndrome'
                ]
                predicted_class = random.choice(spine_diseases)

                # Optionally remove the file after use
                os.remove(file_path)

                return render_template('predict.html', prediction=predicted_class)
            except Exception as e:
                print(f"Prediction error: {str(e)}")
                return redirect(request.url)
        else:
            print("Invalid file format")
            return redirect(request.url)
    return render_template('predict.html')


if __name__ == '__main__':
    app.run(debug=True)