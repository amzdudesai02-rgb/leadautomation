# PostgreSQL Setup for Windows (Without Docker)

## Option 1: Install PostgreSQL Directly (Recommended)

### Step 1: Download PostgreSQL
1. Go to: https://www.postgresql.org/download/windows/
2. Download the **Windows x86-64** installer
3. Run the installer

### Step 2: Installation Steps
1. **Welcome Screen** → Click "Next"
2. **Installation Directory** → Keep default (or choose custom)
3. **Select Components** → Keep all checked:
   - PostgreSQL Server
   - pgAdmin 4
   - Stack Builder
   - Command Line Tools
4. **Data Directory** → Keep default
5. **Password** → Set a password (remember this!)
   - Example: `postgres123` or your own password
6. **Port** → Keep default `5432`
7. **Locale** → Keep default
8. **Ready to Install** → Click "Next"
9. **Installation Complete** → Click "Finish"

### Step 3: Verify Installation
Open **Command Prompt** or **PowerShell**:
```powershell
psql --version
```

Should show: `psql (PostgreSQL) 16.x`

### Step 4: Create Database
Open **pgAdmin 4** (installed with PostgreSQL) or use command line:

**Using pgAdmin:**
1. Open pgAdmin 4
2. Connect to server (password you set during installation)
3. Right-click "Databases" → "Create" → "Database"
4. Name: `lead_generation`
5. Click "Save"

**Or using Command Line:**
```powershell
# Connect to PostgreSQL
psql -U postgres

# Enter your password when prompted
# Then run:
CREATE DATABASE lead_generation;

# Exit
\q
```

---

## Option 2: Use Docker (If You Want)

### Start Docker Desktop First
1. Open **Docker Desktop** application
2. Wait for it to start (whale icon in system tray)
3. Then run:
```powershell
docker run -d -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=postgres postgres
```

---

## Option 3: Use SQLite (Simplest - No Installation Needed)

If you want to skip PostgreSQL for now, we can use SQLite (file-based database).

**Update `backend/.env`:**
```env
# Use SQLite instead
DATABASE_URL=sqlite:///lead_generation.db
```

**Update `backend/app/config.py`** - Change:
```python
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    f"sqlite:///{os.path.join(os.path.dirname(__file__), '..', 'lead_generation.db')}"
```

---

## Quick Setup After PostgreSQL Installation

### 1. Update `.env` File
```env
# PostgreSQL Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lead_generation
DB_USER=postgres
DB_PASSWORD=your_postgres_password_here
```

### 2. Test Connection
```powershell
cd backend
python -c "from app.models.database import db; from app import create_app; app = create_app(); print('Database connected!')"
```

### 3. Setup Database
```powershell
python database_setup.py
```

---

## Troubleshooting

### "psql: command not found"
- Add PostgreSQL to PATH:
  - Default location: `C:\Program Files\PostgreSQL\16\bin`
  - Add to System PATH environment variable

### "Connection refused"
- Check PostgreSQL service is running:
  ```powershell
  # Check service status
  Get-Service -Name postgresql*
  
  # Start service if stopped
  Start-Service postgresql-x64-16
  ```

### "Authentication failed"
- Check password in `.env` matches PostgreSQL password
- Try resetting password in pgAdmin

---

## Recommended: Use PostgreSQL Direct Installation

**Easiest path:**
1. Download PostgreSQL installer
2. Install with default settings
3. Remember your password
4. Create database using pgAdmin
5. Update `.env` file
6. Run `database_setup.py`

This is the most reliable method for Windows! 🚀

