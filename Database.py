from peewee import *
from Errors import Error
import datetime
import os

error = Error()
db = SqliteDatabase('WorkLog.db')


class Entry(Model):

    class Meta:
        database = db


class User(Entry):
    Employee = CharField()
    Task = CharField()
    Time = IntegerField()
    Notes = TextField()
    Date = DateField()


# DONE NEEDS COMMENTS
def initialize():
    db.connect()
    db.create_tables([User], safe=True)


# DONE NEEDS COMMENTS
def close():
    db.close()


# DONE NEEDS COMMENTS
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# DONE NEEDS COMMENTS
def add_entry():

    employee = error.empty_string_error()
    task = error.empty_task_error()
    time = error.time_spent_error()
    notes = input("Input any additional notes (optional).\n>>")

    now = datetime.datetime.now()
    User.create(Employee=employee, Task=task, Time=time, Notes=notes, Date=now.strftime("%m/%d/%Y"))


# DONE NEEDS COMMENTS
def delete_entry(delete_list):
    for entry in User.select():
        if str(entry.Employee) == delete_list[0] and str(entry.Task) == delete_list[1] and str(entry.Time)\
             == delete_list[2] and str(entry.Notes) == delete_list[3] and str(entry.Date) == delete_list[4]:
                entry.delete_instance()


# DONE NEEDS COMMENTS
def edit_entry(edit_list, user_edit):
    for entry in User.select():
        if str(entry.Employee) == edit_list[0] and str(entry.Task) == edit_list[1] and str(entry.Time)\
             == edit_list[2] and str(entry.Notes) == edit_list[3] and str(entry.Date) == edit_list[4]:

                if user_edit == 1:
                    new_date = error.time_error()
                    entry.Date = new_date
                    entry.save()
                elif user_edit == 2:
                    new_name = error.empty_task_error()
                    entry.Task = new_name
                    entry.save()
                elif user_edit == 3:
                    new_time_spent = error.time_spent_error()
                    entry.Time = new_time_spent
                    entry.save()
                elif user_edit == 4:
                    new_notes = input("Input the notes here:\n>>")
                    entry.Notes = new_notes
                    entry.save()


# DONE NEEDS COMMENTS
def pull_entry(pull_id):
    to_pull = User.get(User.id == pull_id)
    pull_list = [to_pull.Employee, to_pull.Task, str(to_pull.Time), to_pull.Notes, to_pull.Date]
    return pull_list


# DONE NEEDS COMMENTS
def pull_dates():
    date_list = []
    for entry in User.select():
        date_list.append(entry.Date)
    output = set(date_list)
    final = list(output)
    return final


# DONE NEEDS COMMENTS
def pull_names():
    name_list = []
    for entry in User.select():
        name_list.append(entry.Employee)
    return name_list


# DONE NEEDS COMMENTS
def pull_dates1(date_object):
    date_list = []
    for entry in User.select():
        if entry.Date == date_object:
            date_list.append(pull_entry(entry.id))
    return date_list


# DONE NEEDS COMMENTS
def pull_time_spent(time_spent_object):
    time_list = []
    for entry in User.select():
        if entry.Time == time_spent_object:
            time_list.append(pull_entry(entry.id))
    return time_list


# DONE NEEDS COMMENTS
def pull_string(string_object):
    string_list = []
    for entry in User.select():
        if str(string_object).lower() in entry.Task.lower() or str(string_object).lower() in entry.Notes.lower():
            string_list.append(pull_entry(entry.id))
    return string_list


# DONE NEEDS COMMENTS
def pull_name(name_object):
    name_list = []
    for entry in User.select():
        if str(name_object).lower() == entry.Employee.lower():
            name_list.append(pull_entry(entry.id))
    return name_list


# DONE NEEDS COMMENTS
def pull_date_range(date1, date2):
    date_range_list = []
    for entry in User.select():
        if datetime.datetime.strptime(date1, '%m/%d/%Y') <= datetime.datetime.strptime(entry.Date, '%m/%d/%Y') <=\
           datetime.datetime.strptime(date2, '%m/%d/%Y'):
                date_range_list.append(pull_entry(entry.id))
    return date_range_list
