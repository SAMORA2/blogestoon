from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "نام کاربری", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("ایمیل", validators=[DataRequired(), Email()])
    password = PasswordField("پسورد", validators=[DataRequired()])
    confirm_password = PasswordField(
        "تایید پسورد", validators=[DataRequired(), EqualTo("password")]
    )

    submit = SubmitField("ثبت نام")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('این نام کاربری ثبت شده است')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError('این ایمیل ثبت شده است')


class LoginForm(FlaskForm):
    email = StringField("ایمیل", validators=[DataRequired(), Email()])
    password = PasswordField("پسورد", validators=[DataRequired()])
    remember = BooleanField("مرا به یاد داشته باش")
    submit = SubmitField("ورود")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "نام کاربری", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("ایمیل", validators=[DataRequired(), Email()])
    picture = FileField('ویرایش عکس پروفایل', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField("ویرایش")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('این نام کاربری ثبت شده است')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('این ایمیل ثبت شده است')


class RequestResetForm(FlaskForm):
    email = StringField("ایمیل", validators=[DataRequired(), Email()])
    submit = SubmitField('بازنشانی پسورد')

    def validate_email(self, email):

        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError('هیچ حساب کاربری با این ایمیل یافت نشد')


class ResetPasswordForm(FlaskForm):
    password = PasswordField("پسورد", validators=[DataRequired()])
    confirm_password = PasswordField(
        "تایید پسورد", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField('بازنشانی پسورد')
