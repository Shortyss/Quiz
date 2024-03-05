from dataclasses import dataclass

from api import ApiClient

#
# class ChoseQuiz:
#     def __init__(self, category, difficulty, number_of_questions):
#         self.category = category
#         self.difficulty = difficulty
#         self.number_of_questions = number_of_questions
#
#     def chose_quiz(self):
#         ApiClient.get_quiz_options()
#
#
# class Question:
#     def __init__(self, question, answers, correct_answer):
#         self.question = question
#         self.answers = answers
#         self.correct_answer = correct_answer
#
#
# class Quiz:
#     def __init__(self, questions):
#         self.questions = questions
#         self.current_question = 0
#         self.score = 0
#
#     def next_question(self):
#         if self.current_question < len(self.questions):
#             self.current_question += 1
#             return self.questions[self.current_question - 1]
#         else:
#             return None
#
#     def check_answer(self, chosen_answer):
#         if chosen_answer == self.questions[self.current_question - 1].correct_answer:
#             self.score += 1
#
#
# class ScoreBoard:
#     def __init__(self):
#         pass
#
#     def save_score(self, name, score):
#         pass
#
#     def get_best_score(self, count=10):
#         pass
#
#
# class PlayerPosition:
#     def __init__(self, name, score, place):
#         self.name = name
#         self.score = score
#         self.place = place

