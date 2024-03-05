import json
import random
from dataclasses import dataclass, field
from typing import List

import requests

from django.db import models
from django.db.models import Model, TextChoices, CharField, IntegerField, DateTimeField, JSONField, ForeignKey
from django.http import request

from api import ApiClient

# Create your models here.
DIFFICULTY_CHOICES = (
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
)


@dataclass
class Question:
    category: str
    type: str
    difficulty: str
    question: str
    correct_answer: str
    incorrect_answers: List[str]
    answers: List[str] = field(default_factory=list, init=False)

    def check_answer(self, answer: str):
        return answer == self.correct_answer

    def __post_init__(self):
        self.answers.extend(self.incorrect_answers)
        self.answers.append(self.correct_answer)
        random.shuffle(self.answers)


class Category(Model):
    name = CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Quiz(Model):
    number_of_questions = IntegerField()
    category = IntegerField(default=0)
    difficulty = CharField(max_length=32, choices=DIFFICULTY_CHOICES)
    current_question = IntegerField(default=0)
    score = IntegerField(default=0)
    questions = JSONField()
    player_name = CharField(max_length=255, blank=True, null=True)

    @classmethod
    def create_game(cls, number_of_questions, difficulty, category):
        questions = ApiClient.get_questions(number_of_questions, category, difficulty)
        print('create question: ', questions)
        print('model questions: ', number_of_questions)
        print('Model category: ', category)
        print('model difficulty: ', difficulty)

        quiz = cls.objects.create(
            number_of_questions=number_of_questions,
            category=category,
            difficulty=difficulty,
            questions=questions,
        )
        print('create question2: ', quiz.questions)
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
        correct_answer = json.loads(self.questions)[self.current_question]["correct_answer"]
        if answer == correct_answer:
            self.score += 1

    def get_question(self):
        print('Otázky: ', self.questions)
        if not self.questions:
            raise IndexError("No questions remaining.")

        try:
            question = random.choice(self.question)
            print('question: ', question)
            return question

        except (IndexError, json.JSONDecodeError) as e:
            print(f"Error getting question: {e}")
            return None

    def get_result(self):
        return {'score': self.score, 'number_of_questions': self.number_of_questions}

    def stop_game(self, request):
        self.player_name = request.POST['player_name']
        self.save()


class Score(Model):
    player_name = CharField(max_length=255)
    score = IntegerField()
    timestamp = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player_name} - {self.score}"
