from flask import Flask, render_template, request, jsonify, redirect, url_for, g, session
import sqlite3
import random
import datetime
import uuid
try:
    from google.oauth2 import id_token
    from google.auth.transport import requests as google_requests
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False

app = Flask(__name__)
app.secret_key = 'super_secret_key_mindwell_2024'
DATABASE = 'mindwell.db'
GOOGLE_CLIENT_ID = '522137806672-a5mvig6sr2ktr15jgjhlgemb59j7ikfg.apps.googleusercontent.com'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                score INTEGER NOT NULL,
                severity TEXT NOT NULL,
                date TEXT,
                session_id TEXT
            )
        ''')
        # Add users table for authentication
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE,
                password TEXT,
                auth_provider TEXT DEFAULT 'local',
                points INTEGER DEFAULT 100,
                tree_level INTEGER DEFAULT 1,
                streak INTEGER DEFAULT 1
            )
        ''')
        # Add session_id column if not exists
        try:
            db.execute('ALTER TABLE assessments ADD COLUMN session_id TEXT')
        except:
            pass
        db.commit()

# Mock Data - Constants
DAILY_QUESTS = [
    {
        'id': 1,
        'title': "The 'Traffic Jam' Scenario",
        'description': "You are stuck in heavy traffic and running late for an important meeting. Your chest feels tight.",
        'options': [
            {'text': 'Honk aggressively', 'feedback': 'Stress +10! Aggression often increases anxiety.'},
            {'text': 'Listen to music', 'feedback': 'Calm +5! Distraction can be a healthy coping mechanism.'}
        ]
    },
    {
        'id': 2,
        'title': "The 'Unknown Caller' Scenario",
        'description': "Your phone rings from an unknown number. You usually avoid these calls.",
        'options': [
            {'text': 'Ignore it', 'feedback': 'Avoidance +5. Valid, but exposure therapy might suggest answering.'},
            {'text': 'Answer politely', 'feedback': 'Courage +10! Facing uncertainty builds resilience.'}
        ]
    },
    {
        'id': 3,
        'title': "The 'Critical Email' Scenario",
        'description': "You receive an email from your boss saying 'We need to talk'. Panic sets in.",
        'options': [
            {'text': 'Overthink everything', 'feedback': 'Anxiety +10. Catastrophizing drains your energy.'},
            {'text': 'Ask for time', 'feedback': 'Control +5. Clarifying the context helps reduce fear.'}
        ]
    }
]

@app.before_request
def ensure_session():
    if 'user' not in session:
        session['user'] = {
            'name': 'Guest',
            'streak': random.randint(1, 5),
            'points': 100,
            'avatar': 'avatar1.png',
            'tree_level': 1,
            'current_quest': DAILY_QUESTS[0],
            'id': str(uuid.uuid4())
        }
    if 'journal' not in session:
        session['journal'] = []

@app.context_processor
def inject_user():
    if 'user' in session:
        return dict(user=session['user'])
    return dict(user={})

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        db = get_db()
        user_row = None
        
        if action == 'register':
            try:
                db.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
                db.commit()
                user_row = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            except sqlite3.IntegrityError:
                return "Username or email already exists. Go back and try again."
        elif action == 'login':
            user_row = db.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
            if not user_row:
                return "Invalid credentials. Go back and try again."
        elif action == 'google_mock':
            user_row = db.execute('SELECT * FROM users WHERE email = ?', ('google_mock@example.com',)).fetchone()
            if not user_row:
                db.execute('INSERT INTO users (username, email, auth_provider) VALUES (?, ?, ?)', ('GoogleUser', 'google_mock@example.com', 'google'))
                db.commit()
                user_row = db.execute('SELECT * FROM users WHERE email = ?', ('google_mock@example.com',)).fetchone()

        if user_row:
            user = session['user']
            user['name'] = user_row['username']
            user['id'] = str(user_row['id'])
            user['points'] = user_row['points'] + 10  # Simulate login reward
            user['tree_level'] = user_row['tree_level']
            user['streak'] = user_row['streak']
            user['current_quest'] = random.choice(DAILY_QUESTS)
            session['user'] = user
            
            # update points in db
            db.execute('UPDATE users SET points = ? WHERE id = ?', (user['points'], user_row['id']))
            db.commit()
            
            return redirect(url_for('dashboard', show_garden=1))

    # Fallback if no POST or if direct GET request
    return redirect(url_for('index'))

@app.route('/auth/google', methods=['POST'])
def auth_google():
    credential = request.form.get('credential')
    if not credential:
        return redirect(url_for('index'))

    try:
        if GOOGLE_AUTH_AVAILABLE:
            idinfo = id_token.verify_oauth2_token(
                credential,
                google_requests.Request(),
                GOOGLE_CLIENT_ID
            )
            email = idinfo.get('email')
            name = idinfo.get('name', email.split('@')[0])
            picture = idinfo.get('picture', '')
        else:
            return "google-auth library not installed. Run: pip install google-auth", 500

        db = get_db()
        user_row = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if not user_row:
            username = name.replace(' ', '') or email.split('@')[0]
            # Ensure unique username
            base = username
            counter = 1
            while db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone():
                username = f"{base}{counter}"
                counter += 1
            db.execute(
                'INSERT INTO users (username, email, password, auth_provider) VALUES (?, ?, ?, ?)',
                (username, email, '', 'google')
            )
            db.commit()
            user_row = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        user = session['user']
        user['name'] = user_row['username']
        user['id'] = str(user_row['id'])
        user['points'] = user_row['points'] + 10
        user['tree_level'] = user_row['tree_level']
        user['streak'] = user_row['streak']
        user['current_quest'] = random.choice(DAILY_QUESTS)
        session['user'] = user

        db.execute('UPDATE users SET points = ? WHERE id = ?', (user['points'], user_row['id']))
        db.commit()

        return redirect(url_for('dashboard', show_garden=1))

    except ValueError as e:
        print(f"Google token error: {e}")
        return redirect(url_for('index'))

