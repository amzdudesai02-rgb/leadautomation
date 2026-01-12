# 🚀 Quick Database Setup - PostgreSQL Already Installed!

## ✅ Good News!

PostgreSQL is **already installed and running** on your system!

I can see these services running:
- postgresql-x64-13
- postgresql-x64-17  
- postgresql-x64-18

---

## 📋 Quick Setup Steps

### Step 1: Find Your PostgreSQL Password

**Option A: Check if you remember it**
- It's the password you set during PostgreSQL installation

**Option B: Reset it (if forgotten)**
1. Open **pgAdmin 4** (installed with PostgreSQL)
2. Or use Windows Services to reset

**Option C: Try common defaults**
- `postgres` (common default)
- `admin`
- Or check your installation notes

### Step 2: Create Database

**Using pgAdmin (Easiest):**
1. Open **pgAdmin 4** from Start Menu
2. Connect to PostgreSQL server (enter password)
3. Right-click **"Databases"** → **"Create"** → **"Database"**
4. Name: `lead_generation`
5. Click **"Save"**

**Or Using Command Line:**
```powershell
# Connect to PostgreSQL (replace 'postgres' with your password)
psql -U postgres

# Enter password when prompted, then:
CREATE DATABASE lead_generation;

# Exit
\q
```

### Step 3: Configure Backend

Edit `backend/.env` file:

```env
# PostgreSQL Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lead_generation
DB_USER=postgres
DB_PASSWORD=your_postgres_password_here

# JWT Secret
JWT_SECRET_KEY=your-secret-jwt-key-change-this

# Other settings...
SECRET_KEY=your-secret-key
FLASK_ENV=development
PORT=5000
```

### Step 4: Test Connection

```powershell
cd backend
python -c "from app import create_app; app = create_app(); print('✅ Database connected!')"
```

### Step 5: Setup Database Tables

```powershell
python database_setup.py
```

This will:
- ✅ Create all tables
- ✅ Create admin user (admin/admin123)

### Step 6: Start Application

```powershell
# Terminal 1 - Backend
python run.py

# Terminal 2 - Frontend  
cd ..\frontend
npm run dev
```

---

## 🔍 Find PostgreSQL Port

If port 5432 doesn't work, check which port PostgreSQL is using:

```powershell
# Check PostgreSQL configuration
Get-Content "C:\Program Files\PostgreSQL\*\data\postgresql.conf" | Select-String "port"
```

Or check in pgAdmin:
- Right-click server → Properties → Connection tab

---

## 🎯 Default Credentials

**PostgreSQL:**
- User: `postgres`
- Password: (the one you set during installation)
- Port: `5432` (usually)

**Application Admin:**
- Username: `admin`
- Password: `admin123` (created by database_setup.py)

---

## ⚡ Quick Test

Try this to test PostgreSQL connection:

```powershell
# Test connection (replace password)
$env:PGPASSWORD='your_password'; psql -U postgres -h localhost -c "SELECT version();"
```

If this works, PostgreSQL is ready! ✅

---

## 🆘 Still Having Issues?

1. **Check PostgreSQL is running:**
   ```powershell
   Get-Service postgresql*
   ```

2. **Check port:**
   ```powershell
   netstat -an | findstr 5432
   ```

3. **Try connecting with pgAdmin:**
   - Open pgAdmin 4
   - See if you can connect

4. **Use SQLite instead (temporary):**
   - See `POSTGRESQL_WINDOWS_SETUP.md` for SQLite option

---

## ✅ Next Steps

1. Create `lead_generation` database
2. Update `backend/.env` with your PostgreSQL password
3. Run `python database_setup.py`
4. Start the application!

You're almost there! 🚀

