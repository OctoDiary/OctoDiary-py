from ...model import Type


class Subject(Type):
    subject_id: int
    subject_name: str

class SubjectList(Type):
    payload: list[Subject]
