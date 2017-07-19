from wtforms import StringField, PasswordField, Form, SelectField, BooleanField
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    '''Login Form'''
    username = StringField('username', validators=[InputRequired(), Length(min=1, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=15)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    '''Signup Form'''
    username = StringField('username', validators=[InputRequired(), Length(min=1, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=15)])
    confirmpassword = PasswordField('confirm password', validators=[InputRequired(), Length(min=1, max=15)])


class NewBucketList(FlaskForm):
    '''New Bucket List Form'''
    bucketname = StringField('bucketname', validators=[InputRequired(), Length(min=1, max=20)])

class EditBucket(FlaskForm):
    '''Edit Form'''
    newname = StringField('newname', validators=[InputRequired(), Length(min=1, max=20)])
    bucketname = StringField('bucketname', validators=[InputRequired(), Length(min=1, max=20)])

class DeleteBucket(FlaskForm):
    '''Delete Form'''
    bucketname = StringField('bucketname', validators=[InputRequired(), Length(min=1, max=20)])


class NewItem(FlaskForm):
    '''New Bucket List Form'''
    bucketname = StringField('bucketname', validators=[InputRequired(), Length(min=1, max=20)])
    itemname = StringField('itemname', validators=[InputRequired(), Length(min=1, max=20)])
    status = BooleanField('status')

class EditItem(FlaskForm):
    '''Edit Form'''
    bucketname = StringField('bucketname', validators=[InputRequired(), Length(min=1, max=20)])
    newname = StringField('newname', validators=[InputRequired(), Length(min=1, max=20)])
    status = SelectField('status')

class DeleteItem(Form):
    '''Delete Form'''
    itemname = StringField('itemname', validators=[InputRequired(), Length(min=1, max=20)])
