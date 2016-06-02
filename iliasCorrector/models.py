from iliasCorrector import db

def _split_ident(ident):
    data = ident.split('_')
    matr = int(data[-1])
    last = data[0]
    first = ' '.join(data[1:-2])
    return first, last, matr

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


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Float)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    student_ident = db.Column(db.String(256))
    files = db.relationship('File', backref='submission', lazy='dynamic')
    remarks = db.Column(db.Text)

    def __repr__(self):
        return '<Submission of {} for exercise {}>'.format(self.student_ident,
                                                           self.exercise)
    @property
    def first_name(self):
        return _split_ident(self.student_ident)[0]

    @property
    def last_name(self):
        return _split_ident(self.student_ident)[1]

    @property
    def student(self):
        return '{}, {}'.format(self.last_name, self.first_name)

    @property
    def matriculation_number(self):
        return _split_ident(self.student_ident)[2]


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    path = db.Column(db.String(256))
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'))

    def __repr__(self):
        return '<File {}>'.format(self.name)
