from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from database import db, User, Quiz
from werkzeug.security import generate_password_hash, check_password_hash
import json
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///viva_quiz.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])  # Hash the password
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

@app.route('/teacher_dashboard', methods=['GET', 'POST'])
@login_required
def teacher_dashboard():
    return render_template('teacher_dashboard.html')

@app.route('/create_quiz', methods=['POST'])
@login_required
def create_quiz():
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

        return redirect(url_for('quiz_confirmation', quiz_id=quiz_id))  # Redirect to confirmation page
    except Exception as e:
        flash('An error occurred while creating the quiz. Please try again.', 'error')  # Flash an error message

    return redirect(url_for('teacher_dashboard'))

@app.route('/quiz_confirmation/<quiz_id>', methods=['GET'])
@login_required
def quiz_confirmation(quiz_id):
    return render_template('quiz_confirmation.html', quiz_id=quiz_id)

@app.route('/view_quizzes', methods=['GET'])
@login_required
def view_quizzes():
    quizzes = Quiz.query.all()  # Retrieve all quizzes from the database
    # Parse the questions for each quiz
    for quiz in quizzes:
        quiz.questions = json.loads(quiz.questions)  # Parse the JSON string into a Python object
    return render_template('view_quizzes.html', quizzes=quizzes)

@app.route('/student_dashboard', methods=['GET'])
@login_required
def student_dashboard():
    return render_template('student_dashboard.html')

@app.route('/quiz/<quiz_id>', methods=['GET', 'POST'])
@login_required
def quiz(quiz_id):
    quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
    if request.method == 'POST':
        # Process answers and calculate results
        return redirect(url_for('results'))
    return render_template('quiz.html', quiz=json.loads(quiz.questions))

@app.route('/results', methods=['GET'])
@login_required
def results():
    return render_template('results.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))  # Corrected line

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)