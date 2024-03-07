const categorySelect = document.getElementById('category');
const difficultySelect = document.querySelector('select[name="difficulty"]');
const availableQuestionsElement = document.getElementById('available_questions');

const difficulties = ["easy", "medium", "hard"];
const questionCounts = {
  easy: 0,
  medium: 0,
  hard: 0,
};

async function updateMaxQuestions() {
  const categoryId = categorySelect.selectedOptions[0].value;

  if (categoryId !== "") {
    const response = await fetch(`https://opentdb.com/api_count.php?category=${categoryId}`);
    const data = await response.json();

    if (data.category_question_count !== undefined) {
      for (const difficulty of difficulties) {
        questionCounts[difficulty] = data.category_question_count[`total_${difficulty}_question_count`];
      }

      // Zobrazení dat (opravená verze)
      const selectedDifficulty = difficultySelect.value;
      const selectedCount = questionCounts[selectedDifficulty];
      availableQuestionsElement.textContent = selectedCount;
    } else {
      console.error('Chyba: Objekt questionCounts je undefined.');
      // Zobrazte chybovou zprávu pro uživatele, pokud chcete
    }
  }
}

// Nastavení počátečních hodnot (bez appendChild)
for (const difficulty of difficulties) {
  const element = document.createElement('span');
  element.id = `available_${difficulty}`;
  element.textContent = "0";
  // availableQuestionsElement.appendChild(element); // Odebráno, předpokládám, že elementy jsou již v HTML
}

// Posluchač událostí
categorySelect.addEventListener('change', updateMaxQuestions);
difficultySelect.addEventListener('change', updateMaxQuestions);

// Spuštění úvodního načtení
updateMaxQuestions();