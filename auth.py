from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User
from __init__ import db

import datetime

import typing as t
import os

from get_avatar import get_avatar


class Auth(Blueprint):
    def __init__(self, name: str, import_name: str, static_folder: t.Optional[t.Union[str, os.PathLike]] = None, static_url_path: t.Optional[str] = None, template_folder: t.Optional[str] = None, url_prefix: t.Optional[str] = None, subdomain: t.Optional[str] = None, url_defaults: t.Optional[dict] = None, root_path: t.Optional[str] = None, cli_group: t.Optional[str] = ...):
        super().__init__(name, import_name, static_folder, static_url_path,
                         template_folder, url_prefix, subdomain, url_defaults, root_path, cli_group)

        self.add_url_rule('/login/', view_func=self.login)
        self.add_url_rule(
            '/login/', view_func=self.login_post, methods=['POST'])

        self.add_url_rule('/signup/', view_func=self.signup)
        self.add_url_rule(
            '/signup/', view_func=self.signup_post, methods=['POST'])

        self.add_url_rule('/logout/', view_func=self.logout)

    def login(self) -> str:
        return render_template('login.html')

    def signup(self) -> str:
        return render_template('signup.html')

    def signup_post(self) -> str:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        date = request.form.get('date')
        gender = request.form.get('gender')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        avatar = get_avatar(date, gender)
        date = datetime.datetime.strptime(date, "%Y-%m-%d")

        new_user = User(email=email, name=name, password=generate_password_hash(
            password, method='sha256'), date=date, gender=gender, avatar=avatar)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    def login_post(self) -> str:
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

    @login_required
    def logout(self) -> str:
        logout_user()
        return redirect(url_for('main.index'))
