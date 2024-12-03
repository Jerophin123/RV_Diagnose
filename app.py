import os
import sqlite3
import json
import numpy as np
from flask import Flask, request, render_template, url_for, redirect, session
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from datetime import datetime
import pywhatkit as kit
import threading

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Load the model
model = load_model('model.h5')  # Ensure this path is correct
print('Model loaded. Check http://127.0.0.1:8080/')

# Updated labels for 10 classes
labels = {
    0: 'Bacterial Leaf Blight',
    1: 'Brown Spot',
    2: 'Healthy',
    3: 'Leaf Blast',
    4: 'Leaf Scald',
    5: 'Narrow Brown Spot',
    6: 'Neck Blast',
    7: 'Rice Hispa',
    8: 'Sheath Blight',
    9: 'Tungro'
}

upload_folder = 'static/uploads'
session_folder = 'session_data'
os.makedirs(upload_folder, exist_ok=True)
os.makedirs(session_folder, exist_ok=True)

def get_db_connection():
    connection = sqlite3.connect('flask_app.db')
    connection.row_factory = sqlite3.Row
    return connection

def initialize_db():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Create necessary tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS session_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            login_timestamp TEXT NOT NULL,
            session_data TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            login_timestamp TEXT NOT NULL,
            ip_address TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prediction_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            filename TEXT NOT NULL,
            label TEXT NOT NULL,
            confidence REAL NOT NULL
        )
    ''')

    connection.commit()
    cursor.close()
    connection.close()

# Call initialize_db at the start of your application to ensure tables are created
initialize_db()

def save_log(filename, label, confidence):
    log_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'filename': filename,
        'label': label,
        'confidence': float(confidence)  # Ensure confidence is stored as a float
    }
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO prediction_logs (timestamp, filename, label, confidence)
            VALUES (:timestamp, :filename, :label, :confidence)
        ''', log_entry)

        connection.commit()
        cursor.close()
        connection.close()

        print("Log entry inserted successfully with confidence:", log_entry['confidence'])
    except sqlite3.Error as e:
        print(f"Error saving log entry: {e}")

def getResult(image_path):
    try:
        img = load_img(image_path, target_size=(150, 150))  # Adjust target size to match training
        x = img_to_array(img)
        x = x.astype('float32') / 255.0
        x = np.expand_dims(x, axis=0)
        predictions = model.predict(x)[0]
        return predictions
    except Exception as e:
        print(f"Error in getResult: {e}")
        return None

