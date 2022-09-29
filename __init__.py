from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import typing as t
import os

db = SQLAlchemy()


class App(Flask):
    def __init__(self, import_name: str, static_url_path: t.Optional[str] = None, static_folder: t.Optional[t.Union[str, os.PathLike]] = "static", static_host: t.Optional[str] = None, host_matching: bool = False, subdomain_matching: bool = False, template_folder: t.Optional[str] = "templates", instance_path: t.Optional[str] = None, instance_relative_config: bool = False, root_path: t.Optional[str] = None):
        super().__init__(import_name, static_url_path, static_folder, static_host, host_matching,
                         subdomain_matching, template_folder, instance_path, instance_relative_config, root_path)

        self.config['SECRET_KEY'] = 'admin'
        self.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(self)
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(self)

        from models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        from main import Main
        main_blueprint = Main('main', __name__)
        self.register_blueprint(main_blueprint)

        from auth import Auth
        auth_blueprint = Auth('auth', __name__)
        self.register_blueprint(auth_blueprint)


if __name__ == '__main__':
    app = App(import_name=__name__)
    app.run(debug=True)
