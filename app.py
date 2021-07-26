from flask import Flask,render_template, request, flash,redirect, url_for
from flask_login import  LoginManager,logout_user,login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import jwt


app = Flask(__name__)
app.secret_key="1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = app.secret_key
db=SQLAlchemy(app)


class Users(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password=db.Column(db.String(120), nullable=False,unique=True)
    admin = db.Column(db.Boolean(), default=False)
    email = db.Column(db.String(100), nullable=False)
    date_registration = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_token(self):
        token=jwt.encode({"user":self.username,"password":self.password},key=app.secret_key)
        return token

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)


@app.route('/')
@app.route('/home')
def home():
    users = Users.query.all()
    return render_template("home.html", users=users)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)

@app.route("/login",  methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user=Users.query.filter_by(username=username).first()
            if user.get_token()==jwt.encode({"user":username,"password":password},key=app.secret_key):
                login_user(user)
                return redirect('/home')
            else:
                flash("Неверный логин  или пароль")
        else:
            flash("Ошибка")
    return render_template('login.html')

@app.route('/users')
def users():
    articles = Users.query.order_by(Users.date_registration.desc()).all()
    return render_template("users.html",articles=articles)

@app.route('/users/create',methods=['post','get'])
@login_required
def users_create():
    if request.method == "POST":
        username=request.form.get('username'),
        email=request.form.get('email'),
        password=request.form.get('password')
        admin=request.form.get('admin')
        user=Users(username=username,email=email,password=password,admin=bool(admin))
        db.session.add(user)
        try:
            db.session.commit()
            return redirect("/users")
        except Exception:
            db.session.rollback()
            flash('Ошибка')
            return render_template('users-create.html')
        users = Users.query.all()
        return render_template('users.html', users=users)
    else:
        return render_template("users-create.html")


@app.route('/users/<int:id>/update',methods=["POST","GET"])
@login_required
def users_update(id):
    field = Users.query.get(id)
    if request.method=="POST":
        field.username = request.form.get('username'),
        field.email = request.form.get('email'),
        field.password = request.form.get('password')
        field.admin = bool(request.form.get('admin'))
        field.updated_on=datetime.now()
        try:
            db.session.commit()
            return redirect('/users')
        except Exception:
            return "При обновлении пользователя произошла ошибка"
    else:
        return render_template("users_update.html",field=field)

@app.route('/users/<int:id>/delete')
def users_delete(id):
    user = Users.query.get_or_404(id)

    try:
        db.session.delete(user)
        db.session.commit()
        return redirect('/users')
    except Exception:
        return "При удалении пользователя произошла ошибка"

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/home')

@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)