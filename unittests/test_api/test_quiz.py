from copy import copy

import pytest
from fastapi.testclient import TestClient

from app.main import app
from crud.quiz import QuizCRUD


@pytest.fixture
def expected_data_in_response():
    return {
        '_id': '6061ee7d0cdbf594cfa34114',
        'post_id': 123,
        'name': 'Quiz name',
        'description': 'Quiz description',
        'questions': [
            {
                'description': 'Question description',
                'media': None,
                'type': 'checkbox',
                'options': [
                    'option1',
                    'option2',
                    'option3',
                    'option4',
                    'option5'
                ],
                'answer': [1, 3]
            },
            {
                'description': 'Question description',
                'media': None,
                'type': 'radio',
                'options': [
                    'option1',
                    'option2',
                    'option3',
                    'option4',
                    'option5'
                ],
                'answer': 2
            },
            {
                'description': 'Question description',
                'media': None,
                'options': None,
                'type': 'text',
                'answer': 'Answer'
            }
        ]
    }


def test_get_all_quizzes(monkeypatch, quiz_data, expected_data_in_response):
    async def mock_get_many(*args, **kwargs):
        return [quiz_data]

    monkeypatch.setattr(QuizCRUD, 'get_many', mock_get_many)

    with TestClient(app) as client:
        response = client.get('/quiz/')
        assert response.status_code == 200
        assert response.json() == [expected_data_in_response]


def test_get_quiz_by_id(monkeypatch, quiz_data, expected_data_in_response):
    async def mock_get(*args, **kwargs):
        return quiz_data

    monkeypatch.setattr(QuizCRUD, 'get_by_id', mock_get)

    with TestClient(app) as client:
        response = client.get('/quiz/<some_id>')
        assert response.status_code == 200
        assert response.json() == expected_data_in_response


def test_create_quiz(monkeypatch, quiz_data, expected_data_in_response):
    async def mock_create(*args, **kwargs):
        return quiz_data

    monkeypatch.setattr(QuizCRUD, 'create', mock_create)

    with TestClient(app) as client:
        request_data = copy(quiz_data)
        request_data.pop('_id')
        response = client.post('/quiz/', json=request_data)

        assert response.status_code == 201
        assert response.json() == expected_data_in_response


def test_update_quiz(monkeypatch, quiz_data, expected_data_in_response):
    async def mock_update(*args, **kwargs):
        return quiz_data

    monkeypatch.setattr(QuizCRUD, 'update', mock_update)

    with TestClient(app) as client:
        request_data = copy(quiz_data)
        request_data.pop('_id')
        response = client.put('/quiz/<some_id>', json=request_data)

        assert response.status_code == 200
        assert response.json() == expected_data_in_response


def test_delete_quiz(monkeypatch):
    async def mock_delete(*args, **kwargs):
        return

    monkeypatch.setattr(QuizCRUD, 'delete', mock_delete)

    with TestClient(app) as client:
        response = client.delete('/quiz/<some_id>')
        assert response.status_code == 204
