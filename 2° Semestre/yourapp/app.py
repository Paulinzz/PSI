from flask import Flask, render_template
from config import Config
from extensions import db, login_manager
from models.user import User  # Import necessário para o user_loader
from auth import auth_bp
from controllers.user_controllers import users_bp
from controllers.product_controllers import product_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializa extensões
    db.init_app(app)
    login_manager.init_app(app)
    
    # Registra blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(product_bp, url_prefix='')
    
    # Rota principal
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Cria tabelas
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)