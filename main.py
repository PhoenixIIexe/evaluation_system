
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from models import Publication
from __init__ import db

import typing as t
import os


class Main(Blueprint):
    def __init__(self, name: str, import_name: str, static_folder: t.Optional[t.Union[str, os.PathLike]] = None, static_url_path: t.Optional[str] = None, template_folder: t.Optional[str] = None, url_prefix: t.Optional[str] = None, subdomain: t.Optional[str] = None, url_defaults: t.Optional[dict] = None, root_path: t.Optional[str] = None, cli_group: t.Optional[str] = ...):
        super().__init__(name, import_name, static_folder, static_url_path,
                         template_folder, url_prefix, subdomain, url_defaults, root_path, cli_group)

        self.add_url_rule('/', view_func=self.index)
        self.add_url_rule('/profile/', view_func=self.profile)
        self.add_url_rule('/add_publication/', view_func=self.add_publication)
        self.add_url_rule('/add_publication/',
                          view_func=self.add_publication_post, methods=['POST'])

    def index(self) -> str:
        if current_user.is_authenticated:
            publications = Publication.query.all()
            return render_template('content.html', publications=publications)

        return render_template('index.html')

    @login_required
    def profile(self) -> str:
        return render_template('profile.html')

    @login_required
    def add_publication(self) -> str:
        return render_template('add_publication.html')

    @login_required
    def add_publication_post(self) -> str:
        text = request.form.get('text_publication')
        new_publication = Publication(user_id=current_user.id, text=text)

        db.session.add(new_publication)
        db.session.commit()

        return redirect(url_for('main.index'))
