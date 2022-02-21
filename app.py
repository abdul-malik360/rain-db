#   create a database using sql
import sqlite3

#   flask
from flask import Flask, request, jsonify

#   created a db and called it Rain
connect = sqlite3.connect('Rain.db')
cursor = connect.cursor()

#   a table for rain employees
connect.execute("CREATE TABLE IF NOT EXISTS Rain_Employees(Employee_No INTEGER PRIMARY KEY AUTOINCREMENT,"
                "Fullname TEXT NOT NULL,"
                "Rain_Email TEXT NOT NULL UNIQUE,"
                "Password TEXT NOT NULL)")
#   close connection to db
connect.close()
#   to show table was created (console)
print("Rain Employee Table created Successfully")

#   starting to use flask
app = Flask(__name__)
app.debug = True    # when a bug is found, code continues to run


# routes to add and show data in Rain DB
@app.route('/', methods=["POST", "GET"])    # this route adds and gets info in db
def add_employee():
    response = {}

    #   adds data in route
    if request.method == "POST":
        fullname = request.json['Fullname']
        email = request.json['Rain_Email']
        password = request.json['Password']

        with sqlite3.connect("Rain.db") as connect:
            cursor = connect.cursor()
            cursor.execute("INSERT INTO Rain_Employees("
                           "Fullname,"
                           "Rain_Email,"
                           "Password) VALUES(?, ?, ?)", (fullname, email, password))
            connect.commit()
            response["message"] = "Successfully added Rain Employee"
            response["status_code"] = 201
        return response

    #   shows data in route
    if request.method == "GET":
        response = {}

        with sqlite3.connect("Rain.db") as connect:
            cursor = connect.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute("SELECT * FROM Rain_Employees")

            rain_employees_data = cursor.fetchall()

            rain_employees = []

            for employee in rain_employees_data:
                rain_employees.append({i: employee[i] for i in employee.keys()})

        response['status_code'] = 200
        response['rain_employees'] = rain_employees
        return response


#   to run api
if __name__ == '__main__':
    app.run()
