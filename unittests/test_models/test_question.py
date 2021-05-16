import pytest
from pytest_cases import parametrize_with_cases
from pydantic import ValidationError

from models.quiz_question import TextQuestionInCreate, RadioQuestionInCreate, CheckboxQuestionInCreate


class IncorrectTextQuestionCases:
    base_question_data = {
        'description': 'Question description',
        'type': 'text',
        'answer': 'answer'
    }

    def case_incorrect_answer_type_list(self):
        question_data = self.base_question_data
        question_data['answer'] = [1, 2, 3]

        return question_data

    def case_incorrect_options(self):
        question_data = self.base_question_data
        question_data['options'] = [1, 2, 3]

        return question_data


class IncorrectRadioQuestionCases:
    base_question_data = {
        'description': 'Question description',
        'type': 'radio',
        'options': [
            'option1',
            'option2',
            'option3',
        ],
        'answer': 2
    }

    def case_incorrect_answer_type_str(self):
        question_data = self.base_question_data
        question_data['answer'] = 'answer'

        return question_data

    def case_incorrect_answer_type_list(self):
        question_data = self.base_question_data
        question_data['answer'] = [1, 2, 3]

        return question_data

    def case_incorrect_answer_value(self):
        question_data = self.base_question_data
        question_data['answer'] = len(question_data['options']) + 1

        return question_data


class IncorrectCheckboxQuestionCases:
    base_question_data = {
        'description': 'Question description',
        'type': 'checkbox',
        'options': [
            'option1',
            'option2',
            'option3',
        ],
        'answer': [1, 3]
    }

    def case_incorrect_answer_type_str(self):
        question_data = self.base_question_data
        question_data['answer'] = 'answer'

        return question_data

    def case_incorrect_answer_type_int(self):
        question_data = self.base_question_data
        question_data['answer'] = 1

        return question_data

    def case_incorrect_answer_value(self):
        question_data = self.base_question_data
        incorrect_answer_value = len(question_data['options']) + 1
        question_data['answer'] = [1, incorrect_answer_value]

        return question_data


@pytest.fixture
def text_question_in_create():
    return {
        'description': 'Question description',
        'media': None,
        'type': 'text',
        'options': None,
        'answer': 'Answer'
    }


@pytest.fixture
def radio_question_in_create():
    return {
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
    }


@pytest.fixture
def checkbox_question_in_create():
    return {
        'description': 'Question description',
        'media': 'https://www.example.com/images/123.jpg',
        'type': 'checkbox',
        'options': [
            'option1',
            'option2',
            'option3',
            'option4',
            'option5'
        ],
        'answer': [1, 3]
    }


def test_correct_text_question_in_create(text_question_in_create):
    model = TextQuestionInCreate(**text_question_in_create)
    assert model.dict() == text_question_in_create


def test_correct_radio_question_in_create(radio_question_in_create):
    model = RadioQuestionInCreate(**radio_question_in_create)
    assert model.dict() == radio_question_in_create


def test_correct_checkbox_question_in_create(checkbox_question_in_create):
    model = CheckboxQuestionInCreate(**checkbox_question_in_create)
    assert model.dict() == checkbox_question_in_create


@parametrize_with_cases('question_data', cases=IncorrectTextQuestionCases)
def test_text_question_in_create_validation_error(question_data):
    with pytest.raises(ValidationError):
        TextQuestionInCreate(**question_data)


@parametrize_with_cases('question_data', cases=IncorrectRadioQuestionCases)
def test_radio_question_in_create_validation_error(question_data):
    with pytest.raises(ValidationError):
        RadioQuestionInCreate(**question_data)


@parametrize_with_cases('question_data', cases=IncorrectCheckboxQuestionCases)
def test_checkbox_question_in_create_validation_error(question_data):
    with pytest.raises(ValidationError):
        CheckboxQuestionInCreate(**question_data)
