from flask_wtf import FlaskForm
from wtforms import TextAreaField,StringField,DateField,DecimalField, EmailField,PasswordField,SubmitField,SelectField,RadioField,IntegerField
from wtforms.validators import InputRequired,Length,EqualTo,NumberRange

class RegistrationForm(FlaskForm): #To register an account
    username = StringField("Please enter a username:",validators=[InputRequired()])
    email=EmailField("Please enter email:",validators=[InputRequired()])
    password= PasswordField("Please enter password:",validators=[InputRequired(),Length(min=4)])
    password2= PasswordField("Please re-enter your password:", validators=[InputRequired(),EqualTo("password")])
    submit= SubmitField("Submit:")

class LoginForm(FlaskForm):
    username = StringField("Please enter a user name:",validators=[InputRequired()])
    password= PasswordField("Please enter password:",validators=[InputRequired()])
    submit= SubmitField("Submit:")


class Gig_regForm(FlaskForm): #To register a gig 
    artist_name=StringField("Enter artist name:",validators=[InputRequired()])
    gig_date= DateField("Please enter a date",validators=[InputRequired()])
    gig_venue=StringField("Please enter the venue:",validators=[InputRequired()])
    genre =SelectField("What genre of music is this event:", choices=["Rock","Pop","EDM","Rap"],validators=[InputRequired()])
    price = IntegerField("What is the price per ticket:",validators=[InputRequired(),NumberRange(min=1,max=200)])
    num_of_tickets=IntegerField("How many tickets are for sale?",validators=[InputRequired(),NumberRange(min=1,max=1000000)])
    submit= SubmitField("Submit:")

class GigForm(FlaskForm):#To search for a gig 
    artist_name=StringField("artist name:")
    #gig_date= DateField("Please enter a date")
    #gig_venue=StringField("Please enter the venue:")
    genre =SelectField("Genre:", choices=["None","Pop","EDM","Rap","Rock"],default=["None"])
    submit= SubmitField("Submit:")

class ReviewForm(FlaskForm):
    #artist_name= StringField("Enter artist name",validators=[InputRequired()])
    review =TextAreaField("Please leave a comment:",validators=[InputRequired()])
    score = RadioField("Please Rate your experience:",choices=[1,2,3,4,5],validators=[InputRequired()])
    submit=SubmitField("Submit")



class ForgotForm(FlaskForm):
    username=StringField("Please insert your username:",validators=[InputRequired()])
    email = EmailField("Please insert email:",validators=[InputRequired()])
    submit=SubmitField("Submit")

class ResetForm(FlaskForm):
    password= PasswordField("Please enter password:",validators=[InputRequired()])
    password2= PasswordField("Please re-enter your password:", validators=[InputRequired(),EqualTo("password")])
    submit=SubmitField("Submit")
    

class DeleteForm(FlaskForm):
    username=StringField("Insert username:",validators=[InputRequired()])
    password=PasswordField("Insert password:",validators=[InputRequired()])
    submit=SubmitField("Submit")
