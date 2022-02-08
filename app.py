from flask import Flask, render_template, url_for, redirect, flash, request
from logging import FileHandler, WARNING
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from form import LoginForm, RegisterForm, EventForm, JoinForm, RateForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DATABASE.sqlite'
app.config['SECRET_KEY'] = 'jbhkkjbhdnslk98723bkj4o'

# aggiungo sqlalchemy all'app
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)




login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    from model import User
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'], defaults={"page": 1})
@app.route('/<int:page>', methods=['GET', 'POST'])
def index(page):
    from model import Event, join_Event
    form = JoinForm()
    page = page
    pages = 5
    event = Event.query.paginate(page, pages, error_out=False)
    joined_Event = join_Event.query.all()
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        event = Event.query.filter(Event.Position.like(search)).paginate(per_page=pages, error_out=False)
        empty = ""
        if not event.items:
            empty = "there are not event in this zone"
        return render_template('homepage/index.html', event=event, tag=tag, empty=empty)
    return render_template('homepage/index.html', event=event, joined_Event= joined_Event)


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
                return redirect(url_for('index'))

    return render_template('login/index.html', form=form)




@app.route('/newevent', methods=['GET', 'POST'])

def newevent():
    from model import Event

    form = EventForm()
    if form.validate_on_submit():
        d = form.data.data
        t = form.time.data
        x = datetime.combine(d, t)

        formt = x.strftime("%d/%m/%Y %H:%M")
        print(formt)

        event = Event(Name=form.name.data, Organiser=form.organiser.data, Date=x,
                      Position=form.position.data,
                      Number_of_entrance=form.numberentrance.data, Ticket_price=form.price.data,
                      Typology=form.typology.data
                      )

        flash('Event created!', 'success')
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_event/index.html', form=form)

@app.route('/loginfornewevent', methods=['GET', 'POST'])
def loginfornewevent():
    from model import User
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.Password, form.password.data):
                return redirect(url_for('newevent'))

    return render_template('login2/index.html', form=form)


@app.route('/signupfornewevent', methods=['GET', 'POST'])
def sign_up_fornewevent():
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
        return redirect(url_for('loginfornewevent'))
    return render_template('registration2/index.html', form=form)




@app.route('/join/<int:id>' , methods=["GET","POST"])
def join(id):
    from model import Event, join_Event
    join_form = JoinForm()
    if request.method == "POST":
        Email = join_form.email.data
        e_data = Event.query.get(id)
        event = join_Event(Email=Email, Name=e_data.Name, Organiser=e_data.Organiser, Date=e_data.Date,
                Position=e_data.Position,
                Number_of_entrance =int(e_data.Number_of_entrance), Ticket_price=int(e_data.Ticket_price),
                Typology =e_data.Typology)
        db.session.add(event)
        db.session.commit()

        return redirect("/")

    return render_template('join/index.html', form=join_form, id=id)


@app.route('/delete/<id>/', methods=['GET','POST'])
def delete(id):
    print(id)
    from model import join_Event
    delete_event = db.session.query(join_Event).filter(join_Event.id == id).first()
    flash("Evenet deleted")
    db.session.delete(delete_event)
    db.session.commit()
    return redirect("/")





@app.route('/rate')
def rating():
    form = RateForm()
    return render_template("rate/index.html", form =form)


@app.route('/rate/<int:id>', methods=["GET","POST"])
def rate(id):
    from model import Feedback
    data = Feedback(Rate=id)
    db.session.add(data)
    db.session.commit()

    return redirect("/")


@app.route('/aboutus')
def about_us():
    return render_template("about_us/index.html")

@app.route('/conditions')
def conditions():
    return render_template("conditions/index.html")

@app.route('/notfound')
def notfound():
    return render_template("notfound/index.html")


if __name__ == '__main__':
    app.run(debug=True)


@app.before_first_request
def setup_db():
    db.create_all()
