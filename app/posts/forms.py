from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('عنوان', validators=[DataRequired()])
    content = TextAreaField('متن', validators=[DataRequired()])
    submit = SubmitField('پست جدید')
