
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from __init__ import db

import typing as t
import os


class Main(Blueprint):
    def __init__(self, name: str, import_name: str, static_folder: t.Optional[t.Union[str, os.PathLike]] = None, static_url_path: t.Optional[str] = None, template_folder: t.Optional[str] = None, url_prefix: t.Optional[str] = None, subdomain: t.Optional[str] = None, url_defaults: t.Optional[dict] = None, root_path: t.Optional[str] = None, cli_group: t.Optional[str] = ...):
        super().__init__(name, import_name, static_folder, static_url_path,
                         template_folder, url_prefix, subdomain, url_defaults, root_path, cli_group)

        self.add_url_rule('/', view_func=self.index)
        self.add_url_rule('/profile/', view_func=self.profile)

    def index(self) -> str:
        context = {}

        if current_user.is_authenticated:
            context['avatar'] = current_user.avatar
        return render_template('index.html', **context)

    @login_required
    def profile(self) -> str:
        return render_template('profile.html', name=current_user.name, avatar=current_user.avatar)
