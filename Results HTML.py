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
        "__VIEWSTATE": "/HUgraSKjKN9O/ZnCK18pQaLtXX7d0Hz33iWW5dXENCjMZdQfqZb6MzjTbtyFr1x6BkzRJAW3FKyFX5QqADWwbn8tHZEfdoaZ/rGteD2eReYF7X4f+yo61aBLCmD/A+lkHb1GJoErwNqfKCPqZ3HxhKsd4RI7WyiDVSh+nWiXxXTIRKtoYjjcYV/ceZTTAWxsB3bcAKKGjt9krNqlNnRA3/TdK1Ug4MiAL/VUSKcJpxX8T3JDZnd1uomyXkz9KxG9FvkHGPjLwDJjdfYijxskrFNYnAmDV4ydw2zgh8Cc51P1M/gCao6u643mBWifSD+iFwS9T/1BzUOmrBmdYL1E3bUPJiGFXqm5V8ZuX1dRXEso6oUiZYXrfIZM206Oq92xzaA/Nhm41bl2jLgq9X9EiRRfdiLCSfZMH1G0+kNQYr7CLBTkbXOGuI4ZgFPaUlbouNw5MLxXopDcbE0a/iCsoEZuVgHQuKFeF9hozSBJVWO6s4ft1Q/4ccwrbaojdO1rUHJVFclxHEJqDrv5Z3z7rtkUWRdEBCHALAjsr7nxOZ1Cvxg1a5PgrVoNLMuC/HF0OaTOsB9I9NghfJyWCY7yGxDsjjmyK7KuO0SIwxsIgGXFmsGWuGWMVtP5Le2FydRI1MN7sohEnowFO97AkS/mUb/O2YTEptsu1IydvFK/o6g4bi4Ton5I/T/7V+enjAO+9N1cCTQzSmm/PCt6RaQRQpOs7Ew79gkjxcXoz+B/fvee6ErvPlw9yPVjqLgxJR6xUjxwqZb6+9/7JHAezYClpQbpRlQpI2piRfhpqMIs4Qln6APT6qj6PFwZqEKmZKSIT/LFacxS4C9Zc6iPyOX7FcdufixLyhsGt0WasjpkDiSjQt/AEahxylO8BT+gTH+HEEA7Mr1BlqNz+LLkWe6oY1KuHHFuytG3oOGtODsJXfB5EcRpSJpzsdCcQzS24tUhg+uRD7/D0m9dz3zhdBWeF48fDfQssPNgLxNvoTjwE41m4BxAwAPV+MXdAHOfwhslRjv8ey/Cel1aC/xKdXIlh2HDXZXglNbxXbfd4lBdOA=",
        "__EVENTVALIDATION": "FIdAE24fUmSX9aotugdaq9czxle/pRZkJL9aIg+AVQTh1BG7x2uAnoHQrCCpFcnyf4WkZqdK6/XqQfVq9u77T9cFSbf2x0QVPr6agtQEpYOtoIdJzN6DLgUhwnxU/hxO"
    }

input_filed_name = "ctl00$main$TextBox1"

file_departments_data = open('department_data', 'w+')

files_directory = 'html_files'
for i in range(10, 11):
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