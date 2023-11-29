from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField, SubmitField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed

class SignUpForm(FlaskForm):
    id = StringField('Username', validators=[DataRequired()])
    email_address = StringField('Email')
    passwd = PasswordField('Password', validators=[DataRequired()])
    passwd_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')
    
class SignInForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')
    
class BeatForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    audio_file = FileField('Audio File', validators=[FileRequired(), FileAllowed(['mp3', 'wav'], 'Audio only!')])
    submit = SubmitField('Create Beat')
    
