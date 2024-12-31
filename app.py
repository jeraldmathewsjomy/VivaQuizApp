from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///viva_quiz.db'
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Database models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'teacher' or 'student'

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.String(20), unique=True, nullable=False)
    questions = db.Column(db.Text, nullable=False)  # JSON format

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('signup.html', error="Username already exists. Please choose a different one.")

        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('teacher_dashboard' if user.role == 'teacher' else 'student_dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/teacher_dashboard')
@login_required
def teacher_dashboard():
    if current_user.role != 'teacher':
        return "Unauthorized", 403
    return render_template('teacher_dashboard.html')

@app.route('/student_dashboard')
@login_required
def student_dashboard():
    return render_template('student_dashboard.html')

@app.route('/take_quiz', methods=['GET', 'POST'])
@login_required
def take_quiz():
    if request.method == 'POST':
        quiz_id = request.form['quiz_id']
        quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()  # Check if quiz_id exists in the database
        if quiz:
            return redirect(url_for('quiz', quiz_id=quiz.quiz_id))
        else:
            flash('Invalid Quiz ID. Please try again.')
    return render_template('take_quiz.html')


@app.route('/create_quiz', methods=['POST'])
@login_required
def create_quiz():
    if current_user.role != 'teacher':
        return "Unauthorized", 403

    try:
        num_questions = int(request.form['numQuestions'])
        quiz_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))  # Generate a random quiz ID
        questions = []

        # Collect questions and options from the form
        for i in range(num_questions):
            question = request.form[f'question_{i}']
            options = {
                'A': request.form[f'option_a_{i}'],
                'B': request.form[f'option_b_{i}'],
                'C': request.form[f'option_c_{i}'],
                'D': request.form[f'option_d_{i}'],
            }
            correct_answer = request.form[f'correct_answer_{i}']
            questions.append({
                'question': question,
                'options': options,
                'correct_answer': correct_answer
            })

        # Store the quiz in the database
        new_quiz = Quiz(quiz_id=quiz_id, questions=json.dumps(questions))
        db.session.add(new_quiz)
        db.session.commit()

        return redirect(url_for('quiz_confirmation', quiz_id=quiz_id))
    except Exception as e:
        flash('An error occurred while creating the quiz. Please try again.')
        return render_template('create_quiz.html', error=str(e))
    
@app.route('/quiz/<quiz_id>', methods=['GET', 'POST'])
@login_required
def quiz(quiz_id):
    quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()  # Retrieve the quiz from the database
    if not quiz:
        return "Quiz not found", 404

    if request.method == 'POST':
        user_answers = []
        total_points = 0
        questions = json.loads(quiz.questions)  # Parse the JSON string into a Python list

        # Calculate total points
        for i, question in enumerate(questions):
            user_answer = request.form.get(f'answer_{i + 1}')
            user_answers.append(user_answer)
            if user_answer == question['correct_answer']:
                total_points += 1

        # Pass total_points to the results template
        return render_template('quiz_results.html', questions=questions, user_answers=user_answers, total_points=total_points)
    return render_template('quiz.html', quiz=json.loads(quiz.questions))

if __name__ == '__main__':
    with app.app_context():  # Set up application context
        db.create_all()  # Create database tables
    app.run(debug=True)