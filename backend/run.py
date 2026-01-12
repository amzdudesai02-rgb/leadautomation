"""
Entry point for running the Flask application
Run this file from the backend directory: python run.py
"""
import sys
import os

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app import create_app
from app.tasks.scheduler import init_scheduler

app = create_app()

# Initialize scheduler for automated tasks
if os.environ.get('ENABLE_SCHEDULER', 'true').lower() == 'true':
    try:
        init_scheduler()
    except Exception as e:
        print(f"Warning: Could not initialize scheduler: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    print(f"\n{'='*50}")
    print(f"🚀 Starting Lead Generation Tool Backend")
    print(f"{'='*50}")
    print(f"📍 Running on: http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"{'='*50}\n")
    app.run(host='0.0.0.0', port=port, debug=debug)

