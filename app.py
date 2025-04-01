from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
import random
import string
from speech_utils import text_to_speech
from flask import send_file
from gtts import gTTS
import os
from flask import send_from_directory
import time



# Import audio functions

app = Flask(__name__)
app.secret_key = 'your_secret_key'
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

class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.String(20), nullable=False)
    user_answers = db.Column(db.Text, nullable=False)  # JSON format
    total_points = db.Column(db.Integer, nullable=False)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

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
    if current_user.role != 'student':
        return "Unauthorized", 403
    return render_template('student_dashboard.html')


@app.route('/quiz_confirmation/<quiz_id>')
def quiz_confirmation(quiz_id):
    return render_template('quiz_confirmation.html', quiz_id=quiz_id)

@app.route('/create_quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    if current_user.role != 'teacher':
        return "Unauthorized", 403

    if request.method == 'POST':
        try:
            num_questions = int(request.form['numQuestions'])
            quiz_id = generate_quiz_id()  # Generate a secure 6-character quiz ID
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

            return redirect(url_for('quiz_confirmation', quiz_id=new_quiz.quiz_id))

        except Exception as e:
            flash('An error occurred while creating the quiz. Please try again.')
            return render_template('teacher_dashboard.html', error=str(e))

    return render_template('teacher_dashboard.html')

def generate_quiz_id():
    """Generate a secure 6-character alphanumeric quiz ID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route('/view_quizzes')
@login_required
def view_quizzes():
    if current_user.role != 'teacher':
        return "Unauthorized", 403
    quizzes = Quiz.query.all()
    return render_template('view_quizzes.html', quizzes=quizzes)

@app.route('/teacher_quiz_view/<quiz_id>', methods=['GET', 'POST'])
@login_required
def teacher_quiz_view(quiz_id):
    if current_user.role != 'teacher':
        return "Unauthorized", 403

    quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
    if not quiz:
        return "Quiz not found", 404

    # Load questions from JSON
    questions = json.loads(quiz.questions)

    if request.method == 'POST':
        try:
            print("Received Form Data:", request.form)  # Debugging Step

            # Update each question
            for i in range(len(questions)):
                questions[i]['question'] = request.form.get(f'question_{i}', questions[i]['question'])
                
                for key in questions[i]['options'].keys():
                    questions[i]['options'][key] = request.form.get(f'option_{key}_{i}', questions[i]['options'][key])
                
                questions[i]['correct_answer'] = request.form.get(f'correct_answer_{i}', questions[i]['correct_answer'])

            quiz.questions = json.dumps(questions)  # Convert updated questions to JSON
            db.session.commit()
            flash("Quiz updated successfully!", "success")
            print("Updated Quiz:", quiz.questions)  # Debugging Step

        except Exception as e:
            flash("Error updating quiz: " + str(e), "error")
            print("Error:", e)  # Debugging Step

    return render_template('teacher_quiz_view.html', quiz=quiz, questions=questions, enumerate=enumerate)



@app.route("/speak/<text>")
def speak(text):
    try:
        audio_path = "static/question_audio.mp3"

        # **Ensure no file lock exists before generating new audio**
        if os.path.exists(audio_path):
            try:
                os.remove(audio_path)  # Delete old file
                time.sleep(0.5)  # Wait briefly to release file lock
            except Exception as e:
                print(f"Error deleting old audio file: {e}")

        # Generate new TTS file
        tts = gTTS(text=text, lang="en")
        tts.save(audio_path)

        return send_file(audio_path, mimetype="audio/mpeg", as_attachment=False)

    except Exception as e:
        print(f"TTS Error: {e}")  # Log error for debugging
        return str(e), 500
    
    
@app.route('/attempt_quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def attempt_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = json.loads(quiz.questions)  # Load questions

    if request.method == 'POST':
        answers = []

        for i, question in enumerate(questions):
            text_to_speech(f"Question {i+1}: {question['question']}")
            
            options = question['options']
            for letter, option in options.items():
                text_to_speech(f"Option {letter}: {option}")

        return redirect(url_for('results', quiz_id=quiz.id))

    return render_template('attempt_quiz.html', quiz=quiz, questions=questions)

@app.route('/take_quiz', methods=['GET', 'POST'])
@login_required
def take_quiz():
    if request.method == 'POST':
        quiz_id = request.form['quiz_id']
        quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
        if quiz:
            # **🔹 Reset session to start the quiz from the beginning**
            session.pop('quiz_progress', None)
            session.pop('quiz_responses', None)
            session.pop('quiz_id', None)
            return redirect(url_for('quiz', quiz_id=quiz.quiz_id))
        else:
            flash('Invalid Quiz ID. Please try again.')
    return render_template('take_quiz.html')

@app.route('/quiz/<quiz_id>', methods=['GET', 'POST'])
@login_required
def quiz(quiz_id):
    quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
    if not quiz:
        return "Quiz not found", 404

    questions = json.loads(quiz.questions)
    total_questions = len(questions)

    # **🔹 Reset session when starting a new quiz**
    if 'quiz_id' not in session or session.get('quiz_id') != quiz_id:
        session['quiz_progress'] = 0
        session['quiz_responses'] = []
        session['quiz_id'] = quiz_id

    current_index = session['quiz_progress']

    # **🔹 Redirect to results if all questions are answered**
    if current_index >= total_questions:
        attempt = QuizAttempt.query.filter_by(student_id=current_user.id, quiz_id=quiz_id).first()
        if attempt:
            return redirect(url_for('quiz_result', attempt_id=attempt.id))  # ✅ Redirect to quiz results page

    if request.method == 'POST':
        user_answer = request.form.get('answer')

        if 'quiz_responses' not in session:
            session['quiz_responses'] = []

        session['quiz_responses'].append(user_answer)

        if request.form.get('action') == 'next':
            session['quiz_progress'] += 1
            return redirect(url_for('quiz', quiz_id=quiz_id))

        elif request.form.get('action') == 'submit':
            user_responses = session.get('quiz_responses', [])
            total_points = sum(
                1 for i, q in enumerate(questions) if user_responses[i] == q['correct_answer']
            )

            new_attempt = QuizAttempt(
                student_id=current_user.id,
                quiz_id=quiz_id,
                user_answers=json.dumps(user_responses),
                total_points=total_points
            )
            db.session.add(new_attempt)
            db.session.commit()

            # **✅ Redirect to results after storing responses**
            return redirect(url_for('quiz_result', attempt_id=new_attempt.id))

    # **🔹 Prevents IndexError by checking current_index before accessing questions**
    if current_index < total_questions:
        return render_template('quiz.html', question=questions[current_index], current_index=current_index, total_questions=total_questions)
    else:
        return redirect(url_for('quiz_result', attempt_id=attempt.id))  # ✅ Redirect if quiz is completed

@app.route('/previous_attempts')
@login_required
def previous_attempts():
    attempts = QuizAttempt.query.filter_by(student_id=current_user.id).all()
    return render_template('previous_attempts.html', attempts=attempts)

@app.route('/quiz_result/<int:attempt_id>')
@login_required
def quiz_result(attempt_id):
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    if attempt.student_id != current_user.id:
        return "Unauthorized", 403

    quiz = Quiz.query.filter_by(quiz_id=attempt.quiz_id).first()
    if not quiz:
        return "Quiz not found", 404

    questions = json.loads(quiz.questions)
    user_answers = json.loads(attempt.user_answers)
    return render_template('quiz_results.html', questions=questions, user_answers=user_answers, total_points=attempt.total_points)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)  # Run the app in debug mode