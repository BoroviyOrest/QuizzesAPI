from copy import copy

import pytest

from core.config import database_name
from db.exceptions import DatabaseResultException
from crud.quiz import QuizCRUD


class MockMongoDBClient:
    def __init__(self, quiz_data, collection_class=None):
        self.__mocked_db = {database_name: MockMongoDBDatabase(quiz_data, collection_class)}

    def __getitem__(self, item):
        return self.__mocked_db[item]


class MockMongoDBDatabase:
    def __init__(self, quiz_data, collection_class=None):
        collection_class = collection_class or MockMongoDBCollection
        self.__mocked_collections = {'quizzes': collection_class(quiz_data)}

    def __getitem__(self, item):
        return self.__mocked_collections[item]


class MockMongoDBCollection:
    def __init__(self, quiz_data):
        self.quiz_data = quiz_data

    async def find_one(self, *args, **kwargs):
        return self.quiz_data

    def find(self, *args, **kwargs):
        return MockMongoDBCursor(self.quiz_data)

    async def insert_one(self, *args, **kwargs):
        return MockMongoDBInsertResult(self.quiz_data)

    async def find_one_and_update(self, *args, **kwargs):
        return self.quiz_data

    async def delete_one(self, *args, **kwargs):
        return MockMongoDBDeleteResult()


class MockMongoDBCollectionException:
    def __init__(self, quiz_data):
        self.quiz_data = quiz_data

    async def find_one(self, *args, **kwargs):
        return None

    async def find_one_and_update(self, *args, **kwargs):
        return None

    async def delete_one(self, *args, **kwargs):
        return MockMongoDBDeleteResultException()


class MockMongoDBCollectionCreateSuccess(MockMongoDBCollection):
    async def find_one(self, *args, **kwargs):
        return None


class MockMongoDBCursor:
    def __init__(self, quiz_data):
        self.quiz_data = quiz_data

    async def to_list(self, *args, **kwargs):
        return [self.quiz_data]


class MockMongoDBInsertResult:
    def __init__(self, quiz_data):
        self.inserted_id = quiz_data['_id']


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
async def test_get_success(quiz_data):
    expected_quiz_data = simulate_quiz_data_validation(quiz_data)

    crud = QuizCRUD(MockMongoDBClient(quiz_data))
    result = await crud.get(_id=quiz_data['_id'])
    assert result.dict() == expected_quiz_data


@pytest.mark.asyncio
async def test_get_no_documents(quiz_data):
    crud = QuizCRUD(MockMongoDBClient(quiz_data, collection_class=MockMongoDBCollectionCreateSuccess))
    with pytest.raises(DatabaseResultException):
        await crud.get(_id=quiz_data['_id'])


@pytest.mark.asyncio
async def test_get_many_success(quiz_data):
    expected_quiz_data = simulate_quiz_data_validation(quiz_data)
    expected_quiz_list_data = [expected_quiz_data]

    crud = QuizCRUD(MockMongoDBClient(quiz_data))
    result = await crud.get_many()
    for quiz_result, expected_quiz in zip(result, expected_quiz_list_data):
        assert quiz_result.dict() == expected_quiz


@pytest.mark.asyncio
async def test_create_success(quiz_data):
    crud = QuizCRUD(MockMongoDBClient(quiz_data, collection_class=MockMongoDBCollectionCreateSuccess))

    expected_quiz_data = simulate_quiz_data_validation(quiz_data)
    quiz_data = copy(quiz_data)
    quiz_data.pop('_id')

    result = await crud.create(quiz_data)
    assert result.dict() == expected_quiz_data


@pytest.mark.asyncio
async def test_create_post_id_exists(quiz_data):
    crud = QuizCRUD(MockMongoDBClient(quiz_data))

    quiz_data = copy(quiz_data)
    quiz_data.pop('_id')

    with pytest.raises(DatabaseResultException):
        await crud.create(quiz_data)


@pytest.mark.asyncio
async def test_update_success(quiz_data):
    crud = QuizCRUD(MockMongoDBClient(quiz_data))

    expected_quiz_data = simulate_quiz_data_validation(quiz_data)
    quiz_data = copy(quiz_data)
    quiz_id = quiz_data.pop('_id')
    result = await crud.update(quiz_id, quiz_data)
    assert result.dict() == expected_quiz_data


@pytest.mark.asyncio
async def test_update_exception(quiz_data):
    crud = QuizCRUD(MockMongoDBClient(quiz_data, collection_class=MockMongoDBCollectionException))

    quiz_data = copy(quiz_data)
    quiz_id = quiz_data.pop('_id')

    with pytest.raises(DatabaseResultException):
        await crud.update(quiz_id, quiz_data)


@pytest.mark.asyncio
async def test_delete_success(quiz_data):
    crud = QuizCRUD(MockMongoDBClient(quiz_data))
    result = await crud.delete(quiz_data['_id'])
    assert result is None


@pytest.mark.asyncio
async def test_delete_exception(quiz_data):
    crud = QuizCRUD(MockMongoDBClient(quiz_data, collection_class=MockMongoDBCollectionException))
    with pytest.raises(DatabaseResultException):
        await crud.delete(quiz_data['_id'])
