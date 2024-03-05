import json
from dataclasses import dataclass, field
from logging import getLogger
from random import shuffle
from typing import List

from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect

from api import ApiClient
from viewer.models import Quiz, Category

# Create your views here.

LOGGER = getLogger()


def index(request):
    try:
        quiz_options = ApiClient.get_quiz_options()
        print('quiz options: ', quiz_options)
        return render(request, 'index.html', quiz_options)
    except ValueError:
        return render(request, 'error.html', {'error_message': "Error fetching quiz options."})


def start_game(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method. POST required.')

    try:
        number_of_questions = int(request.POST['quantity'])
    except ValueError:
        return HttpResponseBadRequest('Invalid number of questions. Must be an integer.')

    category = int(request.POST['category'])
    difficulty = request.POST['difficulty']
    print('start number of questions: ', number_of_questions)
    print('start difficulty: ', difficulty)
    print('start category: ', category)
    quiz = Quiz.create_game(number_of_questions, difficulty, category)
    quiz.save_game()
    quiz_id = quiz.id
    print('QUIZ ID: ', quiz_id)
    return redirect('/on_game?quiz_id=' + str(quiz_id), {'quiz_id': quiz_id})


def on_game(request):
    quiz_id = request.GET.get('quiz_id')
    print('QUIZ ID Restore: ', quiz_id)
    quiz = Quiz.restore_game(quiz_id)
    print('QUIZ on_game: ', quiz)
    print('QUIZ RESTORED')

    if request.method == 'POST':  # Zpracování odpovědi
        print('POST')
        answer = list(request.POST.get('answer'))
        if answer:
            quiz.check_answer(answer)

    try:
        print('TRY')
        question = quiz.get_question()
        print('question: ', question)

        if question:
            context = {'question': question, 'quiz_id': quiz_id}
            return render(request, 'game.html', context)
        else:
            return redirect('/results')

    except (IndexError, json.JSONDecodeError) as e:
        return redirect('/results')


def results(request):
    quiz = Quiz.restore_game(request)
    result = quiz.get_result()
    quiz.stop_game(request)
    return render(request, 'results.html', result)
