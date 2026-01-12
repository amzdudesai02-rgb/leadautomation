"""
Database setup script for Neon Database
Run this once to create all tables and initial admin user
"""
import sys
import os

# Add backend to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app import create_app
from app.models.database import db
from app.models.user import User

def setup_database():
    """Create all tables and initial admin user"""
    app = create_app()
    
    with app.app_context():
        try:
            # Test connection first
            print("Testing database connection...")
            db.session.execute(db.text("SELECT 1"))
            print("✅ Connected to database!")
            
            # Create all tables
            print("\nCreating database tables...")
            db.create_all()
            print("✅ All tables created!")
            
            # Create admin user if doesn't exist
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@leadgen.com',
                    full_name='Administrator',
                    role='admin',
                    is_active=True,
                    is_verified=True
                )
                admin.set_password('admin123')  # Change this password!
                
                db.session.add(admin)
                db.session.commit()
                print("✅ Admin user created!")
                print("\n" + "="*50)
                print("Default Admin Credentials:")
                print("="*50)
                print("   Username: admin")
                print("   Password: admin123")
                print("   ⚠️  Please change the password after first login!")
                print("="*50)
            else:
                print("ℹ️  Admin user already exists")
            
            print("\n🎉 Database setup complete!")
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("\nTroubleshooting:")
            print("1. Check DATABASE_URL in .env file")
            print("2. Verify Neon project is active")
            print("3. Check internet connection")
            print("4. Verify connection string format")
            return False
    
    return True

if __name__ == '__main__':
    success = setup_database()
    if not success:
        sys.exit(1)

