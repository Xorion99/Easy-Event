from flask import Flask, render_template, url_for, redirect, flash, request
from flask_bootstrap import Bootstrap
from logging import FileHandler, WARNING
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy import or_
import model
from form import LoginForm, RegisterForm, EventForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

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


@app.route('/', methods=['GET', 'POST'], defaults={"page": 1})
@app.route('/<int:page>', methods=['GET', 'POST'])
# @login_required
def index(page):
    from model import Event
    page = page
    pages = 5
    event = Event.query.paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        event = Event.query.filter(Event.Position.like(search)).paginate(per_page=pages, error_out=False)
        return render_template('homepage/index.html',event=event, tag=tag)


    return render_template('homepage/index.html', event=event)


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




@app.route('/newevent', methods=['GET', 'POST'])
# @login_required
def newevent():
    from model import Event

    form = EventForm()
    if form.validate_on_submit():
        d = form.data.data

        t = form.time.data
        # we combine both time and date object togather and make another datetime object with name x as mention below
        x = datetime.combine(d, t)

        # this is the way how to format data, once you use this method it will return string
        # string contains data and time with your provided format, but the problem is that
        # we can't save this directly to sqlite database, because sqlite only support python datetime object
        # if you want to display data from sqlite than you can use this way to format datetime and remove string from it.
        formt = x.strftime("%d/%m/%Y %H:%M")
        # please go to the console and see result how strftime works
        print(formt)

       # dt = x
        event = Event(Name=form.name.data, Organiser=form.organiser.data, Date=x,
                      Position=form.position.data,
                      Number_of_entrance=form.numberentrance.data, Ticket_price=form.price.data,
                      Typology=form.typology.data)

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
