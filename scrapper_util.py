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


def view_results(use_cache: bool = False):
    """Shows the classes data result

    :param use_cache: should the results be taken from the cache? (if not it'll take from file)"""
    global student_classes

    if use_cache:
        classes = json.loads(json.dumps(student_classes, default=lambda o: o.__dict__))
    else:
        with open('result.json', 'r', encoding='utf8') as file:
            classes = json.load(file)

    def repeatstr(_string: str, count: int):
        """Repeats a string"""
        if count < 0:
            return _string

        temp = _string
        for i in range(1, count):
            _string += temp

        return _string

    # prettifies the string results
    for data in classes:
        print(repeatstr('-', 64))
        for key, value in data.items():
            if value is None:
                continue

            if key == 'class_code':
                key = 'Class Code'
            else:
                key = str(key).capitalize()

            if isinstance(value, dict):
                print(f'Meeting ID       : {value["id"]}')
                print(f'Meeting Password : {value["password"]}')
                print(f'Meeting URL      : {value["url"]}')
                continue

            spaces = repeatstr(' ', 17 - len(key))
            print(f'{key}{spaces}: {value}')

        print(repeatstr('-', 64))
        print('\n')
