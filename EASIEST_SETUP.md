# 🎯 Easiest Setup Guide - Step by Step

## ✅ PostgreSQL is Already Installed!

Your system has PostgreSQL running. Let's set it up:

---

## 📝 Step-by-Step Instructions

### Step 1: Open pgAdmin 4

1. Press **Windows Key**
2. Type: `pgAdmin`
3. Click **pgAdmin 4**

### Step 2: Connect to PostgreSQL

1. In pgAdmin, you'll see **"Servers"** in the left panel
2. Click on **"PostgreSQL 13"** (or 17/18 - whichever you have)
3. Enter password when prompted
   - This is the password you set during PostgreSQL installation
   - If you forgot it, see "Reset Password" section below

### Step 3: Create Database

1. Right-click on **"Databases"** (under your PostgreSQL server)
2. Click **"Create"** → **"Database"**
3. In the **"Database"** field, type: `lead_generation`
4. Click **"Save"**

✅ Database created!

### Step 4: Configure Backend

**Option A: Use the PowerShell script**
```powershell
.\setup_database.ps1
```

**Option B: Manual setup**

Create/edit `backend/.env`:
```env
# PostgreSQL Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lead_generation
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD_HERE

# JWT Secret
JWT_SECRET_KEY=change-this-to-random-string

# Flask
SECRET_KEY=change-this-to-random-string
FLASK_ENV=development
PORT=5000
```

### Step 5: Setup Database Tables

```powershell
cd backend
python database_setup.py
```

You should see:
```
✅ All tables created!
✅ Admin user created!
```

### Step 6: Start Application

**Terminal 1 - Backend:**
```powershell
cd backend
python run.py
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

### Step 7: Login

1. Open browser: `http://localhost:3000`
2. Login with:
   - **Username:** admin
   - **Password:** admin123

---

## 🔑 If You Forgot PostgreSQL Password

### Reset Password in pgAdmin:

1. Open pgAdmin
2. Right-click your PostgreSQL server
3. Click **"Properties"**
4. Go to **"Connection"** tab
5. Change password there

### Or Reset via Windows:

1. Open **Services** (services.msc)
2. Find **postgresql-x64-XX** service
3. Stop the service
4. Edit `pg_hba.conf` file (usually in `C:\Program Files\PostgreSQL\XX\data\`)
5. Change `md5` to `trust` temporarily
6. Start service
7. Connect without password
8. Reset password: `ALTER USER postgres WITH PASSWORD 'newpassword';`
9. Change `trust` back to `md5`
10. Restart service

---

## 🧪 Test Connection

After setting password in `.env`, test:

```powershell
cd backend
python -c "from app import create_app; app = create_app(); print('✅ Connected!')"
```

---

## ⚡ Quick Alternative: Use SQLite (No Password Needed)

If PostgreSQL setup is too complicated, use SQLite:

1. **Update `backend/app/config.py`:**
   Change line 11-12 to:
   ```python
   SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
       f"sqlite:///{os.path.join(os.path.dirname(__file__), '..', 'lead_generation.db')}"
   ```

2. **No `.env` database config needed!**

3. **Run setup:**
   ```powershell
   cd backend
   python database_setup.py
   ```

SQLite works the same way, just uses a file instead of a server!

---

## 🎯 Recommended Path

1. ✅ Open pgAdmin 4
2. ✅ Create `lead_generation` database
3. ✅ Run `setup_database.ps1` script
4. ✅ Enter your PostgreSQL password
5. ✅ Run `python database_setup.py`
6. ✅ Start application!

**You're ready to go!** 🚀

