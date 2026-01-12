# ✅ Setup with Your Neon Database

## 🎯 Your Neon Connection String

```
postgresql://neondb_owner:npg_e1GpPDlqicI7@ep-cool-poetry-ah4s3njj-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

---

## 📝 Step 1: Create `.env` File

**Create `backend/.env` file** with this exact content:

```env
DATABASE_URL=postgresql://neondb_owner:npg_e1GpPDlqicI7@ep-cool-poetry-ah4s3njj-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development
PORT=5000

JWT_SECRET_KEY=dev-jwt-secret-key-change-this
JWT_ACCESS_TOKEN_EXPIRES=86400

CORS_ORIGINS=http://localhost:3000,http://localhost:5173
LOG_LEVEL=INFO
ENABLE_SCHEDULER=true
```

**Save this file as:** `backend/.env`

---

## 🚀 Step 2: Setup Database

```powershell
cd backend
pip install -r requirements.txt
python database_setup.py
```

**You should see:**
```
Testing database connection...
✅ Connected to database!

Creating database tables...
✅ All tables created!
✅ Admin user created!
```

---

## 🎯 Step 3: Start Application

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

## 🔐 Step 4: Login

1. Open: **http://localhost:3000**
2. Login:
   - Username: `admin`
   - Password: `admin123`

---

## ✅ Verify in Neon Dashboard

1. Go to: https://console.neon.tech/
2. Open your project
3. Click **"Tables"** tab
4. You should see all 5 tables created!

---

## 🎉 Done!

Your application is now connected to Neon database!

**Everything is ready to use!** 🚀

