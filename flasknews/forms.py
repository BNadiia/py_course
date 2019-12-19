from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flasknews.models import User, CKTextAreaField
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign up')

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user:
			raise ValidationError('That username is taken. Choose a different one, please.')

	def validate_email(self, field):
		user = User.query.filter_by(email = field.data).first()
		if user:
			raise ValidationError('Email is already registered.')



class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('About Me')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    old_pass = PasswordField('Old password')
    new_pass = PasswordField('New password')
    confirm_pass = PasswordField('Confirm password', validators=[EqualTo('new_pass')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one')




class AdminUserCreateForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    role = SelectField(u'Role',  choices=[('admin', 'Admin'), ('moderator', 'Moderator'), ('user', 'User')])
    submit = SubmitField('Create')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Choose a different one, please.')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Email is already registered.')


class AdminUserUpdateForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    role = SelectField(u'Role', choices=[('admin', 'Admin'), ('moderator', 'Moderator'), ('user', 'User')])
    submit = SubmitField('Edit')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')

class AddCommentForm(FlaskForm):
    body = StringField("Body", validators=[DataRequired()])
    submit = SubmitField("Post")