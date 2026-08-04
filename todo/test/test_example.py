import pytest

def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1

def test_is_instance():
    assert isinstance('this is a string', str)
    assert isinstance('10', str)
    # assert not isinstance(10, int)
    # assert isinstance('123'.encode('utf-8'), str)
    assert not isinstance('123'.encode('utf-8'), str)
    assert isinstance('123'.encode('utf-8'), bytes)

def test_boolean():
    validate = True
    assert validate is True
    assert ('hello' == 'world') is False

def test_type():
    assert type('hello') is str
    assert type('world') is not int

def test_greater_and_less_than():
    assert 7 > 3
    assert 4 < 10

def test_list():
    num_list = [1,2,3,4,5]
    any_list = [False, False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)

class Student:
    def __init__(self, first_name: str, last_name: str, major:str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_employee():
    return Student('jack','yao', 'computer science', 3)

def test_initialization():
    p = Student('jack','yao', 'computer science', 3)

    assert p.first_name == 'jack', 'First name should be jack'
    assert p.last_name == 'yao', 'Last name should be yao'
    assert p.major == 'computer science'
    assert p.years == 3

def test_fixture_initialization(default_employee):
    assert default_employee.first_name == 'jack', 'First name should be jack'
    assert default_employee.last_name == 'yao', 'Last name should be yao'
    assert default_employee.major == 'computer science'
    assert default_employee.years == 3
