__author__ = 'yousefhamza'

import os
import MySQLdb
from BeautifulSoup import BeautifulSoup

db = MySQLdb.connect("localhost", "root", "", "Fall_2014_Grades")

cursor = db.cursor()

special_credit_hours = {}

special_cr_file = open('Special_credit_hour_courses.csv', 'r')

for line in special_cr_file.readlines():
    data = line.strip('\n').strip('\r').split(',')[-2:]
    special_credit_hours[data[0].strip(' ')] = float(data[1])


#Grades and it's 4.0 scale
grades  = {
    "A+": 4.0,
    "A" : 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "E": 0.0,
    "F": 0.0,
    "P": 0.0,
    "W": 0.0
}

#Empty dictionary for courses
courses = {
}

ID  = 0

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

        if os.path.exists(department_directory):
            student_files = [html_files for html_files in os.listdir(department_directory) if html_files[0] != '.']

            for file in student_files:

                with open(department_directory+'/'+file, 'r') as content_file:
                    html_content = content_file.read()

                parsed_html = BeautifulSoup(html_content.decode('utf-8'))
                tables = parsed_html.findChildren('table')

                student_id = file[:7]
                student_name = parsed_html.find("span", {"id": "main_DataList2_StudentName_0"}).text

                table = tables[1]
                rows = table.findChildren('tr')

                number_of_courses = 0
                total_grades  = 0
                for row in rows:
                    cols = row.findChildren('td')
                    if len(cols)< 2:
                        continue

                    course_name = str(cols[0].text)
                    if(special_credit_hours.has_key(course_name)):
                        number_of_courses += (1*special_credit_hours[course_name])
                    else:
                        number_of_courses += 3

                    #Check if course already added to dictionary or not
                    if(not courses.has_key(course_name)):
                        courses[course_name] = [0, 1, 0.0, 4.0, ID, 1]
                        ID += 1
                    else:
                        courses[course_name][1] = courses[course_name][1] + 1
                        courses[course_name][5] += 1

                    student_grade_for_course = grades[cols[1].text]

                    if (special_credit_hours.has_key(course_name)):
                        total_grades += student_grade_for_course*special_credit_hours[course_name]
                    else:
                        total_grades += student_grade_for_course * 3.0

                    course_average = courses[course_name][0]
                    course_counter = courses[course_name][1]
                    course_max = courses[course_name][2]
                    course_min = courses[course_name][3]

                    courses[course_name][2] = student_grade_for_course if student_grade_for_course > course_max else course_max
                    courses[course_name][3] = student_grade_for_course if student_grade_for_course < course_min else course_min

                    #average calculation on the go:
                    # new_average = (i-th element)/i + (old_average*(i-1)/i
                    courses[course_name][0] = grades[cols[1].text]/course_counter +\
                                              (course_average*(course_counter - 1))/course_counter

                    #insert into Courses table
                    sql = "INSERT INTO Courses(course_id, student_id, courses_grade)" \
                          "VALUES({0}, \"{1}\", {2});".format(int(courses[course_name][4]), student_id, student_grade_for_course)

                    try:
                       cursor.execute(sql)
                       db.commit()
                    except:
                       db.rollback()

                student_grade = total_grades/number_of_courses

                sql = "INSERT INTO Students(student_id, student_name, student_grade)" \
                      "VALUES(\"{0}\", \"{1}\", {2});".format(student_id, student_name, student_grade)
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    db.rollback()


for course_name in courses.keys():
    sql = "INSERT INTO Courses_info(course_id, course_name, course_average, course_max, course_min, number_of_students)" \
          "VALUES({0}, \"{1}\", {2}, {3}, {4}, {5});".format(courses[course_name][4], course_name, courses[course_name][0],
                                                     courses[course_name][2], courses[course_name][3],
                                                     courses[course_name][5])
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

db.close()
