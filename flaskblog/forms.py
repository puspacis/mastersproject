from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username',
							validators=[DataRequired(), Length(min=3, max=10)])
	email = StringField('Email',
						 validators=[DataRequired(), Email()])
	password = PasswordField('Password',
							  validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
									  validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('username already taken.')

	def validate_email(self, email):
		email = User.query.filter_by(email=email.data).first()
		if email:
			raise ValidationError('email already taken.')


class LoginForm(FlaskForm):
	email = StringField('Email',
						 validators=[DataRequired(), Email()])
	password = PasswordField('Password',
							  validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
	username = StringField('Username',
							validators=[DataRequired(), Length(min=3, max=10)])
	email = StringField('Email',
						 validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
	submit = SubmitField('Update Account')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('username already taken.')

	def validate_email(self, email):
		if email.data != current_user.email:
			email = User.query.filter_by(email=email.data).first()
			if email:
				raise ValidationError('email already taken.')


class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Comment')