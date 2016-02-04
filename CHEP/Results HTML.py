__author__ = 'yousefhamza'

import requests
from BeautifulSoup import BeautifulSoup
import os

def create_file(directory, file_name, content):
    if not os.path.exists(directory):
        os.makedirs(directory)
    html_file = open(directory +'/' + file_name, 'w+')
    html_file.write(content)
    html_file.close()

data = {
        "__VIEWSTATE": "/wEPDwUKMTE0MTgyMzA2MWRkTVT3/xXUSp16CSrB5hOgkWjC9UJYWp7C1QQJ18NLmAs=",
        "__EVENTVALIDATION": "/wEdAANPEvVgwxyl6IGKZicy6Ys5WdyjOOJja56tPh/KF/Iuy3b4zQ92ZI3W7mIN024CSE6ols1gh2Vbk4YBgq13T/zImD4GXfubMCmCpW1ift7jBg==",
        "__VIEWSTATEGENERATOR": "158BA121",
        "btnDisplayResults": "Show Results"
    }

input_filed_name = "txtID"

file_departments_data = open('department_data', 'w+')

files_directory = 'html_files'
for i in range(10, 15):
    if (i < 10):
        year_ID = '0' + str(i) + 'p'
        directory = files_directory + '/' + '0' + str(i)
    else:
        year_ID = str(i) + 'p'
        year_directory = files_directory + '/' +str(i)

    for j in range(1, 9):
        department_ID = year_ID + str(j)
        department_directory = year_directory + '/' + 'p' + str(j)
        last_ID = 0

        no_of_students =0
        for k in range(0, 1000):
            if ((k - last_ID) > 50):
                file_departments_data.write('Number of students at ' + department_ID + ' = ' + str(no_of_students) +'\n')
                break

            if (k < 10):
                student_ID = department_ID + '00' + str(k)
            elif (k < 100):
                student_ID = department_ID + '0' + str(k)
            else:
                student_ID = department_ID + str(k)

            data[input_filed_name] = student_ID

            response = requests.post("http://engasu.net/chepfall/Results.aspx", data = data)

            parsed_html = BeautifulSoup(response.text)
            tables = parsed_html.findChildren('table')

            #No grades table available = students grade not available
            if (len(tables) >= 2):
                create_file(department_directory, student_ID +'.html', response.text.encode('utf-8'))
                print 'Printed file for student ' + student_ID
                last_ID  = k
                no_of_students += 1
            else:
                print 'Student ' + student_ID + ' is not available'


file_departments_data.close()