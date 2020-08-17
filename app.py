from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    json,
    session
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "thisissecretkey"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120))

    def __repr__(self):
        return "<User %r>" % self.username


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/users")
def get_users():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            return {"message": "There is no user with that email."}

        if user.password != password:
            return {"message": "Password is incorrect!"}

        session["username"] = user.username

        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        new_user = User(
            username=username,
            email=email,
            password=password
        )

        # add the new_user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run()
