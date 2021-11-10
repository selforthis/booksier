from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, length


class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), length(max=200)])
    total_pages = IntegerField('Pages', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_total_pages(self, total_pages):
        if total_pages.data < 1 or total_pages.data > 5000:
            raise ValidationError('The number of pages should be in the range [1, 5000].')
