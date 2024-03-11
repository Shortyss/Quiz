import json
from logging import getLogger

from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect

from api import ApiClient
from viewer.models import Quiz, Category, Score

# Create your views here.

LOGGER = getLogger()


def index(request):
    try:
        quiz_options = ApiClient.get_quiz_options()
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
    quiz = Quiz.create_game(number_of_questions, difficulty, category)
    quiz.save_game()
    quiz_id = quiz.id
    print('start id: ', quiz_id)
    return redirect('/on_game?quiz_id=' + str(quiz_id), {'quiz_id': quiz_id})


def on_game(request):
    quiz_id = request.GET.get('quiz_id')
    quiz = Quiz.restore_game(quiz_id)

    if request.method == 'POST':
        answer = list(request.POST.get('answer'))
        if answer:
            quiz.check_answer(answer)

    if quiz.current_question > quiz.number_of_questions:
        result = Score(
            score=quiz.score,
        )
        result.save()
        print('on_game id', quiz_id)

        return redirect('/finish?quiz_id=' + str(quiz_id), {'quiz_id': quiz_id})

    try:
        question = quiz.get_question()

        if question:
            context = {'question': question, 'quiz_id': quiz_id}
            return render(request, 'game.html', context)
        else:
            return redirect('/finish?quiz_id=' + str(quiz_id), {'quiz_id': quiz_id})

    except (IndexError, json.JSONDecodeError) as e:
        return redirect('/finish?quiz_id=' + str(quiz_id), {'quiz_id': quiz_id})


def results(request):
    quiz_id = request.GET.get('quiz_id')
    quiz = Quiz.restore_game(quiz_id)
    if not quiz:
        return redirect('/finish')

    if request.method == 'POST':
        player_name = request.POST.get('player_name')
        score = request.POST.get('score')
        if player_name and score:
            Score.objects.create(player_name=player_name, score=score)
        return redirect('leaderboard')

    result = quiz.get_result()
    return render(request, 'results.html', {'quiz': quiz, 'result': result})


def save_score(request):
    if request.method == 'POST':
        player_name = request.POST.get('player_name')
        score = request.POST.get('score')
        if player_name and score:
            quiz_id = request.POST.get('quiz_id')
            quiz = Quiz.restore_game(quiz_id)
            if quiz:
                Score.objects.create(player_name=player_name, score=score)
                return redirect('leaderboard')
    return redirect('/')


def leaderboard(request):
    scores = Score.objects.order_by('-score')[:10]
    print('name: ', scores)
    return render(request, 'leaderboard.html', {'scores': scores})