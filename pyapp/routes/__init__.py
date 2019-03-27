from flask import flash, redirect, render_template, request, send_from_directory, url_for
from flask_cors import CORS
from flask_login import current_user, login_required, login_user, logout_user
from pyapp import login_manager, pyapp, db
from pyapp.forms.LoginForm import LoginForm
from pyapp.models.Account import Account as Account_Model
from pyapp.routes import Account, Entry, Tag
from pyapp.utils.auth import role_required
from werkzeug.urls import url_parse

# Allow CORS so client can make requests to DB
CORS(pyapp)

pyapp.register_blueprint(Account.blueprint)
pyapp.register_blueprint(Entry.blueprint)
pyapp.register_blueprint(Tag.blueprint)

pyapp.config.update(
    PERMANENT_SESSION_LIFETIME=600
)

@login_manager.user_loader
def load_user(id):
    return Account_Model.query.get(int(id))


@pyapp.route('/')
@pyapp.route('/index')
def index():
    return send_from_directory(pyapp.static_folder, 'index.html')


@pyapp.route('/<path:path>')
def forward(path):
    return send_from_directory(pyapp.static_folder, path)


@pyapp.route('/api/v1/')
@login_required
@role_required('admin')
def apiRoute():
    return render_template('api.html', title='API Home')


@pyapp.route('/auth/')
@login_required
def auth():
    return render_template('auth.html', title='Not Authorized!')


@pyapp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = Account_Model.query.filter_by(
            email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')

            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@pyapp.route('/logout', methods=['GET'])
@login_required
def logout():
    user = current_user

    user.authenticated = False

    db.session.add(user)
    db.session.commit()

    logout_user()

    return redirect(url_for('login'))