@app.route('/', methods=['GET'])
def get_started():
    return render_template('get_started.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('signup.html', error="Passwords do not match")

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute('''
                INSERT INTO users (first_name, last_name, email, phone, password)
                VALUES (?, ?, ?, ?, ?)
            ''', (first_name, last_name, email, phone, password))
            connection.commit()
        except sqlite3.IntegrityError:
            connection.rollback()
            return render_template('signup.html', error="Email already exists")
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT * FROM users WHERE email = ? AND password = ?
        ''', (email, password))
        user = cursor.fetchone()

        if user:
            # Store user data in session
            session['user'] = {
                'id': user['id'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'email': user['email'],
                'phone': user['phone']
            }

            # Log the login history
            login_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ip_address = request.remote_addr  # Get the user's IP address
            cursor.execute('''
                INSERT INTO login_history (user_id, login_timestamp, ip_address)
                VALUES (?, ?, ?)
            ''', (user['id'], login_timestamp, ip_address))

            # Store session data
            session_data = str(session['user'])  # Convert session data to string
            cursor.execute('''
                INSERT INTO session_logs (user_id, login_timestamp, session_data)
                VALUES (?, ?, ?)
            ''', (user['id'], login_timestamp, session_data))

            connection.commit()
            cursor.close()
            connection.close()

            return redirect(url_for('main_page'))
        else:
            cursor.close()
            connection.close()
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user' in session:
        user_id = session['user']['id']
        # Save session data as a JSON file
        session_file = os.path.join(session_folder, f'session_{user_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        with open(session_file, 'w') as f:
            json.dump(dict(session), f, indent=4)

        session.clear()
    return redirect(url_for('login'))

@app.route('/main', methods=['GET'])
def main_page():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        if not f:
            return render_template('index.html', result="No file uploaded", icon="", remedy="", file_size_valid=False)

        # Check if the file size exceeds 5MB
        if request.content_length > 5 * 1024 * 1024:  # 5MB limit
            return render_template('index.html', result="File size exceeds 5MB limit", icon="", remedy="", file_size_valid=False)

        # If the file size is within the limit, save and process the file
        file_path = os.path.join(upload_folder, secure_filename(f.filename))
        f.save(file_path)

        predictions = getResult(file_path)
        if predictions is None:
            return render_template('index.html', result="Error processing image", icon="", remedy="", file_size_valid=True)

        predicted_label = labels[np.argmax(predictions)]
        icon = "✅" if predicted_label == 'Healthy' else "⚠"
        confidence = np.max(predictions)

        # Example data - replace with actual logic to fetch these details
        remedy_details = "Apply copper-based bactericides."
        fertilizers_details = "Use balanced fertilizers focusing on potassium."
        pesticides_details = "Use appropriate fungicides."

        # Store the details in session
        session['disease_name'] = predicted_label
        session['remedy_details'] = remedy_details
        session['fertilizers_details'] = fertilizers_details
        session['pesticides_details'] = pesticides_details

        # Save prediction log (this inserts the record into the prediction_logs table)
        save_log(secure_filename(f.filename), predicted_label, confidence)

        # Save specific session data as a JSON file after the prediction
        user_data = {
            'id': session['user']['id'],
            'first_name': session['user']['first_name'],
            'last_name': session['user']['last_name'],
            'email': session['user']['email'],
            'phone': session['user']['phone']
        }
        session_file = os.path.join(session_folder, f'session_{user_data["id"]}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        with open(session_file, 'w') as f:
            json.dump(user_data, f, indent=4)

        return render_template('index.html', result=predicted_label, icon=icon, remedy=remedy_details, fertilizers=fertilizers_details, pesticides=pesticides_details, file_size_valid=True)

@app.route('/disease/<disease>', methods=['GET'])
def disease_details(disease):
    return render_template(f'{disease.lower().replace(" ", "_")}.html', disease=disease)

@app.route('/video/<disease>', methods=['GET'])
def video_view(disease):
    video_mapping = {
        'Bacterial Leaf Blight': 'videos/bacterial_leaf_blight.mp4',
        'Brown Spot': 'videos/brown_spot.mp4',
        'Healthy': 'videos/healthy.mp4',
        'Leaf Blast': 'videos/leaf_blast.mp4',
        'Leaf Scald': 'videos/leaf_scald.mp4',
        'Narrow Brown Spot': 'videos/narrow_brown_spot.mp4',
        'Neck Blast': 'videos/neck_blast.mp4',
        'Rice Hispa': 'videos/rice_hispa.mp4',
        'Sheath Blight': 'videos/sheath_blight.mp4',
        'Tungro': 'videos/tungro.mp4'
    }
    video_url = video_mapping.get(disease)
    if not video_url:
        return redirect(url_for('detailed_view'))
    return render_template('video.html', disease=disease, video_url=url_for('static', filename=video_url))

# Background task to send WhatsApp message
def send_whatsapp_in_background(phone_number, message_body):
    try:
        current_time = datetime.now()
        hour = current_time.hour
        minute = current_time.minute + 1  # Send the message one minute from now
        kit.sendwhatmsg(f"+{phone_number}", message_body, hour, minute)
        print("WhatsApp message sent successfully!")
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")

@app.route('/send_whatsapp', methods=['POST'])
def send_whatsapp():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']
    phone_number = user['phone']

    # Fetching the diagnosis details
    disease_name = session.get('disease_name', '[Disease Name]')
    remedy_details = session.get('remedy_details', '[Remedy Details]')
    fertilizers_details = session.get('fertilizers_details', '[Fertilizer Details]')
    pesticides_details = session.get('pesticides_details', '[Pesticide Details]')

    # Construct the message with actual details
    message_body = (
        f"Hello {user['first_name']},\n\n"
        f"Here are the details of your plant diagnosis:\n\n"
        f"Disease: {disease_name}\n"
        f"Remedy: {remedy_details}\n"
        f"Fertilizers: {fertilizers_details}\n"
        f"Pesticides: {pesticides_details}\n\n"
        f"Stay healthy and keep your plants healthy!"
    )

    # Start the WhatsApp sending process in a background thread
    thread = threading.Thread(target=send_whatsapp_in_background, args=(phone_number, message_body))
    thread.start()

    return render_template('index.html', success="WhatsApp message is being sent!")

if __name__ == "__main__":
    app.run(debug=True)
