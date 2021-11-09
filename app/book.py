from app import db


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True)
    total_pages = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        full_title = "{} {}".format(self.title, self.total_pages)
        return '<Book {}>'.format(full_title)
