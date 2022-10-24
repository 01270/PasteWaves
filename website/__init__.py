from flask import Flask, Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def run_website():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Q3JFU4KC@!djg84jvd&##XxX:5633;FXXX'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    def page_not_found(e): return render_template('404.html'), 404

    from .routes import routes
    app.register_blueprint(routes, url_prefix='/')

    from .models import User, Paste
    run_database(app)

    app.register_error_handler(404, page_not_found)
    return app

def run_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')
