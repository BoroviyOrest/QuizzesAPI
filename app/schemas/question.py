from typing import List, Optional, Union, Dict

from pydantic import BaseModel, HttpUrl, validator


class Question(BaseModel):
    description: str
    media: Optional[HttpUrl]
    type: str
    options: Optional[List[str]]

    @validator('type', pre=True)
    def validate_type(cls, value: str) -> str:
        if value not in ['text', 'radio', 'checkbox']:
            raise ValueError('"type" value must be one of those in list ["text", "radio", "checkbox"]')

        return value

    @validator('options', pre=True, always=True)
    def validate_option(cls, value: Optional[List[str]], values: Dict) -> Optional[List[str]]:
        answer_type = values.get('type')

        if answer_type in ['radio', 'checkbox'] and isinstance(value, list) is False:
            raise ValueError('"options" must be list when "type" is "radio" or "checkbox"')

        return value


class QuestionInDB(Question):
    answer: Union[int, str, List[int]]

    @validator('answer')
    def validate_answer(cls, answer: Union[int, str, List[int]], values: Dict) -> Union[int, str, List[int]]:
        answer_type = values.get('type')
        options = values.get('options')

        if answer_type == 'text':
            return str(answer)
        if answer_type == 'radio':
            try:
                answer = int(answer)
                if isinstance(options, list) and len(options) <= answer:
                    raise ValueError('Answer value is greater then options list length')
                return answer
            except TypeError:
                raise ValueError('Type value "radio" should have answers in type "int"')
        if answer_type == 'checkbox':
            if isinstance(answer, list) is False:
                raise ValueError('Type value "checkbox" should have answers in type "list"')

            for value in answer:
                if isinstance(options, list) and len(options) <= value:
                    raise ValueError('Answer value is greater then options list length')

            return answer


class QuestionInResponse(Question):
    pass
