from flask import Flask, render_template, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from logging import FileHandler, WARNING
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from form import LoginForm, RegisterForm, EventForm
from flask_login import UserMixin, login_user,LoginManager,login_required,logout_user, current_user



app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DATABASE'
app.config['SECRET_KEY'] = 'jbhkkjbhdnslk98723bkj4o'

# aggiungo sqlalchemy all'app
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
Bootstrap(app)

app.config['SECRET_KEY'] = '234JI432OHJ4OI3HOH4322H43H'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    from model import User
    return User.query.get(int(user_id))

@app.route('/')
def index():
    form = RegisterForm()# put application's code here
    return render_template('homepage/index.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    from model import User
    form = RegisterForm()
    if form.validate_on_submit():
        ashed_password = bcrypt.generate_password_hash(form.Password.data)
        new_user = User(Username=form.Username.data, Name=form.Name.data,
                        Surname=form.Surname.data, Email=form.Email.data,
                        Age=form.Age.data, Password=ashed_password, Language=form.Language.data)
        flash('Account created!', 'success')
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration/index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    from model import User
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.Password, form.password.data):
                return redirect(url_for('home'))
    return render_template('login/index.html', form=form)



@app.route('/home')
#@login_required
def home():
    return render_template('homepage/index.html')

@app.route('/newevent',methods=['GET', 'POST'])
#@login_required
def newevent():
    from model import Event
    form = EventForm()
    if form.validate_on_submit:
        event = Event(Name=form.name.data, Organiser=form.organiser.data,
                      Position=form.position.data, Date=form.data.data,
                      Number_of_entrance= form.numberentrance.data, Ticket_price=form.price.data,Typology=form.typology.data)


        flash('Event created!', 'success')
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_event/index.html', form=form)




if __name__ == '__main__':
    app.run(debug=True)


@app.before_first_request
def setup_db():
    db.create_all()


