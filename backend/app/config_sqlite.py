"""
Alternative SQLite configuration (no PostgreSQL installation needed)
Use this if you want to skip PostgreSQL setup for now
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration with SQLite"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # SQLite Database (No installation needed!)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{os.path.join(BASE_DIR, '..', 'lead_generation.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 86400))
    
    # Amazon API Configuration
    AMAZON_API_KEY = os.environ.get('AMAZON_API_KEY')
    AMAZON_SECRET_KEY = os.environ.get('AMAZON_SECRET_KEY')
    AMAZON_ASSOCIATE_TAG = os.environ.get('AMAZON_ASSOCIATE_TAG')
    AMAZON_ENDPOINT = os.environ.get('AMAZON_ENDPOINT', 'webservices.amazon.com')
    AMAZON_REGION = os.environ.get('AMAZON_REGION', 'us-east-1')
    AMAZON_MARKETPLACE = os.environ.get('AMAZON_MARKETPLACE', 'www.amazon.com')
    
    # Email Finder API (Hunter.io)
    HUNTER_API_KEY = os.environ.get('HUNTER_API_KEY')
    
    # Gmail Configuration
    GMAIL_USER = os.environ.get('GMAIL_USER')
    GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

