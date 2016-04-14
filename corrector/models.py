from corrector import db


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    path = db.Column(db.String(256), unique=True)
    submissions = db.relationship('Submission', backref='exercise', lazy='dynamic')

    @property
    def num_corrected(self):
        return len(self.submissions.filter(Submission.grade != None).all())

    @property
    def num_submissions(self):
        return len(self.submissions.all())

    @property
    def num_to_correct(self):
        return len(self.submissions.filter_by(grade=None).all())

    def __repr__(self):
        return '<Exercise {}>'.format(self.name)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    matriculation_nr = db.Column(db.Integer, unique=True)
    ident = db.Column(db.String(256))
    submissions = db.relationship('Submission', backref='student', lazy='dynamic')

    def __repr__(self):
        return '<Student {}, {}>'.format(self.first_name, self.last_name)

    def __str__(self):
        return '{}, {}'.format(self.first_name, self.last_name)


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Integer)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    files = db.relationship('File', backref='submission', lazy='dynamic')
    remarks = db.Column(db.Text)

    def __repr__(self):
        return '<Submission of {} for exercise {}>'.format(self.student, self.exercise)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    path = db.Column(db.String(256))
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'))

    def __repr__(self):
        return '<File {}>'.format(self.name)
