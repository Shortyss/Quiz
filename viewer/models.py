import json
import random

from django.db.models import Model, CharField, IntegerField, DateTimeField, JSONField
from django.http import request
from django.shortcuts import redirect, render

from api import ApiClient

# Create your models here.
DIFFICULTY_CHOICES = (
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
)


class Category(Model):
    name = CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Score(Model):
    player_name = CharField(max_length=255)
    score = IntegerField()
    timestamp = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player_name} - {self.score}"


class Quiz(Model):
    number_of_questions = IntegerField()
    category = IntegerField(default=0)
    difficulty = CharField(max_length=32, choices=DIFFICULTY_CHOICES)
    current_question = IntegerField(default=0)
    score = IntegerField(default=0)
    questions = JSONField(null=True, blank=True)
    player_name = CharField(max_length=255, blank=True, null=True)

    @classmethod
    def create_game(cls, number_of_questions, difficulty, category):
        questions = ApiClient.get_questions(number_of_questions, category, difficulty)

        quiz = cls.objects.create(
            number_of_questions=number_of_questions,
            category=category,
            difficulty=difficulty,
            questions=questions,
        )
        return quiz

    def save_game(self):
        self.save()

    @classmethod
    def restore_game(cls, quiz_id):
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
        except ValueError:
            return None
        return quiz

    def check_answer(self, answer):
        answer = ''.join(answer).strip()
        if self.current_question < len(self.questions):
            correct_answer = self.questions[self.current_question]['correct_answer'].strip()
            self.current_question += 1
            if answer == correct_answer:
                self.score += 1
                self.save()

        if self.current_question >= len(self.questions):
            return redirect('/finish')

    def get_question(self):
        if not self.questions:
            return redirect('/finish')

        try:
            question = self.questions[self.current_question]
            question["answers"] = question["incorrect_answers"] + [question["correct_answer"]]
            random.shuffle(question["answers"])
            self.current_question += 1
            return question

        except (IndexError, json.JSONDecodeError) as e:
            print(f"Error getting question: {e}")
            return None

    def get_result(self):
        return {'score': self.score, 'number_of_questions': self.number_of_questions}

    @classmethod
    def results(request):
        quiz_id = request.GET.get('quiz_id')
        if not quiz_id:
            return redirect('/')

        quiz = Quiz.restore_game(quiz_id)
        if not quiz:
            return redirect('/')

        result = quiz.get_result()
        quiz.stop_game()
        return render(request, 'results.html', {'result': result})

    def stop_game(self):
        self.save()

    def save_score(request):
        if request.method == 'POST':
            player_name = request.POST.get('player_name')
            score = int(request.POST.get('score'))
            if player_name and score:
                score_instance = Score(player_name=player_name, score=score)
                score_instance.save()
        return redirect('leaderboard')

    def leaderboard(request):
        scores = Score.objects.order_by('-score')[:10]
        return render(request, 'leaderboard.html', {'scores': scores})