@app.route('/refresh_scenario')
def refresh_scenario():
    user = session['user']
    current_id = user['current_quest']['id']
    available_quests = [q for q in DAILY_QUESTS if q['id'] != current_id]
    if available_quests:
        user['current_quest'] = random.choice(available_quests)
        session['user'] = user
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    db = get_db()
    # Filter history by session_id
    user_id = session['user']['id']
    cursor = db.execute('SELECT * FROM assessments WHERE session_id = ? ORDER BY id DESC LIMIT 5', (user_id,))
    history = cursor.fetchall()
    return render_template('dashboard.html', user=session['user'], history=history)

@app.route('/assessment/<type>', methods=['GET', 'POST'])
def assessment(type):
    if request.method == 'POST':
        score = 0
        answers = request.form
        for key in answers:
            try:
                score += int(answers[key])
            except:
                pass
        
        severity = "Mild"
        if score > 10: severity = "Moderate"
        if score > 15: severity = "Severe"
        
        # Growth Logic
        user = session['user']
        if user['tree_level'] < 5:
            user['tree_level'] += 1
        
        user['points'] += 50
        session['user'] = user
        
        # Save to Database with session_id
        db = get_db()
        current_date = datetime.datetime.now().strftime("%Y-m-%d %H:%M")
        db.execute('INSERT INTO assessments (type, score, severity, date, session_id) VALUES (?, ?, ?, ?, ?)',
                   (type, score, severity, current_date, session['user']['id']))
        db.commit()
        
        return render_template('result.html', type=type, score=score, severity=severity)
    
    return render_template('assessment.html', type=type)

@app.route('/delete_assessment/<int:id>', methods=['POST'])
def delete_assessment(id):
    db = get_db()
    db.execute('DELETE FROM assessments WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('dashboard'))

@app.route('/rppg')
def rppg():
    return render_template('rppg.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    user_msg = request.json.get('message', '').lower()
    
    # Smart Keyword Detection System
    response = "I'm here for you. Can you tell me more about that?"
    
    keywords = {
        'anxiety': ["Take a deep breath. 4-7-8 breathing can help.", "It's valid to feel this way. Focus on the present moment.", "Would you like to try a grounding exercise?"],
        'anxious': ["Take a deep breath. 4-7-8 breathing can help.", "It's valid to feel this way. Focus on the present moment.", "Would you like to try a grounding exercise?"],
        'sad': ["I'm sorry you're feeling down. I'm listening.", "It's okay to cry. Let it out.", "Do you want to talk about what's making you sad?"],
        'depress': ["I'm sorry you're feeling down. I'm listening.", "It's okay to cry. Let it out.", "Do you want to talk about what's making you sad?"],
        'happy': ["That's wonderful! Hold onto this feeling.", "I'm glad to hear that! What made you smile?", "Celebrate these moments! 🎉"],
        'good': ["That's wonderful! Hold onto this feeling.", "I'm glad to hear that! What made you smile?", "Celebrate these moments! 🎉"],
        'suicide': ["Please, if you are in danger, call the SOS helpline immediately.", "You are not alone. Please use the SOS button on the dashboard.", "Your life matters. Please reach out to a professional."],
        'sleep': ["Sleep is important. Have you tried the sleep music in Resources?", "Try to avoid screens before bed.", "A warm tea might help you relax."],
        'help': ["I'm here. You can use the 'Resources' tab for tools or 'SOS' for urgent help.", "How can I support you right now?"]
    }
    
    found = False
    for key, answers in keywords.items():
        if key in user_msg:
            response = random.choice(answers)
            found = True
            break
            
    if not found:
        generics = [
            "I hear you.",
            "That sounds challenging.",
            "I'm listening. Go on.",
            "How long have you felt this way?",
            "Mindwell is a safe space for you."
        ]
        response = random.choice(generics)

    return jsonify({'response': response})

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if 'journal' not in session:
        session['journal'] = []
    
    if request.method == 'POST':
        entry = request.form.get('entry')
        mood = request.form.get('mood')
        entry_id = str(uuid.uuid4())
        
        new_entry = {'id': entry_id, 'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 'text': entry, 'mood': mood}
        
        journal_list = session['journal']
        journal_list.insert(0, new_entry)
        session['journal'] = journal_list # Save back to session
        
        return redirect(url_for('journal'))
    return render_template('journal.html', entries=session['journal'])

@app.route('/delete_journal_entry/<string:entry_id>', methods=['POST'])
def delete_journal_entry(entry_id):
    if 'journal' in session:
        journal_list = [entry for entry in session['journal'] if entry.get('id') != entry_id]
        session['journal'] = journal_list
    return redirect(url_for('journal'))

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/sos')
def sos():
    return render_template('sos.html')

@app.route('/community')
def community():
    return render_template('community.html')

@app.route('/counsellors')
def counsellors():
    return render_template('counsellors.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000, host='0.0.0.0')
