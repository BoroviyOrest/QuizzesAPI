from copy import copy

import pytest
from bson import ObjectId

from core.config import database_name
from core.exceptions import DatabaseResultException
from crud.quiz import QuizCRUD
from models.quiz import QuizInCreate

QUIZ_DATA = {
    '_id': ObjectId('6061ee7d0cdbf594cfa34114'),
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


class MockMongoDBClient:
    def __init__(self, on_error=False):
        self.__mocked_db = {database_name: MockMongoDBDatabase(on_error)}

    def __getitem__(self, item):
        return self.__mocked_db[item]


class MockMongoDBDatabase:
    def __init__(self, on_error=False):
        collection_class = MockMongoDBCollection if on_error is False else MockMongoDBCollectionException
        self.__mocked_collections = {'quizzes': collection_class()}

    def __getitem__(self, item):
        return self.__mocked_collections[item]


class MockMongoDBCollection:
    def __init__(self):
        self.quiz_data = copy(QUIZ_DATA)

    async def find_one(self, *args, **kwargs):
        return self.quiz_data

    def find(self, *args, **kwargs):
        return MockMongoDBCursor()

    async def insert_one(self, *args, **kwargs):
        return MockMongoDBInsertResult()

    async def find_one_and_update(self, *args, **kwargs):
        return self.quiz_data

    async def delete_one(self, *args, **kwargs):
        return MockMongoDBDeleteResult()


class MockMongoDBCollectionException:
    def __init__(self):
        self.quiz_data = copy(QUIZ_DATA)

    async def find_one(self, *args, **kwargs):
        return None

    async def find_one_and_update(self, *args, **kwargs):
        return None

    async def delete_one(self, *args, **kwargs):
        return MockMongoDBDeleteResultException()


class MockMongoDBCursor:
    async def to_list(self, *args, **kwargs):
        return [copy(QUIZ_DATA)]


class MockMongoDBInsertResult:
    def __init__(self):
        self.inserted_id = QUIZ_DATA['_id']


class MockMongoDBDeleteResult:
    def __init__(self):
        self.deleted_count = 1


class MockMongoDBDeleteResultException:
    def __init__(self):
        self.deleted_count = 0


def simulate_quiz_data_validation(data):
    simulated_data = copy(data)
    simulated_data['id'] = simulated_data.pop('_id')
    return simulated_data


@pytest.mark.asyncio
async def test_get_by_id_success():
    expected_quiz_data = simulate_quiz_data_validation(QUIZ_DATA)

    crud = QuizCRUD(MockMongoDBClient())
    result = await crud.get_by_id(QUIZ_DATA['_id'])
    assert result.dict() == expected_quiz_data


@pytest.mark.asyncio
async def test_get_by_id_no_documents():
    crud = QuizCRUD(MockMongoDBClient(on_error=True))
    with pytest.raises(DatabaseResultException):
        await crud.get_by_id(QUIZ_DATA['_id'])


@pytest.mark.asyncio
async def test_get_by_post_id_success():
    expected_quiz_data = simulate_quiz_data_validation(QUIZ_DATA)

    crud = QuizCRUD(MockMongoDBClient())
    result = await crud.get_by_post_id(QUIZ_DATA['post_id'])
    assert result.dict() == expected_quiz_data


@pytest.mark.asyncio
async def test_get_by_post_id_no_documents():
    crud = QuizCRUD(MockMongoDBClient(on_error=True))
    with pytest.raises(DatabaseResultException):
        await crud.get_by_post_id(QUIZ_DATA['post_id'])


@pytest.mark.asyncio
async def test_get_many_success():
    quiz_data = simulate_quiz_data_validation(QUIZ_DATA)
    expected_quiz_list_data = [quiz_data]

    crud = QuizCRUD(MockMongoDBClient())
    result = await crud.get_many()
    for quiz, expected_quiz_data in zip(result, expected_quiz_list_data):
        assert quiz.dict() == expected_quiz_data


@pytest.mark.asyncio
async def test_create_success():
    expected_quiz_data = simulate_quiz_data_validation(QUIZ_DATA)

    crud = QuizCRUD(MockMongoDBClient())
    result = await crud.create(QuizInCreate(**QUIZ_DATA))
    assert result.dict() == expected_quiz_data


@pytest.mark.asyncio
async def test_update_success():
    expected_quiz_data = simulate_quiz_data_validation(QUIZ_DATA)

    crud = QuizCRUD(MockMongoDBClient())
    result = await crud.update(QUIZ_DATA['_id'], QuizInCreate(**QUIZ_DATA))
    assert result.dict() == expected_quiz_data


@pytest.mark.asyncio
async def test_update_exception():
    crud = QuizCRUD(MockMongoDBClient(on_error=True))
    with pytest.raises(DatabaseResultException):
        await crud.update(QUIZ_DATA['_id'], QuizInCreate(**QUIZ_DATA))


@pytest.mark.asyncio
async def test_delete_success():
    crud = QuizCRUD(MockMongoDBClient())
    result = await crud.delete(QUIZ_DATA['_id'])
    assert result is None


@pytest.mark.asyncio
async def test_delete_exception():
    crud = QuizCRUD(MockMongoDBClient(on_error=True))
    with pytest.raises(DatabaseResultException):
        await crud.delete(QUIZ_DATA['_id'])
