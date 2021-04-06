import pytest
from fastapi.testclient import TestClient

from crud.quiz import QuizCRUD
from main import app


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
            },
            {
                'description': 'Question description',
                'media': None,
                'options': None,
                'type': 'text',
            }
        ]
    }


def test_get_quiz_by_post_id(monkeypatch, quiz_data, expected_data_in_response):
    async def mock_get(*args, **kwargs):
        return quiz_data

    monkeypatch.setattr(QuizCRUD, 'get_by_post_id', mock_get)

    with TestClient(app) as client:
        response = client.get('/post_quiz/123')
        assert response.status_code == 200
        assert response.json() == expected_data_in_response
