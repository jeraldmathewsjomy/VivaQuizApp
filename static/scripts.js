// Copy Quiz ID to Clipboard
function copyToClipboard(quizId) {
    navigator.clipboard.writeText(quizId).then(
        () => alert('Quiz ID copied to clipboard!'),
        () => alert('Failed to copy Quiz ID.')
    );
}

// Text-to-Speech (TTS)
function speakText(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(utterance);
    } else {
        alert('Text-to-Speech is not supported in this browser.');
    }
}

// Read Out Questions and Options
function readQuizQuestions(questions) {
    questions.forEach((question, index) => {
        speakText(`Question ${index + 1}: ${question.text}`);
        question.options.forEach((option, optIndex) => {
            speakText(`Option ${optIndex + 1}: ${option}`);
        });
    });
}

// Voice Recognition for Answering
function startVoiceRecognition(callback) {
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = function () {
            console.log('Voice recognition started. Speak now.');
        };

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            console.log(`Recognized: ${transcript}`);
            if (callback) callback(transcript);
        };

        recognition.onerror = function (event) {
            console.error('Voice recognition error:', event.error);
        };

        recognition.onend = function () {
            console.log('Voice recognition ended.');
        };

        recognition.start();
    } else {
        alert('Voice recognition is not supported in this browser.');
    }
}

// Quiz Form Validation
document.addEventListener('DOMContentLoaded', () => {
    const quizForm = document.querySelector('#quiz-form');
    if (quizForm) {
        quizForm.addEventListener('submit', (event) => {
            const unanswered = Array.from(quizForm.querySelectorAll('input[type="radio"]'))
                .filter(input => !input.checked)
                .length;

            if (unanswered > 0) {
                event.preventDefault();
                alert('Please answer all questions before submitting.');
            }
        });
    }

    // Example: Add voice recognition to answer quiz
    const voiceAnswerButton = document.getElementById('voice-answer');
    if (voiceAnswerButton) {
        voiceAnswerButton.addEventListener('click', () => {
            startVoiceRecognition((transcript) => {
                alert(`You said: ${transcript}`);
                // Map the transcript to an answer option if needed
            });
        });
    }
});
