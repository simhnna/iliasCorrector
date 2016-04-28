from iliasCorrector import app, db
from iliasCorrector.models import Student, Exercise, Submission, File
from flask import g
from sqlalchemy import func

import os
import statistics


def import_grades(exercise, points):
    with open(points) as f:
        for line in f:
            data = line.split(';')
            matr = int(data[0].split('_')[-1])
            grade = data[1]
            remarks = data[2]
            if grade == '---':
                grade = None
            if remarks.strip() == '-- keine Bemerkung --':
                remarks = None

            submission = exercise.submissions.join(Student).filter(Student.matriculation_nr == matr).first()
            if not submission:
                student = Student.query.filter_by(matriculation_nr=matr).first()
                if not student:
                    student_data = data[0].split('_')
                    last = student_data[0]
                    first = ' '.join(student_data[1:-2])
                    student = Student(first_name=first, last_name=last, ident=data[0], matriculation_nr = matr)
                    db.session.add(student)
                    db.session.commit()
                submission = Submission(exercise_id=exercise.id,
                        student_id=student.id, grade=0, remarks='-- keine Abgabe --')
                db.session.add(submission)
                db.session.commit()
                continue

            if grade or remarks:
                submission.remarks = remarks or submission.remarks
                submission.grade = float(grade or '0') or submission.grade
                db.session.add(submission)
                db.session.commit()


def export_grades(exercise):
    lines = []
    for submission in exercise.submissions.join(Student).order_by(func.lower(Student.ident)).all():
        grade = submission.grade
        if grade:
            grade = str(grade)
        else:
            grade = '---'
        remarks = submission.remarks
        if remarks:
            remarks = remarks.strip()
            remarks.replace('\n', '  ')
        else:
            remarks = '-- keine Bemerkung --'
        lines.append(';'.join([submission.student.ident, grade, remarks]))
    return lines


def update_exercises():
    exercises = next(os.walk(os.path.join(app.config['BASE_DIR'], 'data')))[1]
    for exercise in exercises:
        if Exercise.query.filter_by(name=exercise).first() is not None:
            continue
        path = os.path.join(app.config['BASE_DIR'], 'data', exercise)
        root =  [x[0] for x in os.walk(path)]
        dirs = next(os.walk(path))[1]
        files = [x[2] for x in os.walk(path)]

        exercise_path = root[0]
        exercise_name = root[0].split('/')[-1]
        students = [x for x in dirs]

        if len(students) < 1:
            continue

        exercise = Exercise(name=exercise_name, path=exercise_path)
        db.session.add(exercise)
        db.session.commit()
        for i in range(len(students)):
            student_data = students[i].split('_')
            matr = int(students[i].split('_')[-1])
            last = student_data[0]
            first = ' '.join(student_data[1:-2])

            student = Student.query.filter_by(matriculation_nr=int(matr)).first()
            if not student:
                student = Student(first_name=first, last_name=last, matriculation_nr=int(matr), ident=students[i])
                db.session.add(student)
                db.session.commit()
            submission = Submission(student=student, exercise=exercise)
            db.session.add(submission)
            db.session.commit()
            for f in files[i + 1]:
                stored_file = File(submission=submission, name=f, path=root[i + 1])
                db.session.add(stored_file)
                db.session.commit()

        # import grades
        import_grades(exercise, os.path.join(path, 'points.csv'))


def get_exercises():
    return next(os.walk(os.path.join(app.config['BASE_DIR'], 'groups')))[1]


def get_groups(exercise):
    return next(os.walk(os.path.join(app.config['BASE_DIR'], 'groups', exercise)))[2]


def get_students(exercise, group):
    students = []
    with open(os.path.join(app.config['BASE_DIR'], 'groups', exercise, group)) as f:
        for line in f:
            data = line.strip().split(';')
            for i in range(len(data)):
                if not data[i]:
                    data[i] = 0
            students.append(data)
    return students


def submission_median(submissions):
    grades = list(filter((None).__ne__, [s.grade for s in submissions]))
    if grades:
        return statistics.median(grades)
    return "Can't be determined yet"

def submission_mean(submissions):
    grades = list(filter((None).__ne__, [s.grade for s in submissions]))
    if grades:
        return statistics.mean(grades)
    return "Can't be determined yet"

def split_ident(ident):
    data = ident.split('_')
    matr = int(data[-1])
    last = data[0]
    first = ' '.join(data[1:-2])
    return first, last, matr
