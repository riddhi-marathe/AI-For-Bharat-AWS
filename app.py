from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta
import subprocess
import os
import boto3
import json

# --- CONFIGURATION ---
app = Flask(__name__)
app.secret_key = 'hackathon_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learnflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- AWS BEDROCK CONFIGURATION ---
try:
    # Note: Humne keys yahan nahi likhi hain kyunki aapne terminal mein 'aws configure' chala diya hai.
    # Boto3 apne aap terminal/system se keys utha lega.
    bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
    print("AWS Bedrock successfully initialized!")
except Exception as e:
    print(f"AWS Initialization Error: {e}")
    bedrock_client = None


# --- DATABASE MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    learning_time_seconds = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=1)
    last_login_date = db.Column(db.Date, default=date.today)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    thumbnail = db.Column(db.String(500), nullable=True)
    progress = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Initialize database tables
with app.app_context():
    db.create_all()


# --- AUTHENTICATION ---
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Prevent database crash if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please login.')
            return redirect(url_for('register'))
            
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            session['username'] = user.username
            
            # Streak Logic
            today = date.today()
            if user.last_login_date == today - timedelta(days=1):
                user.current_streak += 1
            elif user.last_login_date != today:
                user.current_streak = 1
                
            user.last_login_date = today
            db.session.commit()
            return redirect(url_for('dashboard'))
            
        flash('Invalid Credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# --- DASHBOARD & ANALYTICS ---
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    
    # Safety net
    if not user:
        session.clear()
        return redirect(url_for('login'))
    
    hours_learned = round(user.learning_time_seconds / 3600, 1)
    passed_tests = 38  
    total_tests = 55
    donut_data = [passed_tests, total_tests - passed_tests]
    completion_percent = int((passed_tests / total_tests) * 100) if total_tests > 0 else 0
    
    return render_template('dashboard.html', 
                           username=user.username, streak=user.current_streak,
                           hours_learned=hours_learned, passed_tests=passed_tests,
                           total_tests=total_tests, completion_percent=completion_percent,
                           donut_data=donut_data)

@app.route('/analytics')
def analytics():
    if 'user_id' not in session: return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    
    if not user:
        session.clear()
        return redirect(url_for('login'))

    user_courses = Course.query.filter_by(user_id=user.id).all()
    total_courses = len(user_courses)
    
    avg_progress = sum(c.progress for c in user_courses) // total_courses if total_courses > 0 else 0
    hours_learned = round(user.learning_time_seconds / 3600, 1)
    
    return render_template('analytics.html', 
                           username=user.username,
                           total_courses=total_courses,
                           avg_progress=avg_progress,
                           hours_learned=hours_learned,
                           streak=user.current_streak)


# --- COURSES ---
@app.route('/custom_tests', methods=['GET', 'POST'])
def custom_tests():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_course = Course(
            title=request.form.get('title'),
            url=request.form.get('url'),
            thumbnail=request.form.get('thumbnail') or "https://via.placeholder.com/300x150",
            user_id=session['user_id']
        )
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('custom_tests'))
    
    courses = Course.query.filter_by(user_id=session['user_id']).all()
    return render_template('custom_tests.html', username=session['username'], courses=courses)


# --- WORKSPACE & AI CHATBOT (AWS BEDROCK) ---
@app.route('/coding_workspace')
def coding_workspace():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('coding_workspace.html', username=session['username'])

@app.route('/run_code', methods=['POST'])
def run_code():
    if 'user_id' not in session:
        return {'error': 'Unauthorized'}, 401
    
    user_code = request.json.get('code', '')
    try:
        result = subprocess.run(['python', '-c', user_code], capture_output=True, text=True, timeout=5)
        output = result.stdout if result.returncode == 0 else result.stderr
    except subprocess.TimeoutExpired:
        output = "Error: Code execution timed out (Infinite loop?)."
    except Exception as e:
        output = f"Execution Error: {str(e)}"

    return {'output': output}

@app.route('/ai_chatbot')
def ai_chatbot():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('ai_chatbot.html', username=session['username'])

@app.route('/ask_ai', methods=['POST'])
def ask_ai():
    if 'user_id' not in session: 
        return {'error': 'Unauthorized'}, 401
    
    # Safe JSON parsing
    data = request.get_json(silent=True)
    if not data or 'message' not in data:
        return {'reply': "Please ask a question!"}
        
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return {'reply': "I didn't catch that. Please type a message."}

    if not bedrock_client:
        return {'reply': "AWS Bedrock credentials missing or error initializing. Check your terminal logs."}

    try:
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "system": "You are an expert coding tutor for 'Learn Flow AI'. Be encouraging, concise, and help the user figure out the answer rather than just giving away the code immediately.",
            "messages": [
                {"role": "user", "content": user_message}
            ]
        })
        
        # Calling Claude 3 Haiku via Bedrock
        response = bedrock_client.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0', 
            body=body, 
            accept='application/json', 
            contentType='application/json'
        )
        
        response_body = json.loads(response.get('body').read())
        return {'reply': response_body['content'][0]['text']}
        
    except Exception as e:
        print(f"--- BEDROCK ERROR --- : {str(e)}") # Prints detailed error in terminal
        return {'reply': f"AWS Bedrock Error: Please check terminal for details."}

# --- RUN APP ---
if __name__ == '__main__':
    app.run(debug=True)