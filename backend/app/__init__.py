from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.models.database import db, init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    init_db(app)
    
    # Enable CORS for React frontend and Render deployment
    cors_origins = Config.CORS_ORIGINS.copy() if isinstance(Config.CORS_ORIGINS, list) else Config.CORS_ORIGINS.split(',')
    cors_origins.extend([
        "https://*.onrender.com",
        "https://*.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173"
    ])
    CORS(app, resources={
        r"/api/*": {
            "origins": cors_origins,
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        },
        r"/health": {
            "origins": "*",
            "methods": ["GET"]
        },
        r"/": {
            "origins": "*",
            "methods": ["GET"]
        }
    })
    
    # Register blueprints
    from app.routes import health_routes, auth_routes, seller_routes, brand_routes, qa_routes, automation_routes
    
    # Health check (no prefix, accessible at / and /api/health)
    app.register_blueprint(health_routes.bp)
    
    # API routes
    app.register_blueprint(auth_routes.bp, url_prefix='/api/auth')
    app.register_blueprint(seller_routes.bp, url_prefix='/api/sellers')
    app.register_blueprint(brand_routes.bp, url_prefix='/api/brands')
    app.register_blueprint(qa_routes.bp, url_prefix='/api/qa')
    app.register_blueprint(automation_routes.bp, url_prefix='/api/automation')
    
    return app

