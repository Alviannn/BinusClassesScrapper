import requests
from scrapper_util import *


def main():
    config = load_config()
    session = requests.session()

    with session.post('https://myclass.apps.binus.ac.id/Auth/Login', data={
        'Username': config['login']['username'],
        'Password': config['login']['password'],
        'btnSubmit': True
    }) as response:
        try:
            assert response.json()['Status']
        except:
            return print('Error: Failed to login to BINUS Classes site!')

    with session.get('https://myclass.apps.binus.ac.id/Home/GetViconSchedule') as response:
        result = response.json()

        for class_data in result:
            date = class_data['DisplayStartDate']
            time = class_data['StartTime'] + ' - ' + class_data['EndTime']

            code = class_data['ClassCode']
            delivery = class_data['DeliveryMode']
            course = class_data['CourseCode'] + ' - ' + class_data['CourseTitleEn']

            week = class_data['WeekSession']
            session = class_data['CourseSessionNumber']

            meeting_url = class_data['MeetingUrl']
            meeting_id = class_data['MeetingId']
            meeting_password = class_data['MeetingPassword']

            student_class = StudentClass(date, time, code, delivery, course, week, session)
            if meeting_url != '-':
                meeting = MeetingInfo(meeting_id, meeting_password, meeting_url)
                student_class.meeting = meeting

            student_classes.append(student_class)


if __name__ == '__main__':
    main()
    save_results()
