from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3, os
from ich_model import detect_ich

app = Flask(__name__)
app.secret_key = "secret123"  # Needed for session management

UPLOAD_FOLDER = "uploads/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

DATABASE = "ich_system.db"

# ------------------------------
# Database connection handling
# ------------------------------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE, timeout=10)  # wait if DB is locked
        g.db.row_factory = sqlite3.Row  # optional: makes rows dict-like
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# ------------------------------
# Initialize database tables
# ------------------------------
def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DetectionResults (
        resultID INTEGER PRIMARY KEY AUTOINCREMENT,
        scanName TEXT,
        hemorrhageType TEXT,
        confidenceScore REAL
    )
    """)
    db.commit()

with app.app_context():
    init_db()

# ------------------------------
# Routes
# ------------------------------
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO Users (name,email,password) VALUES (?,?,?)",
                       (name, email, password))
        db.commit()

        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()

    if user:
        session['user'] = user['name']  # row_factory lets us use column names
        return redirect(url_for('upload_scan'))
    else:
        return "Invalid login. Try again."

@app.route('/upload', methods=['GET','POST'])
def upload_scan():
    if 'user' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        file = request.files['ctscan']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Run detection model
        hemorrhageType, confidence = detect_ich(filepath)

        # Save result in DB
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO DetectionResults (scanName, hemorrhageType, confidenceScore) VALUES (?,?,?)",
                       (file.filename, hemorrhageType, confidence))
        db.commit()

        return render_template('result.html', scan=file.filename, result=hemorrhageType, confidence=confidence)
    
    return render_template('upload.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# ------------------------------
# Run the app
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
