from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register routes only after the app is created
    with app.app_context():
        from . import routes  # Import routes here to avoid circular import
        app.register_blueprint(routes.bp)

    return app