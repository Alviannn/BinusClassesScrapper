import json

import yaml


class MeetingInfo:
    """The meeting information object"""
    id: str = None
    '''The meeting ID'''
    password: str = None
    '''The meeting password'''
    url: str = None
    '''The meeting zoom link'''

    def __init__(self, id, password, url):
        self.id = id
        self.password = password
        self.url = url


class StudentClass:
    """The student class object"""
    date: str = None
    '''The class date'''
    time: str = None
    '''The class time (starts and ends)'''
    class_code: str = None
    '''The class code name'''
    delivery: str = None
    '''The class delivery mode'''
    course: str = None
    '''The class course name'''
    week: int = None
    '''The class current week'''
    session: int = None
    '''The class current session'''
    meeting: MeetingInfo = None
    '''The class meeting information

    NOTE: Only exists if the class is a Video Conference type!'''

    def __init__(self, date, time, class_code, delivery, course, week, session):
        self.date = date
        self.time = time

        self.class_code = class_code
        self.delivery = delivery
        self.course = course

        self.week = week
        self.session = session

        self.meeting = None


student_classes = []


def load_config():
    """
    Reads the config.yml

    :return: the config object
    :rtype: dict
    """
    with open('config.yml', 'r') as stream:
        config = yaml.full_load(stream)

    return config


def save_results():
    """Saves the fetched classes"""

    # transforms the listed objects into a readable json
    dumped = json.dumps(student_classes, default=lambda o: o.__dict__, indent=4)
    # saves the result
    with open('result.json', 'w', encoding='utf8') as file:
        file.write(dumped)
