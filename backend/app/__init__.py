from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.models.database import db, init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    init_db(app)
    
    # Enable CORS for React frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://localhost:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints
    from app.routes import auth_routes, seller_routes, brand_routes, qa_routes, automation_routes
    app.register_blueprint(auth_routes.bp, url_prefix='/api/auth')
    app.register_blueprint(seller_routes.bp, url_prefix='/api/sellers')
    app.register_blueprint(brand_routes.bp, url_prefix='/api/brands')
    app.register_blueprint(qa_routes.bp, url_prefix='/api/qa')
    app.register_blueprint(automation_routes.bp, url_prefix='/api/automation')
    
    return app

