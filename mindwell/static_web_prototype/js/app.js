// Default User State
const defaultUser = {
    name: 'Guest',
    streak: 3,
    points: 100,
    tree_level: 1,
    current_quest: {
        title: "The 'Unknown Caller' Scenario",
        description: "Your phone rings from an unknown number. You usually avoid these calls.",
        options: [
            { text: 'Ignore it', feedback: 'Avoidance +5. Valid, but exposure therapy might suggest answering.' },
            { text: 'Answer politely', feedback: 'Courage +10! Facing uncertainty builds resilience.' }
        ]
    }
};

const keywords = {
    'anxiety': ["Take a deep breath. 4-7-8 breathing can help.", "It's valid to feel this way. Focus on the present moment.", "Would you like to try a grounding exercise?"],
    'anxious': ["Take a deep breath. 4-7-8 breathing can help.", "It's valid to feel this way. Focus on the present moment.", "Would you like to try a grounding exercise?"],
    'sad': ["I'm sorry you're feeling down. I'm listening.", "It's okay to cry. Let it out.", "Do you want to talk about what's making you sad?"],
    'depress': ["I'm sorry you're feeling down. I'm listening.", "It's okay to cry. Let it out.", "Do you want to talk about what's making you sad?"],
    'happy': ["That's wonderful! Hold onto this feeling.", "I'm glad to hear that! What made you smile?", "Celebrate these moments! 🎉"],
    'good': ["That's wonderful! Hold onto this feeling.", "I'm glad to hear that! What made you smile?", "Celebrate these moments! 🎉"],
    'suicide': ["Please, if you are in danger, call the SOS helpline immediately.", "You are not alone. Please use the SOS button on the dashboard.", "Your life matters. Please reach out to a professional."],
    'sleep': ["Sleep is important. Have you tried the sleep music in Resources?", "Try to avoid screens before bed.", "A warm tea might help you relax."],
    'help': ["I'm here. You can use the 'Resources' tab for tools or 'SOS' for urgent help.", "How can I support you right now?"]
};

const generics = [
    "I hear you.",
    "That sounds challenging.",
    "I'm listening. Go on.",
    "How long have you felt this way?",
    "Mindwell is a safe space for you."
];

function initUser() {
    if (!localStorage.getItem('mindwell_user')) {
        localStorage.setItem('mindwell_user', JSON.stringify(defaultUser));
    }
    if (!localStorage.getItem('mindwell_history')) {
        localStorage.setItem('mindwell_history', JSON.stringify([]));
    }
    if (!localStorage.getItem('mindwell_journal')) {
        localStorage.setItem('mindwell_journal', JSON.stringify([]));
    }
}

function getUser() {
    return JSON.parse(localStorage.getItem('mindwell_user'));
}

function saveUser(user) {
    localStorage.setItem('mindwell_user', JSON.stringify(user));
    updateUI();
}

function updateUI() {
    const user = getUser();
    document.querySelectorAll('.data-user-name').forEach(el => el.textContent = user.name);
    document.querySelectorAll('.data-user-streak').forEach(el => el.textContent = user.streak);
    document.querySelectorAll('.data-user-points').forEach(el => el.textContent = user.points);
    document.querySelectorAll('.data-user-tree-level').forEach(el => el.textContent = user.tree_level);
    document.querySelectorAll('.data-quest-title').forEach(el => el.textContent = user.current_quest.title);
    document.querySelectorAll('.data-quest-desc').forEach(el => el.textContent = user.current_quest.description);
}

// Routing
function handleRoute() {
    let hashStr = window.location.hash.replace('#', '') || 'index';
    
    // Extract base hash and query params
    let hash = hashStr.split('?')[0];

    // Force login check
    const user = getUser();
    if (user.name === 'Guest' && hash !== 'index') {
        window.location.hash = '#index';
        return;
    }

    // Handle sub-routes like #assessment-phq9
    if (hash.startsWith('assessment-')) {
        hash = 'assessment'; // We'll just show the generic assessment view for the prototype
    }

    // Hide/show navbar
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        navbar.style.display = (hash === 'index') ? 'none' : 'flex';
    }

    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active');
    });

    const targetView = document.getElementById(`view-${hash}`);
    if (targetView) {
        targetView.classList.add('active');
    } else {
        document.getElementById('view-index').classList.add('active');
    }
    
    updateUI();
}

