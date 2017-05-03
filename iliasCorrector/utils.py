from iliasCorrector import app, db
from iliasCorrector.models import Exercise, Submission, File
from flask import g
from sqlalchemy import func

import os
import statistics


def import_grades(exercise, points):
    if os.path.isfile(points):
        with open(points) as f:
            for line in f:
                data = line.split(';')
                grade = data[1]
                remarks = data[2]
                if grade == '---':
                    grade = None
                if remarks.strip() == '-- keine Bemerkung --':
                    remarks = None

                submission = exercise.submissions.filter_by(student_ident=data[0]).first()
                if not submission:
                    submission = Submission(exercise_id=exercise.id,
                            student_ident=data[0], grade=0, remarks='-- keine Abgabe --')
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
    for submission in exercise.submissions.order_by(func.lower(Submission.student_ident)).all():
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
        lines.append(';'.join([submission.student_ident, grade, remarks]))
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
            submission = Submission(student_ident=students[i], exercise=exercise)
            db.session.add(submission)
            db.session.commit()
            for f in files[i + 1]:
                stored_file = File(submission=submission, name=f, path=root[i + 1])
                db.session.add(stored_file)
                db.session.commit()

        # import grades
        import_grades(exercise, os.path.join(path, 'points.csv'))


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
