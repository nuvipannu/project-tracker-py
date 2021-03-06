"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (
        row[0], row[1], row[2])


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project_by_title":
            project_title = args[0]
            projects_by_title(project_title)

        elif command == "get_grade":
            github = args[0]
            title = args[1]
            get_grade(github, title)

        elif command == "give_grade":
            github = args[0]
            title = args[1]
            grade = args[2]
            give_grade(github, title, grade)

def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """INSERT INTO Students VALUES (?, ?, ?)"""
    db_cursor.execute(QUERY, (first_name, last_name, github))

    db_connection.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def projects_by_title(title):
    """Query for projects by title"""

    QUERY = """SELECT * FROM Projects WHERE title = ?"""
    db_cursor.execute(QUERY, (title,))

    results = db_cursor.fetchall()
    print results

def get_grade(github, title):
    """Query for a student's grade given a github username and project title."""

    QUERY = """SELECT grade FROM Grades WHERE student_github = ? AND project_title = ?"""
    db_cursor.execute(QUERY, (github, title))

    results = db_cursor.fetchall()
    print results

def give_grade(github, title, grade):
    """Give a grade to a student."""

    QUERY = """INSERT INTO Grades VALUES (?, ?, ?)"""
    db_cursor.execute(QUERY, (github, title, grade))

    db_connection.commit()
    print "Successfully added grade of %s for the github user %s" % (grade, github)

if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
