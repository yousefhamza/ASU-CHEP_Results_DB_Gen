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
        "__VIEWSTATE": "7NMw+ShG5zHDO8udtGkRKDwTGPBfLT7aX6Rc7NWyaeoR4syArDXi/ihLm525lLlHftU5lIo1Iy8r9MruLmzZPGvow4GZLxbDJuWr6x+HRIGQd6GAN1sOqjp6mhRG5ge7Dajh7L4pbhmft1PnNEqUETP1vryAeN9T0bGqZSQKbCurAC5uSq40JKax0el6GINaLlc1RzkxPDhQ7LLDlbwBEg8yur/3uI3nI36sBV2QDnhVgueMA97LQYwns3UxZ9ZoHB2EJyDj5vB9rJaqKOsrrIzy8415HsHVOVBgPhbBxz5szLbit5Qg8nqjVtkmsbNOc5dU3KpOS02Aha0IBLS3AfieLQXx3223f+qvmSm1HyxnDBL3sbj7BGnlCpuxAocRAr9y1oT6hyG2tsn/u9lhi6alBmQz9bxhNSOFzxypxoYFNazebJYGvTETQ3u70m61YI/nAav4tb18aggwUvEMVtx16EZaNTnHDl1gF/eZYoiXuYOaDghw077/p4Kg0bzDiQSwln3MsShxefqoTNfkZkhQHZ1zjk1c9MMlz5lM8l/8sv85JN/heZFp15qvdtIr5LF7pnZ+XE09JkbuNuNOdhQ6Ke8BowcTLuJ8ft6DhOrc19sJNpY4yP4jEkGzjc+mZXv1EIKkUH8hV3lTDLaEpiWOcRQl5S7Mzni/n5VsNBrmn7HQGCskdchlvwvzNd6er5b/YBxXtqtZMAYrKhKneKB+/jUjDauuyVcJJ8JyAgQeXq8KGZ6Xen4bciHMv3Dc4ERVUbdC8t9rK2ay76+2qmTwEOEIIWzq4nqlsWQ5vx1w5njhgDYn2q/4RHE+4ADoJk0VH+PiKM6kP43PTqiOo+5GVGPU3Q7ZTUEP+gIbpJojud+QeCY+3BYs52neoPWE1nJMBFfsnx4SG0hCkvHy0icZUZg/JFGxHl1I6xFqnPd133yLR6uoI4PIiVueBTFLgdzZ4HvMeV5cjc780IOtup58DSrxOdY44dEw8PcdVvgQpoX4/w2B2iS8vzMjXMMEq/v74bD+ooHnD0Vjl+7ciSXZ2BdiosHHtVtvLuGNGzE=",
        "__EVENTVALIDATION": "P69aUk7XIM6Zu5fUB6uuPtb9D4w5gwiPu/vY8uaxDu/pR56hy1ptEkFxmU8DV9eWi1AnosOA/QOJALoJ+yXhabeLRwMo5Us+J19TaoDImoTx7PBEqceGjDP+IVsXa6oY"
    }

input_filed_name = "ctl00$main$TextBox1"

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

            response = requests.post("http://chep.eng.asu.edu.eg/result/", data = data)

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