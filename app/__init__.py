from flask import Flask, render_template
from flask_login import login_required, current_user

from .config import Config
from .extensions import db, login_manager
from .model import init_enum_tables
from .model.Tasks import Task

from .routes.auth.auth import auth_bp
from .routes.tasks.tasks import task_bp


def create_app():
    static_dir = 'static'
    template_dir = 'templates'

    app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Log in required.'

    with app.app_context():
        db.create_all()
        init_enum_tables(db)
        
    app.register_blueprint(auth_bp, url_prefix='')
    app.register_blueprint(task_bp, url_prefix='/tasks')
    

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html')

    
    @app.route('/projects')
    def projects():
        return 'this will be the projects page'
    
    return app