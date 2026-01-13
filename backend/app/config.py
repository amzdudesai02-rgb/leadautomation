import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # PostgreSQL Database Configuration
    # Supports both Neon (cloud) and local PostgreSQL
    # Priority: DATABASE_URL (for Neon) > Individual components (for local)
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'lead_generation')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
    
    # Use DATABASE_URL if provided (Neon), otherwise build from components
    if os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 86400))  # 24 hours
    
    # Google Sheets Configuration (Optional - for backup/export)
    GOOGLE_SHEETS_CREDENTIALS = os.environ.get('GOOGLE_SHEETS_CREDENTIALS')
    GOOGLE_SHEETS_SHEET_ID = os.environ.get('GOOGLE_SHEETS_SHEET_ID')
    
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
    
    # SmartScout Configuration (Optional - for morning automation)
    SMARTSCOUT_USERNAME = os.environ.get('SMARTSCOUT_USERNAME')
    SMARTSCOUT_PASSWORD = os.environ.get('SMARTSCOUT_PASSWORD')
    SMARTSCOUT_URL = os.environ.get('SMARTSCOUT_URL', 'https://app.smartscout.com')
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

