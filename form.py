from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField
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
    Age = IntegerField(validators=[DataRequired(), NumberRange(min=0, max=100)],
                       render_kw={"placeholder": "Age"})
    Language = StringField(validators=[InputRequired()],
                           render_kw={"placeholder": "Language"})

    Submit = SubmitField("SignUp")

    def validate_username(self, Username):
        existing_user_username = User.query.filter_by(username=Username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=40)],
                            render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


from model import User