
from flask import Flask, render_template, request, url_for, redirect, flash, \
session, abort

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
db_name = "auth.db"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{db}'.format(db=db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'configure strong secret key here'

db = SQLAlchemy(app)


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    pass_hash = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '' % self.username


@app.route('/')
def index():
    return render_template('index.html')


# https://myaccount.google.com/u/3/lesssecureapps?pli=1&rapt=AEjHL4MpjjYh8Z-01vJ5GRsQXICYQsXHG0PweSjWenlbAJfes6qNKbHKs_CfCVh0d5qUO58qFeeB0sYCbA3GANLf-965469dVA

@app.errorhandler(404)
def page_not_found(e):
    e = 'Page not Found'
    return ( render_template('404.html', e=e), 404 )


def create_db():
    """ # Execute this first time to create new db in current directory. """
    db.create_all()


# @app.route("/signup/", methods=["GET", "POST"])    # ( No signup allowed )
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
            
        if not (username and password):
            flash("Username or Password cannot be empty")
            return redirect(url_for('signup'))
        else:
            username = username.strip()
            password = password.strip()

        hashed_pwd = generate_password_hash(password, 'sha256')
        new_user = User(username=username, pass_hash=hashed_pwd,)
        db.session.add(new_user)

        try:
            db.session.commit()
        except:
            flash("Username {u} is not available.".format(u=username))
            return redirect(url_for('signup'))

        flash("User account has been created.")
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty.")
            return redirect(url_for('login'))
        else:
            username = username.strip()
            password = password.strip()

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.pass_hash, password):
            session[username] = True
            return redirect(url_for("user_home", username=username))
        else:
            flash("Invalid username or password.")
    return render_template("login_form.html")


@app.route("/user/<username>")
def user_home(username):
    if not session.get(username):
        return redirect(url_for("login"))
    return render_template("user_home.html",
                            username=username,
                            m_get=True,
                            cid=None,
                          )


@app.route("/fetch_history/<username>")
def fetch_history(username):
    if not session.get(username):
        abort(401)

    from account_tests import KhataBook_by_ID as kid
    obj = kid.flask_sheet()
    return render_template("fetch_history.html",
                            username=username,
                            fetch=obj.fetch(0),
                          )


@app.route("/update/<username>", methods=["GET", "POST"])
def update(username):
    if request.method == "POST":
        if not session.get(username):
            abort(401)

        cust = request.form['cust']
        from account_tests import KhataBook_by_ID as kid

        obj = kid.flask_sheet()
        obj.add_cust(cust)
        return render_template("fetch_history.html", 
                                username=username,
                                fetch=obj.fetch(0),
                                )
    else:
        return render_template('404.html')


@app.route("/account/<username>", methods=["GET", "POST"])
def user_account(username):
    try:
        if request.method == "POST":
            if not session.get(username):
                abort(401)

            product = request.form['product']
            cost = float(request.form['cost'])
            cid = int(request.form['cid'])

            from account_tests import KhataBook_by_ID as kid
            obj = kid.flask_sheet()
            attend = [product, cost] 
            obj.mark(attend, cid)

            flash(product)
            flash(cost)
            flash(cid)
            return render_template("user_home.html", 
                                    username=username,
                                    fetch=obj.fetch(cid),
                                    cid=cid,
                                    m_get=False,
                                    )
    except Exception as e:
        return render_template('404.html', e=e)


@app.route("/logout/<username>")
def logout(username):
    session.pop(username, None)
    # print(session)

    flash("successfully logged out.")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True,
            port=5000, 
            host='0.0.0.0',
            )
