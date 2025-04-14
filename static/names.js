function submitQuiz() {
    const total = questions.length;
    let correct = 0;

    for (let i = 1; i <= total; i++) {
        const selected = document.querySelector(`input[name=q${i}]:checked`);
        const correctAns = document.getElementById(`answer_q${i}`).value;
        const options = document.querySelectorAll(`input[name=q${i}]`);

        options.forEach(option => {
            option.disabled = true; // disable further editing

            const label = option.parentElement;

            if (option.value === correctAns) {
                label.style.color = 'green';
            }

            if (selected && option === selected) {
                if (option.value === correctAns) {
                    correct++;
                } else {
                    label.style.color = 'red'; // mark wrong selected answer
                }
            }
        });
    }

    const resultBox = document.getElementById("resultBox");
    resultBox.innerHTML = `
        <h3>You answered ${correct} out of ${total} questions correctly.</h3>
        <button onclick="playAgain()" style="margin-top: 10px;">Play Again with Same Concept</button>
    `;
    resultBox.scrollIntoView({ behavior: 'smooth' });
}

function playAgain() {
    // redirect to same quiz again
    const urlParams = new URLSearchParams(window.location.search);
    const language = urlParams.get("language");
    const concept = urlParams.get("concept");

    if (language && concept) {
        window.location.href = `/quiz?language=${language}&concept=${concept}`;
    } else {
        alert("Missing quiz parameters!");
    }
}


