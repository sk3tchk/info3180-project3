import random
from random import randint
from flask.ext.wtf import Form
from wtforms.fields import TextField, FileField, IntegerField, SelectField, SubmitField, PasswordField, StringField
from wtforms.validators import Required,ValidationError,DataRequired,Email,Length
from flask_wtf.file import FileField,FileAllowed,FileRequired

class myform(Form):
    image = FileField('Image File', validators=[FileRequired(),FileAllowed(['jpg','jpeg' 'png'], 'Images only!')])
    firstname = TextField('First Name',validators=[Required()])
    lastname = TextField('Last Name',validators=[Required()])
    age = TextField('Age',validators=[Required()])
    sex = SelectField('Sex', validators=[Required()], choices=[('male','Male'),('female','Female'),('other','Other')])
    email = TextField('Email Address', validators=[Length(min=6, max=100), Required("Required"), Email()])
    password = PasswordField('Password', validators=[Required("Required"), Length(min=4, max=100)])

class LoginForm(Form):
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class WishForm(Form):
    title = TextField('Title')
    description = TextField('Description')
    description_url = TextField('Reference')
    