# VivaQuiz App 🎤📚

**VivaQuiz App** is a voice-interactive quiz platform built with accessibility at its core. Tailored specifically for blind students and oral assessments, the app enables learners to **hear questions and options** and respond using **voice commands**. Teachers can seamlessly create, manage, and distribute quizzes via unique access codes.

---

## 🧠 Table of Contents

- [🎯 Introduction](#-introduction)
- [🚀 Objective](#-objective)
- [🧩 Problem Statement](#-problem-statement)
- [🛠️ Tech Stack & Libraries](#-tech-stack--libraries)
- [🎥 Demonstration](#-demonstration)
  - [👨‍🏫 Teacher Login Flow](#-teacher-login-flow)
  - [👨‍🎓 Student Login Flow](#-student-login-flow)
- [📸 Screenshots](#-screenshots)
- [🔗 Video Sample](#-video-sample)
- [💡 Additional Features](#-additional-features)
- [📂 Project Structure](#-project-structure)
- [🧪 How to Run This Project](#-how-to-run-this-project)
- [📎 License](#-license)

---

## 🎯 Introduction

**VivaQuiz App** is a web-based solution leveraging speech-to-text and text-to-speech technologies to create an inclusive quiz experience. It is designed to support oral assessments and enhance accessibility for visually impaired students.

---

## 🚀 Objective

- Empower blind students to participate in quizzes using voice input.
- Simplify viva exam creation and management via an intuitive web interface.
- Offer a smooth user experience for both educators and students.
- Automatically track and store quiz performance and history.

---

## 🧩 Problem Statement

Conventional quiz platforms are not optimized for **visually impaired users** or **voice-based assessments**. VivaQuiz bridges this accessibility gap by:

- Using TTS (Text-to-Speech) to read questions and options aloud.
- Capturing spoken answers using voice recognition.
- Providing instant scoring and feedback.
- Allowing teachers to easily create and distribute quizzes through unique codes.

---

## 🛠️ Tech Stack & Libraries

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap (for responsive design)

**Backend:**
- Python (Flask Framework)

**Key Libraries:**
- `Flask-Login` – User authentication and session management
- `SpeechRecognition` – Speech-to-text functionality
- `gTTS` (Google Text-to-Speech) – Converts text to spoken audio
- `SQLAlchemy` – ORM for database operations
- `SQLite` – Lightweight embedded database
- `PyAudio` – Microphone input capture
- `WTForms` – Secure form handling

---

## 🎥 Demonstration

### 👨‍🏫 Teacher Login Flow

#### 1. Signup / Login  
Teachers can sign up or log in using their credentials.  
![Screenshot 2025-04-12 161611](https://github.com/user-attachments/assets/73f1f31a-314b-4c2c-a7a1-6e801ea4a472)

#### 2. Access Dashboard & Create Quiz  
Click the **"Create Quiz"** button to start creating a new quiz.  
![Screenshot 2025-04-12 161706](https://github.com/user-attachments/assets/f7297d73-429a-45ca-9644-f6a16d1c6f56)

#### 3. Set Number of Questions  
Select how many questions you wish to add to the quiz.  
![Screenshot 2025-04-12 161723](https://github.com/user-attachments/assets/621ac2e7-e218-4a60-88ef-5189f0dcb7b3)

#### 4. Enter Questions and Options  
Input the quiz question along with four options and specify the correct one.  
![Screenshot 2025-04-12 162058](https://github.com/user-attachments/assets/59cd98f8-09c0-4698-baf5-e1ad06f94757)

#### 5. Get Unique Code  
After submitting, a **unique code** is generated. Share this with students privately.  
![Screenshot 2025-04-12 162109](https://github.com/user-attachments/assets/9ab45257-026a-4ba6-a197-84125ec9fa11)

#### Additional Features for Teachers:  
- View all previously created quizzes.  
- Edit or delete existing quizzes.  
![Screenshot 2025-04-12 162237](https://github.com/user-attachments/assets/2efd2019-6def-42a9-b8c5-a92defb2b767)  
![Screenshot 2025-04-12 162249](https://github.com/user-attachments/assets/1607e889-dd3c-4ab6-9cfc-b55d525ba388)

---

### 👨‍🎓 Student Login Flow

#### 1. Student Dashboard  
Log in with student credentials to access the dashboard.  
![Screenshot 2025-04-12 161611](https://github.com/user-attachments/assets/f35f5d47-330b-4a76-aab5-6b68c06d7868)

#### 2. Click on “Attempt Quiz”  
Click the **"Attempt Quiz"** button on the dashboard.  
![Screenshot 2025-04-12 162313](https://github.com/user-attachments/assets/f4e8aee7-cb54-4490-bb04-fab28be85425)

#### 3. Enter Quiz Code  
Input the validation code shared by the teacher to access the quiz.  
![Screenshot 2025-04-12 162348](https://github.com/user-attachments/assets/5585c11f-df85-4acb-94ab-f0ee11df0712)

#### 4. Voice-Interactive Quiz  
Questions and options will be **read aloud**. Students can **answer by speaking**.  
https://github.com/user-attachments/assets/2d296ac8-e6e8-4b90-a836-7b58bf502ea4

#### 5. View Score Immediately  
After the quiz, the results are displayed instantly with the score.  
![Screenshot 2025-04-12 163303](https://github.com/user-attachments/assets/7278dae8-c65c-4a14-8dc0-06920a627426)

#### Additional Features for Students:  
- Review past quiz attempts.  
- View correct answers after submission.  
![Screenshot 2025-04-12 163321](https://github.com/user-attachments/assets/174fc0e2-218a-4ef1-9fcc-bffd112a5d5f)

---

## 📂 Project Structure

```plaintext
VivaQuizApp/
├── __pycache__/               # Python bytecode cache
├── instance/                  # Flask instance folder (e.g., config, DB)
├── static/                    # Static assets (CSS, JS)
│   └── style.css              # Main stylesheet
├── templates/                 # HTML templates for rendering views
│   ├── login.html
│   ├── teacher_dashboard.html
│   ├── student_dashboard.html
│   ├── create_quiz.html
│   ├── attempt_quiz.html
│   └── result.html
├── app.py                     # Entry point of the Flask app
├── database.py                # SQLAlchemy models and DB logic
├── speech_utils.py            # Text-to-speech and voice input functions
├── temp_audio.mp3             # Temporary audio for TTS output
├── test_speech.py             # Script to test speech functions
├── requirements.txt           # Python package dependencies
└── project_structure.txt      # File structure documentation
```

---

## 🔗 Video Sample

🎬 [Click to Watch a Sample Quiz Attempt](https://github.com/user-attachments/assets/2d296ac8-e6e8-4b90-a836-7b58bf502ea4)

---

## 💡 Additional Features

- Real-time **text-to-speech** for questions and options.
- **Voice input** for seamless and inclusive interaction.
- **Clean dashboards** for teachers and students.
- Support for **reviewing previous attempts** with instant scoring.
- Fully tailored for **accessibility and inclusivity**.
- **Instant feedback** and **auto-grade** functionality.

---

## 🧪 How to Run This Project

### 🔧 Prerequisites

Ensure the following tools are installed:

- Python 3.7 or higher
- pip (Python package installer)
- Git

---

### 📥 1. Clone the Repository

```bash
git clone https://github.com/jeraldmathewsjomy/VivaQuizApp.git
cd VivaQuizApp
```

---

### 📦 2. Set Up a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows
```

---

### 📚 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `pyaudio` fails to install:

**Windows:**

```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**

```bash
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

---

### 🧠 4. Initialize the Database

No manual setup is required. The database initializes automatically when the app is launched.

---

### 🚀 5. Run the Application

```bash
python app.py
```

Access the app via your browser at:

```
http://127.0.0.1:5000
```

---

### 👁️‍🗨️ 6. Start Using VivaQuiz

- **Teachers**: Sign up → Create Quiz → Share Code
- **Students**: Login → Enter Code → Use Voice to Answer → View Results

---

## ✅ You're Ready to Quiz!

You’ve successfully set up the VivaQuiz App. Start exploring accessible, voice-based quizzes for a better, more inclusive learning experience!

---

## 📎 License

This project is intended for academic and demonstration purposes.

---

> Built with ❤️ to make education inclusive and engaging for all.
