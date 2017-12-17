# -*- coding: utf-8 -*-
from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, g, session
from flask.ext.login import logout_user, login_user, login_required, current_user
from app import app
from app import models, db, L_m
from models import User, Post


@app.before_request
def before_request():
    g.user = current_user
    

@app.route('/', methods=['GET', 'POST'])
def startPage():
    items = Post.query.all()
    return render_template('first_page.html',
                          items=items)
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index():
    if 'email' not in session:
        return render_template('first_page.html')
    else:
        user = g.user
        user_id = user.id
        posts = Post.query.filter_by(user_id=user_id).all()
        if request.method == "POST":
            title = request.form['inputTitle']
            text = request.form['inputText']
            user_id = user.id
            new_entry = Post(title=title,
                             text=text,
                             user_id=user_id,
                             timestamp=datetime.utcnow())
            db.session.add(new_entry)
            db.session.commit()
            flash('New entry was successfully posted.')
        return render_template("index.html",
                               user=user,
                               posts=posts)


@app.route('/posts')
def posts():
    if 'email' not in session:
        return render_template('first_page.html')
    else:
        user = g.user
        user_id = user.id
        posts = Post.query.filter_by(user_id=user_id).all()
    return render_template("post.html",
                           user=user,
                           posts=posts)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get(id)
    if post is None:
        flash('Post not found.')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.')
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if 'email' not in session:
        return render_template('first_page.html')
    else:
        user = g.user
        post1 = Post.query.get(id)
        if request.method == "POST":
            post = Post.query.filter_by(id=id).update(dict(title=request.form['inputTitle'],text=request.form['inputText'],timestamp = datetime.utcnow()))
            db.session.commit()
            flash('Entry was successfully edited.')
            return redirect(url_for('posts'))
        return render_template('edit.html',
                               id=id,
                               user=user,
                               post1=post1)


@app.route('/user/<login>')
@login_required
def user(login, page=1):
    user = User.query.filter_by(login=login).first()
    if user is None:
        flash('User ' + login + ' not found.')
        return redirect(url_for('index'))
    if user.login == g.user.login:
        return redirect(url_for('index'))

@L_m.user_loader
def load_user(userid):
    return models.User.query.filter_by(id=userid).first()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form["inputEmail"]
        login = request.form["inputLogin"]
        name = request.form["inputName"]
        surname = request.form["inputSurname"]
        password = request.form["inputPassword"]
        password2 = request.form["inputPassword2"]
        for user in db.session.query(User.login):
            if user.login == login:
                return render_template("register.html", reg_error='A person with this login is already registered')
        for user in db.session.query(User.email):
            if user.email == email:
                return render_template("register.html", reg_error='A person with this email is already registered')

        if password == password2:
            new_user = models.User(login=login, name=name, surname=surname,
                                   email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=False)
            session['email'] = email
            return redirect(url_for('index'))
        else:
            return render_template('register.html', reg_error='The passwords do not match')
    return render_template('register.html',
                           title='registration page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["inputEmail"]
        password = request.form["inputPassword"]

        if 'remember-me' in request.form.values():
            remember_me = True
        else:
            remember_me = False
        user = User.query.filter_by(email=email).first()
        if user is not None and user.verify_password(password):
            login_user(user, remember=remember_me)
            session['email'] = email
            return redirect(url_for('index'))
        else:

            return render_template('login.html', reg_error='Email or password are incorrect', title='Log in')
    return render_template('login.html',
                           title='Log in')


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('login'))
