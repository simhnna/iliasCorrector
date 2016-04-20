from flask import render_template, flash, redirect, url_for, request, send_from_directory, make_response
from iliasCorrector import app, db
from iliasCorrector.models import Exercise, Submission, File, Student
from iliasCorrector import utils
from werkzeug import secure_filename
from sqlalchemy import func
import os


@app.route('/')
def index():
    exercises = Exercise.query.all()
    return render_template('index.html', exercises=exercises)


@app.route('/exercise/<exercise_id>/')
def exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    submissions = exercise.submissions.join(Student).order_by(func.lower(Student.ident))
    return render_template('exercise.html', exercise=exercise, submissions=submissions)


def get_next_submission(exercise_id, ident=''):
    exercise = Exercise.query.filter_by(id=exercise_id).first()
    return exercise.submissions.filter_by(grade=None).join(Student).order_by(
            func.lower(Student.ident)).filter(Student.ident > ident).first()


@app.route('/exercise/<exercise_id>/submission/')
@app.route('/exercise/<exercise_id>/submission/<submission_id>/', methods=['GET', 'POST'])
def submission(exercise_id=None, submission_id=None):
    if not submission_id:
        submission = get_next_submission(exercise_id)
        return redirect(url_for('submission', exercise_id=exercise_id, submission_id=submission.id))
    submission = Submission.query.get_or_404(submission_id)
    next_submission = get_next_submission(exercise_id,
                                          submission.student.ident)
    if request.method == 'POST':
        grade = request.form.get('grade', None)
        remarks = request.form.get('remarks', '')
        flash('Successfully graded {} with {} points'.format(submission.student, grade), 'success')
        submission.grade = grade
        submission.remarks = remarks.strip().replace(';', '-').replace('\r\n', ' -- ')
        db.session.add(submission)
        db.session.commit()
        if not next_submission:
            flash('Finished correcting submissions for exercise {}'.format(submission.exercise), 'success')
            return redirect(url_for('exercise', exercise_id=exercise_id))
        return redirect(url_for('submission', exercise_id=exercise_id, submission_id=next_submission.id))
    return render_template('submission.html', submission=submission,
                           next_submission=next_submission)


@app.route('/files/<file_id>/')
def file(file_id):
    f = File.query.get_or_404(file_id)
    return send_from_directory(f.path, f.name)


@app.route('/sync')
def update_exercises():
    utils.update_exercises()
    return "done"

@app.route('/exercise/<exercise_id>/export/')
def export_grades(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    response = make_response('\n'.join(utils.export_grades(exercise)))
    response.headers["Content-Disposition"] = "attachment; filename=points.csv"
    return response
