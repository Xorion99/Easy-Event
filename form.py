from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField, DateField, TimeField, DateTimeField
from wtforms.validators import InputRequired, Length, ValidationError, Email, DataRequired, NumberRange


class RegisterForm(FlaskForm):
    Username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Username"})
    Name = StringField(validators=[InputRequired()],
                       render_kw={"placeholder": "Name"})
    Surname = StringField(validators=[InputRequired()], render_kw={"placeholder": "Surname"})
    Email = EmailField(validators=[DataRequired(), Email()],
                       render_kw={"placeholder": "Email"})
    Password = PasswordField(validators=[InputRequired(), Length(min=8, max=100)],
                             render_kw={"placeholder": "Password"})
    Confirm_password = PasswordField(validators=[InputRequired(), Length(min=8, max=40)],
                                     render_kw={"placeholder": "Confirm Password"})
    Age = IntegerField(validators=[InputRequired()],
                                  render_kw={"placeholder": "Age"})
    Language = StringField(validators=[InputRequired()],
                           render_kw={"placeholder": "Language"})

    Submit = SubmitField("SignUp")

    def validate_username(self, Username):
        from model import User
        existing_user_username = User.query.filter_by(username=Username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=40)],
                            render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


class EventForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                       render_kw={"placeholder": "Name Event"})
    organiser = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                       render_kw={"placeholder": "Organiser"})
    position = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                       render_kw={"placeholder": "Zone"})
    data = DateField(render_kw={"placeholder": "Data"})
    time = TimeField(validators=[InputRequired()], render_kw={"placeholder": "Time"})

    numberentrance = IntegerField(validators=[InputRequired()],
                       render_kw={"placeholder": "Number of Entrace"})

    price = IntegerField(validators=[InputRequired()],
                       render_kw={"placeholder": "Ticket price"})
    typology = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                       render_kw={"placeholder": "Typology"})
    submit = SubmitField("Create Event")



