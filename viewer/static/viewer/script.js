document.addEventListener("DOMContentLoaded", function() {

  const categorySelect = document.getElementById('category');
  const difficultySelect = document.querySelector('select[name="difficulty"]');
  const quantityInput = document.querySelector('input[name="quantity"]');
  const availableQuestionsElement = document.getElementById('available_questions');
  const startGameButton = document.getElementById('start_game_button');

  async function updateMaxQuestions() {
    const categoryId = categorySelect.selectedOptions[0].value;
    const difficulty = difficultySelect.value;
    const amount = quantityInput.value;

    console.log('Selected category:', categoryId);
    console.log('Selected difficulty:', difficulty);

    try {
      const response = await fetch(`https://opentdb.com/api.php?amount=${amount}&category=${categoryId}&difficulty=${difficulty}`);
      const data = await response.json();
      console.log(JSON.stringify(data));

      if (response.status === 429) {
        console.error('API limit exceeded. Try again later.');
        return;
      }

      if (data.response_code === 0) {
        const availableQuestions = data.results.length;
        availableQuestionsElement.textContent = availableQuestions;

        const enteredQuantity = parseInt(quantityInput.value);
        const isQuantityValid = !isNaN(enteredQuantity) && enteredQuantity <= availableQuestions;
        startGameButton.disabled = !isQuantityValid;
      } else if (data.response_code === 1) {
        availableQuestionsElement.textContent = 'Insufficient number of questions reduce the number.';
        startGameButton.disabled = true;
      } else {
        console.error('API error:', data.results[0].error);
        availableQuestionsElement.textContent = 'Error retrieving data.';
        startGameButton.disabled = true;
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      availableQuestionsElement.textContent = 'Error retrieving data.';
      startGameButton.disabled = true;
    }
  }

  categorySelect.addEventListener('change', updateMaxQuestions);
  difficultySelect.addEventListener('change', updateMaxQuestions);
  quantityInput.addEventListener('input', function(event) {
    setTimeout(function() {
        updateMaxQuestions(event);
        }, 700);
    });

  updateMaxQuestions();
});