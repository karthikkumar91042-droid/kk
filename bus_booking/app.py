from flask import Flask
from config import Config
from extensions import db, login_manager
from routes.auth import auth
from routes.main import main
from routes.admin import admin


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(admin)

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        # Create default admin user if not exists
        from models import User
        admin_user = User.query.filter_by(email='admin@busbook.com').first()
        if not admin_user:
            admin_user = User(name='Admin', email='admin@busbook.com',
                              phone='9999999999', is_admin=True)
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print('✅ Default admin created: admin@busbook.com / admin123')
    app.run(debug=True)