// Setup Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    initUser();
    
    // Check if we need to show garden
    if (window.location.hash.includes('show_garden=1')) {
        const modal = document.getElementById('gardenModal');
        if (modal) {
            modal.style.display = 'flex';
            setTimeout(() => {
                modal.style.opacity = '1';
                modal.querySelector('.card').style.transform = 'scale(1)';
            }, 10);
        }
    }

    window.addEventListener('hashchange', handleRoute);
    handleRoute();

    // Initialize Mock Users Database
    if (!localStorage.getItem('mindwell_users')) {
        localStorage.setItem('mindwell_users', JSON.stringify([]));
    }

    // Auth Form Intercept (Simulated Login/Signup for static prototype)
    const authForm = document.getElementById('authForm');
    if (authForm) {
        authForm.addEventListener('submit', (e) => {
            // Only intercept if we are in the static prototype (hash routing active)
            if (window.location.protocol === 'file:' || !window.location.host.includes('5000')) {
                e.preventDefault();
                const action = document.getElementById('authAction').value;
                const username = authForm.querySelector('input[name="username"]').value;
                const email = authForm.querySelector('input[name="email"]') ? authForm.querySelector('input[name="email"]').value : '';
                
                let users = JSON.parse(localStorage.getItem('mindwell_users'));
                let userObj = null;

                if (action === 'register') {
                    if (users.find(u => u.username === username || (email && u.email === email))) {
                        alert("Username or email already exists!");
                        return;
                    }
                    userObj = { ...defaultUser, name: username, email: email, id: Date.now() };
                    users.push(userObj);
                    localStorage.setItem('mindwell_users', JSON.stringify(users));
                } else if (action === 'login') {
                    userObj = users.find(u => u.username === username);
                    if (!userObj) {
                        alert("Invalid credentials.");
                        return;
                    }
                } else if (action === 'google_mock') {
                    userObj = users.find(u => u.email === 'google_mock@example.com');
                    if (!userObj) {
                        userObj = { ...defaultUser, name: 'GoogleUser', email: 'google_mock@example.com', id: Date.now() };
                        users.push(userObj);
                        localStorage.setItem('mindwell_users', JSON.stringify(users));
                    }
                }

                if (userObj) {
                    userObj.points += 10; // Login reward
                    saveUser(userObj);
                    
                    // Also update users array
                    const userIndex = users.findIndex(u => u.id === userObj.id);
                    if (userIndex > -1) {
                        users[userIndex] = userObj;
                        localStorage.setItem('mindwell_users', JSON.stringify(users));
                    }
                    
                    window.location.hash = '#dashboard?show_garden=1';
                }
            }
        });
    }

    const mockGoogleBtn = document.querySelector('.google-mock-btn');
    if (mockGoogleBtn) {
        mockGoogleBtn.addEventListener('click', () => {
            if (window.location.protocol === 'file:' || !window.location.host.includes('5000')) {
                document.getElementById('authAction').value = 'google_mock';
                if(authForm) {
                    authForm.dispatchEvent(new Event('submit'));
                }
            }
        });
    }

    // Chatbot functionality mock
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    if (chatInput && sendBtn) {
        sendBtn.addEventListener('click', handleChat);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') handleChat();
        });
    }
});

function handleChat() {
    const input = document.getElementById('chatInput');
    const msg = input.value.trim().toLowerCase();
    if (!msg) return;

    addMessage(msg, 'user');
    input.value = '';

    setTimeout(() => {
        let response = "";
        let found = false;
        for (const [key, answers] of Object.entries(keywords)) {
            if (msg.includes(key)) {
                response = answers[Math.floor(Math.random() * answers.length)];
                found = true;
                break;
            }
        }
        if (!found) {
            response = generics[Math.floor(Math.random() * generics.length)];
        }
        addMessage(response, 'bot');
    }, 1000);
}

