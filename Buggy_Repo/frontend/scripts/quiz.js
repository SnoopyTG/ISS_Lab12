const BASE_URL = "http://localhost:8000";

let score = 0;
let highScore = 0;
let currentQuestion = null;
let gameOver = false;
let attemptHistory = [];
//hi
const scoreDisplay = document.getElementById("scoreDisplay");
const questionDiv = document.getElementById("question");
const form = document.getElementById("answerForm");
const feedback = document.getElementById("feedback");
const resetBtn = document.getElementById("resetBtn");
const attemptList = document.getElementById("attemptList");
const attemptCount = document.getElementById("attemptCount");
const searchInput = document.getElementById("search");

function updateScoreDisplay() {
  scoreDisplay.textContent = `Score: ${score} | High Score: ${highScore}`;
}

function updateAttempts() {
  const search = searchInput.value.toLowerCase();
  const filtered = attemptHistory.filter(a =>
    a.question.toLowerCase().includes(search)
  );

  attemptList.innerHTML = filtered.map(a => `
    <div>
      <strong>${a.question}</strong><br/>
      Your answer: ${a.answer} — ${a.result}
    </div>
  `).join("");

  attemptCount.textContent = `Total attempts: ${filtered.length}`;
}

function showError(message) {
  feedback.textContent = message;
  feedback.className = 'error';
  questionDiv.textContent = 'Failed to load question. Click Reset to try again.';
  form.innerHTML = '';
  resetBtn.classList.remove('hidden');
}

searchInput.addEventListener("input", updateAttempts);
// how is life ?
async function loadHighScore() {
  try {
    const res = await fetch(`${BASE_URL}/quiz/highscore`);
    if (!res.ok) {
      throw new Error(`Server returned ${res.status}: ${res.statusText}`);
    }
    const data = await res.json();
    highScore = data.high_score;
    updateScoreDisplay();
  } catch (error) {
    console.error('Failed to load high score:', error);
    showError(`Failed to load high score: ${error.message}`);
  }
}

async function loadQuestion() {
  if (gameOver) return;

  try {
    const res = await fetch(`${BASE_URL}/quiz/question`);
    if (!res.ok) {
      throw new Error(`Server returned ${res.status}: ${res.statusText}`);
    }
    const data = await res.json();
    currentQuestion = data;

    questionDiv.textContent = data.text;

    form.innerHTML = data.options.map(option => `
      <label>
        <input type="radio" name="answer" value="${option}" required>
        ${option}
      </label><br/>
    `).join("") + `<button type="submit">Submit</button>`;

    form.dataset.id = data.id;
    feedback.textContent = "";
    feedback.className = '';
  } catch (error) {
    console.error('Failed to load question:', error);
    showError(`Failed to load question: ${error.message}`);
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (gameOver) return;

  const selected = form.querySelector("input[name=answer]:checked");
  if (!selected) {
    feedback.textContent = "Please select an answer";
    feedback.className = 'error';
    return;
  }

  try {
    const answer = selected.value;
    const id = parseInt(form.dataset.id);

    const res = await fetch(`${BASE_URL}/quiz/answer`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id, answer, score })
    });

    if (!res.ok) {
      throw new Error(`Server returned ${res.status}: ${res.statusText}`);
    }

    const data = await res.json();

    attemptHistory.push({
      question: currentQuestion.text,
      answer,
      result: data.is_correct ? "✅ Correct" : `❌ Wrong (Correct: ${data.correct_answer})`
    });

    updateAttempts();

    if (data.is_correct) {
      score = data.score;
      highScore = data.high_score;
      updateScoreDisplay();
      feedback.textContent = "✅ Correct!";
      feedback.className = 'success';
      await loadQuestion();
    } else {
      feedback.textContent = `❌ Incorrect. Correct answer: ${data.correct_answer}. Game Over.`;
      feedback.className = 'error';
      gameOver = true;
      form.innerHTML = "";
      resetBtn.classList.remove("hidden");
    }
  } catch (error) {
    console.error('Failed to submit answer:', error);
    showError(`Failed to submit answer: ${error.message}`);
  }
});

resetBtn.addEventListener("click", () => {
  score = 0;
  gameOver = false;
  attemptHistory = [];
  updateScoreDisplay();
  updateAttempts();
  resetBtn.classList.add("hidden");
  feedback.className = '';
  loadQuestion();
});

window.addEventListener("DOMContentLoaded", async () => {
  await loadHighScore();
  loadQuestion();
});
