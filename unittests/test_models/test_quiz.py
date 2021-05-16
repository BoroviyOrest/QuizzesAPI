from copy import copy

import pytest
from pydantic import ValidationError

from models.quiz_question import QuestionInCreate
from models.quiz import QuizInCreate


class MockQuestion1:
    _question_type = 'test1'

    def __init__(self, *args, **kwargs):
        pass


class MockQuestion2:
    _question_type = 'test2'

    def __init__(self, *args, **kwargs):
        pass


class MockQuestion3:
    _question_type = 'test3'

    def __init__(self, *args, **kwargs):
        pass


QUESTION_MOCKS = [MockQuestion1, MockQuestion2, MockQuestion3]
BASE_QUIZ = {
    'post_id': 123,
    'name': 'Quiz name',
    'description': 'Quiz description',
    'questions': []
}


def test_correct_validate_questions(monkeypatch):
    def mock_get(*args, **kwargs):
        return QUESTION_MOCKS

    monkeypatch.setattr(QuestionInCreate, '__subclasses__', mock_get)
    data = copy(BASE_QUIZ)
    data['questions'] = [
        {
            'description': 'Question description',
            'type': 'test1',
            'answer': 'Answer'
        },
        {
            'description': 'Question description',
            'type': 'test2',
            'answer': 'Answer'
        },
        {
            'description': 'Question description',
            'type': 'test3',
            'answer': 'Answer'
        },
    ]

    result = QuizInCreate(**data)
    validated_questions = result.questions
    for question, mock_class in zip(validated_questions, QUESTION_MOCKS):
        assert isinstance(question, mock_class)


def test_validate_questions_question_type_dont_exist(monkeypatch):
    def mock_get(*args, **kwargs):
        return QUESTION_MOCKS

    monkeypatch.setattr(QuestionInCreate, '__subclasses__', mock_get)
    data = copy(BASE_QUIZ)
    data['questions'] = [
        {
            'description': 'Question description',
            'type': 'incorrect',
            'answer': 'Answer'
        },
        {
            'description': 'Question description',
            'type': 'test2',
            'answer': 'Answer'
        },
        {
            'description': 'Question description',
            'type': 'test3',
            'answer': 'Answer'
        },
    ]
    with pytest.raises(ValidationError):
        QuizInCreate(**data)