function addMessage(text, sender) {
    const chatWindow = document.getElementById('chatWindow');
    if (!chatWindow) return;
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-message ${sender}-message`;
    msgDiv.innerHTML = `<div class="message-content">${text}</div>`;
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Assessment Logic
const assessmentData = {
    phq9: {
        title: "Depression Assessment (PHQ-9)",
        questions: [
            "Little interest or pleasure in doing things",
            "Feeling down, depressed, or hopeless",
            "Trouble falling or staying asleep, or sleeping too much",
            "Feeling tired or having little energy",
            "Poor appetite or overeating",
            "Feeling bad about yourself - or that you are a failure or have let yourself or your family down",
            "Trouble concentrating on things, such as reading the newspaper or watching television",
            "Moving or speaking so slowly that other people could have noticed",
            "Thoughts that you would be better off dead, or of hurting yourself"
        ]
    },
    gad7: {
        title: "Anxiety Assessment (GAD-7)",
        questions: [
            "Feeling nervous, anxious, or on edge",
            "Not being able to stop or control worrying",
            "Worrying too much about different things",
            "Trouble relaxing",
            "Being so restless that it is hard to sit still",
            "Becoming easily annoyed or irritable",
            "Feeling afraid, as if something awful might happen"
        ]
    }
};

let currentAssessmentType = null;
let currentStep = 0;
let assessmentScores = [];

window.startAssessment = function(type) {
    currentAssessmentType = type;
    currentStep = 0;
    assessmentScores = [];
    
    const data = assessmentData[type];
    document.getElementById('assessmentTitle').textContent = data.title;
    document.getElementById('assessmentFormContainer').style.display = 'block';
    
    const container = document.getElementById('questionContainer');
    container.innerHTML = '';
    
    data.questions.forEach((q, index) => {
        const div = document.createElement('div');
        div.className = 'question-step fade-in';
        div.id = `qstep-${index}`;
        div.style.display = index === 0 ? 'block' : 'none';
        
        div.innerHTML = `
            <h2 style="font-size: 1.5rem; margin-bottom: 2rem; min-height: 80px;">${index + 1}. ${q}</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div class="option-card" onclick="selectOption(${index}, 0)">
                    <span style="font-size: 2rem;">🙂</span><p>Not at all</p>
                </div>
                <div class="option-card" onclick="selectOption(${index}, 1)">
                    <span style="font-size: 2rem;">😐</span><p>Several days</p>
                </div>
                <div class="option-card" onclick="selectOption(${index}, 2)">
                    <span style="font-size: 2rem;">😟</span><p>More than half</p>
                </div>
                <div class="option-card" onclick="selectOption(${index}, 3)">
                    <span style="font-size: 2rem;">😫</span><p>Nearly every day</p>
                </div>
            </div>
        `;
        container.appendChild(div);
    });
    
    document.getElementById('totalQ').textContent = data.questions.length;
    updateProgress();
    document.getElementById('submitBtn').style.display = 'none';
};

window.selectOption = function(qIndex, value) {
    assessmentScores[qIndex] = value;
    const data = assessmentData[currentAssessmentType];
    
    const currentStepDiv = document.getElementById(`qstep-${currentStep}`);
    if (currentStep < data.questions.length - 1) {
        setTimeout(() => {
            currentStepDiv.style.display = 'none';
            currentStep++;
            document.getElementById(`qstep-${currentStep}`).style.display = 'block';
            updateProgress();
        }, 300);
    } else {
        setTimeout(() => {
            currentStepDiv.style.display = 'none';
            document.getElementById('submitBtn').style.display = 'block';
            updateProgress();
        }, 300);
    }
};

function updateProgress() {
    const data = assessmentData[currentAssessmentType];
    if (!data) return;
    const totalSteps = data.questions.length;
    const percent = ((currentStep) / totalSteps) * 100;
    document.getElementById('progressBar').style.width = percent + '%';
    document.getElementById('currentQ').innerText = Math.min(currentStep + 1, totalSteps);
}

window.submitAssessment = function() {
    const score = assessmentScores.reduce((a, b) => (a || 0) + (b || 0), 0);
    let severity = "Mild";
    if (score > 10) severity = "Moderate";
    if (score > 15) severity = "Severe";
    
    const user = getUser();
    if (user.tree_level < 5) user.tree_level += 1;
    user.points += 50;
    saveUser(user);
    
    const history = JSON.parse(localStorage.getItem('mindwell_history') || '[]');
    history.push({
        id: Date.now(),
        type: currentAssessmentType,
        score: score,
        severity: severity,
        date: new Date().toISOString().split('T')[0]
    });
    localStorage.setItem('mindwell_history', JSON.stringify(history));
    
    // Update result view
    const scoreEls = document.querySelectorAll('#view-result .data-score');
    if (scoreEls.length) scoreEls.forEach(el => el.textContent = score);
    
    const sevEls = document.querySelectorAll('#view-result .data-severity');
    if (sevEls.length) sevEls.forEach(el => el.textContent = severity);
    
    window.location.hash = '#result';
};

