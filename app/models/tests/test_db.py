import pytest
from bson import ObjectId
from pydantic import ValidationError

from models.db import DBModelMixin


@pytest.fixture
def id_data():
    return {'_id': '6061ee7d0cdbf594cfa34114'}


def test_db_model_mixin_correct_data(id_data):
    model = DBModelMixin(**id_data)
    assert model.id == ObjectId(id_data['_id'])


@pytest.mark.parametrize('data, exception', [
    ({'id': '6061ee7d0cdbf594cfa34114'}, ValueError),
    ({'_id': 'incorrect_object_id'}, ValidationError)
])
def test_db_model_mixin_incorrect_data(data, exception):
    with pytest.raises(exception):
        DBModelMixin(**data)
