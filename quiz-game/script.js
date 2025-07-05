const quizData = [
  {
    type: "single",
    question: "In which year did the movie Kalki 2898 AD. release?",        
    options: ["2023", "2025", "2024", "2022"],
    answer: "2024"
  },
  {
    type: "multi",
    question: "Select all fruits:",
    options: ["Carrot", "Banana", "Apple", "Broccoli"],
    answer: ["Banana", "Apple"]
  },
  {
    type: "fill",
    question: "Fill in the blank: Water freezes at _____ degrees Celsius.",
    answer: "zero"
  },
  {
   type: "single",
    question: "Telangana film awards are called?",
    options: ["Nandi Filmfare", "Dadasaheb Phaike", "Gaddar Filmfare Awards", "Best Filmfare"],
    answer: "Gaddar Filmfare Awards"
  },
];

const quizContainer = document.getElementById('quiz');
const resultsContainer = document.getElementById('results');
const submitButton = document.getElementById('submit');

function buildQuiz() {
  const output = [];

  quizData.forEach((currentQuestion, questionNumber) => {
    let answers = "";

    if (currentQuestion.type === "single") {
      currentQuestion.options.forEach(option => {
        answers += `
          <label>
            <input type="radio" name="question${questionNumber}" value="${option}">
            ${option}
          </label><br>`;
      });
    } else if (currentQuestion.type === "multi") {
      currentQuestion.options.forEach(option => {
        answers += `
          <label>
            <input type="checkbox" name="question${questionNumber}" value="${option}">
            ${option}
          </label><br>`;
      });
    }  else if (currentQuestion.type === "single") {
      currentQuestion.options.forEach(option => {
        answers += `
          <label>
            <input type="radio" name="question${questionNumber}" value="${option}">
            ${option}
          </label><br>`;
      });
    } else if (currentQuestion.type === "fill") {
      answers = `<input type="text" name="question${questionNumber}" />`;
    }

    output.push(`
      <div class="question"> ${questionNumber + 1}. ${currentQuestion.question} </div>
      <div class="answers"> ${answers} </div>
    `);
  });

  quizContainer.innerHTML = output.join('');
}

function showResults() {
  let score = 0;

  quizData.forEach((currentQuestion, questionNumber) => {
    const selector = `input[name=question${questionNumber}]`;
    const answersContainer = quizContainer.querySelectorAll(selector);

    if (currentQuestion.type === "single") {
      const selected = quizContainer.querySelector(`${selector}:checked`);
      if (selected && selected.value === currentQuestion.answer) {
        score++;
      }
    } else if (currentQuestion.type === "multi") {
      const selected = [];
      answersContainer.forEach(input => {
        if (input.checked) selected.push(input.value);
      });

      const correctAnswers = currentQuestion.answer;
      const isCorrect =
        selected.length === correctAnswers.length &&
        selected.every(a => correctAnswers.includes(a));

      if (isCorrect) score++;
    } else if (currentQuestion.type === "fill") {
      const input = quizContainer.querySelector(selector);
      if (input && input.value.trim().toLowerCase() === currentQuestion.answer.toLowerCase()) {
        score++;
      }
    }
  });

  resultsContainer.innerHTML = `Your score is ${score} out of ${quizData.length}`;
}

buildQuiz();

submitButton.addEventListener('click', showResults);
