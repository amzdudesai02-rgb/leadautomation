# ⚡ Neon Database - Quick Start

## 🎯 Why Neon?

- ✅ **No local PostgreSQL needed**
- ✅ **Free tier available**
- ✅ **Cloud-based** - Access from anywhere
- ✅ **Easy setup** - Just copy connection string

---

## 🚀 5-Minute Setup

### Step 1: Get Neon Connection String

1. Go to: **https://neon.tech/**
2. Sign up (free)
3. Create new project
4. Copy **Connection String**

**It looks like:**
```
postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
```

### Step 2: Create `.env` File

Create `backend/.env`:

```env
# Neon Database Connection (Paste your connection string here)
DATABASE_URL=postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require

# Flask
SECRET_KEY=change-this-random-string
FLASK_ENV=development
PORT=5000

# JWT
JWT_SECRET_KEY=change-this-random-string
JWT_ACCESS_TOKEN_EXPIRES=86400

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

**That's it!** Just paste your Neon connection string.

### Step 3: Setup Database

```powershell
cd backend
pip install -r requirements.txt
python database_setup.py
```

### Step 4: Start Application

```powershell
# Terminal 1
cd backend
python run.py

# Terminal 2
cd frontend
npm install
npm run dev
```

### Step 5: Login

- Open: http://localhost:3000
- Username: `admin`
- Password: `admin123`

---

## ✅ Done!

Your app is now using Neon cloud database!

**Benefits:**
- No local PostgreSQL needed
- Access from anywhere
- Automatic backups
- Free tier for development

---

## 🔍 Verify in Neon Dashboard

1. Go to Neon dashboard
2. Click on your project
3. Go to **"Tables"** tab
4. You should see:
   - users
   - sellers
   - brands
   - qa_analyses
   - audit_logs

**All tables created!** ✅

---

## 🎯 That's It!

Much simpler than local PostgreSQL setup! 🚀

