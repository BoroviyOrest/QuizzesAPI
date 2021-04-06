import pytest
from bson import ObjectId


@pytest.fixture(scope='session')
def quiz_data():
    return {
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
