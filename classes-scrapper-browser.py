from time import sleep

from selenium import webdriver

from scrapper_util import *


def main():
    config = load_config()

    with webdriver.Edge(config['edge-driver-path'], keep_alive=True) as browser:
        browser.get('http://myclass.apps.binus.ac.id/')

        # attempts to login
        username = browser.find_element_by_id('Username')
        password = browser.find_element_by_id('Password')

        username.send_keys(config['login']['username'])
        password.send_keys(config['login']['password'])

        submit_btn = browser.find_element_by_id('btnSubmit')
        submit_btn.click()

        # waits until all classes are loaded
        timeout = 10
        while True:
            try:
                error_msg = browser.find_element_by_id('login_error').text
                if error_msg:
                    return print(f'Error: {error_msg}')
            except:
                pass

            try:
                span_list = browser.find_elements_by_tag_name('span')
                found = False

                for span in span_list:
                    if span.text == '*TBA - To be Announced':
                        found = True
                        break

                if found:
                    break
            except:
                pass

            sleep(1)
            timeout -= 1

            if timeout <= 0:
                return print('Error: Failed to load the BINUS classes table!')

        # grabs all existing classes info from the table
        class_table = browser.find_element_by_id('studentViconList') \
            .find_element_by_tag_name('tbody')

        # loops through all rows
        for row in class_table.find_elements_by_tag_name('tr'):
            class_atr = row.get_attribute('class')

            # ignore these class attributes
            if class_atr == 'trTemplate' or class_atr == 'loaderRow':
                continue

            # shortened the searcher
            find_class = row.find_element_by_class_name

            # grabs all class data
            date = find_class("iDate").text
            time = find_class("iTime").text

            class_code = find_class("iClass").text
            delivery = find_class("iDeliveryMode").text
            course = find_class("iCourse").text

            week = int(find_class("iWeek").text)
            session = int(find_class("iSession").text)

            meeting_id = find_class('iMeetingID').text
            meeting_pass = find_class('iMeetingPassword').text

            student_class = StudentClass(date, time, class_code, delivery, course, week, session)

            # determines if the meeting id exists or not, if not then append it straight away
            if meeting_id == '-' or meeting_pass == '-':
                student_classes.append(student_class)
                continue

            # otherwise creates the meeting info object and then append to the list afterwards
            zoom_link = find_class('iAction') \
                .find_element_by_tag_name('a') \
                .get_attribute('href')

            meeting = MeetingInfo(meeting_id, meeting_pass, zoom_link)
            student_class.meeting = meeting

            student_classes.append(student_class)


if __name__ == '__main__':
    main()
    save_results()
