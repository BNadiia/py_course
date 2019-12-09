from flask import render_template, url_for, flash, redirect, request, abort
from flasknews import app, db, bcrypt
from flasknews.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flasknews.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import os
import errno
import secrets
from PIL import Image


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    path = os.path.join(app.root_path, 'static/images/profile_pics/' + current_user.username)
    make_sure_path_exists(path)
    picture_path = os.path.join(app.root_path, path, picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last__seen = datetime.utcnow()
        db.session.commit()


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))


@app.route("/account", methods=['GET'])
def account():
    form = UpdateAccountForm()
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.about_me.data = current_user.about_me
    image_file = url_for('static', filename='images/profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/accountupdate", methods=['GET', 'POST'])
@login_required
def accountupdate():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        if form.old_pass.data:
            if bcrypt.check_password_hash(current_user.password, form.old_pass.data):
                hashed_password = bcrypt.generate_password_hash(form.new_pass.data).decode('utf-8')
                current_user.password = hashed_password
            elif bcrypt.check_password_hash(current_user.password, form.old_pass.data) == False:
                flash('Old password is wrong!', 'danger')
                return redirect('account')
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    image_file = url_for('static', filename='images/profile_pics/' + current_user.image_file)
    return render_template('_account-update.html', title='Account', image_file=image_file, form=form)




@app.route("/newspost")
def newspost():
    return render_template('news-post.html')





