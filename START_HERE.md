# 🚀 START HERE - Complete Setup Guide

## ✅ Current Status

- ✅ PostgreSQL is **installed and running** on your system
- ✅ Backend code is ready
- ✅ Frontend code is ready
- ⚠️ Need to: Create database and configure connection

---

## 📋 Quick Setup (5 Steps)

### Step 1: Create Database in pgAdmin

1. **Open pgAdmin 4** (search "pgAdmin" in Windows)
2. **Connect** to PostgreSQL server (enter your password)
3. **Right-click** "Databases" → **Create** → **Database**
4. **Name:** `lead_generation`
5. **Click Save**

✅ Database created!

---

### Step 2: Create .env File

**Option A: Copy template**
```powershell
cd backend
Copy-Item .env.template .env
```

**Option B: Use setup script**
```powershell
.\setup_database.ps1
```

**Option C: Manual creation**

Create `backend/.env` file with:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lead_generation
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD

JWT_SECRET_KEY=change-this-random-string
SECRET_KEY=change-this-random-string
FLASK_ENV=development
PORT=5000
```

**⚠️ Important:** Replace `YOUR_POSTGRES_PASSWORD` with your actual PostgreSQL password!

---

### Step 3: Install Backend Dependencies

```powershell
cd backend
pip install -r requirements.txt
```

---

### Step 4: Setup Database Tables

```powershell
python database_setup.py
```

**Expected output:**
```
Creating database tables...
✅ All tables created!
✅ Admin user created!
   Username: admin
   Password: admin123
```

---

### Step 5: Start Application

**Terminal 1 - Backend:**
```powershell
cd backend
python run.py
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm install
npm run dev
```

---

## 🔑 Login Credentials

**Application Login:**
- URL: http://localhost:3000
- Username: `admin`
- Password: `admin123`

**PostgreSQL:**
- User: `postgres`
- Password: (the one you set during installation)

---

## 🆘 Troubleshooting

### "Database connection failed"
- Check PostgreSQL password in `.env` is correct
- Verify database `lead_generation` exists
- Check PostgreSQL service is running

### "Module not found"
```powershell
pip install -r requirements.txt
```

### "Port already in use"
- Change `PORT=5001` in `.env`
- Or kill process using port 5000

---

## ✅ Success Checklist

- [ ] PostgreSQL database `lead_generation` created
- [ ] `backend/.env` file created with correct password
- [ ] Backend dependencies installed
- [ ] Database tables created (`python database_setup.py`)
- [ ] Backend running (`python run.py`)
- [ ] Frontend running (`npm run dev`)
- [ ] Can login at http://localhost:3000

---

## 🎯 You're Ready!

Once all steps are complete:
1. Open http://localhost:3000
2. Login with admin/admin123
3. Start using your professional Lead Generation Tool!

**Need help?** Check:
- `EASIEST_SETUP.md` - Detailed instructions
- `QUICK_DATABASE_SETUP.md` - Database setup
- `POSTGRESQL_WINDOWS_SETUP.md` - PostgreSQL installation

---

**Let's get started!** 🚀

