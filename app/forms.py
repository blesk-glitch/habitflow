from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirm', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


from wtforms import StringField, TextAreaField, DateField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Optional


class TaskForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[Optional()])
    due_date = DateField('Срок выполнения', format='%Y-%m-%d', validators=[DataRequired()])
    priority = SelectField('Приоритет', choices=[('low', 'Низкий'), ('medium', 'Средний'), ('high', 'Высокий')], default='medium')
    image = FileField('Изображение')
    submit = SubmitField('Сохранить')