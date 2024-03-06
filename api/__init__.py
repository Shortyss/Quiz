from requests import get

DIFFICULTY = ('easy', 'medium', 'hard')
MAX_QUESTIONS = 50


class ApiClient:
    CATEGORIES_URL = "https://opentdb.com/api_category.php"
    QUESTIONS_URL = "https://opentdb.com/api.php?amount={}&category={}&difficulty={}"

    @classmethod
    def get_quiz_options(cls) -> dict:
        categories_response = get(ApiClient.CATEGORIES_URL)
        if categories_response.status_code == 200:
            categories = categories_response.json()['trivia_categories']
        else:
            categories = []

        return {'categories': categories, 'max_questions': MAX_QUESTIONS, 'difficulty': DIFFICULTY}

    @classmethod
    def get_questions(cls, max_questions: int, category: int, difficulty: str) -> dict:
        if int(max_questions) > MAX_QUESTIONS:
            max_questions = MAX_QUESTIONS

        print('difficulty API: ', difficulty)
        print('max questions API: ', max_questions)
        print('category API: ', category)
        response = get(ApiClient.QUESTIONS_URL.format(max_questions, category, difficulty))

        if response.status_code != 200:
            return {'error': 'Failed to get questions from API.'}

        return response.json()['results']

