from app import create_app
from app.tasks.scheduler import init_scheduler
import os

app = create_app()

# Initialize scheduler for automated tasks
if os.environ.get('ENABLE_SCHEDULER', 'true').lower() == 'true':
    init_scheduler()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)

