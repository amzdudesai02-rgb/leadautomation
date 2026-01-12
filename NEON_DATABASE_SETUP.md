# 🚀 Neon Database Setup Guide

## What is Neon?

Neon is a **serverless PostgreSQL** database in the cloud. No local installation needed!

**Benefits:**
- ✅ No local PostgreSQL installation
- ✅ Free tier available
- ✅ Automatic backups
- ✅ Easy to use
- ✅ Production-ready

---

## 📋 Setup Steps

### Step 1: Create Neon Account

1. Go to: https://neon.tech/
2. Sign up for free account
3. Create a new project

### Step 2: Get Database Connection String

1. In Neon dashboard, go to your project
2. Click **"Connection Details"** or **"Connection String"**
3. Copy the connection string

It looks like:
```
postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### Step 3: Configure Backend

**Create `backend/.env` file:**

```env
# Neon Database (Use this instead of local PostgreSQL)
DATABASE_URL=postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require

# Or use individual components:
# DB_HOST=ep-xxx-xxx.us-east-2.aws.neon.tech
# DB_PORT=5432
# DB_NAME=neondb
# DB_USER=your_username
# DB_PASSWORD=your_password

# Flask Configuration
SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development
PORT=5000

# JWT Configuration
JWT_SECRET_KEY=dev-jwt-secret-key-change-this
JWT_ACCESS_TOKEN_EXPIRES=86400

# Amazon API (Optional)
AMAZON_API_KEY=
AMAZON_SECRET_KEY=
AMAZON_ASSOCIATE_TAG=

# Email Finder (Optional)
HUNTER_API_KEY=

# Gmail (Optional)
GMAIL_USER=
GMAIL_PASSWORD=

# Scheduler
ENABLE_SCHEDULER=true

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Logging
LOG_LEVEL=INFO
```

### Step 4: Update Config for Neon

The config already supports `DATABASE_URL`, so it will work automatically!

### Step 5: Setup Database Tables

```powershell
cd backend
pip install -r requirements.txt
python database_setup.py
```

This will:
- ✅ Connect to Neon database
- ✅ Create all tables
- ✅ Create admin user

### Step 6: Start Application

```powershell
# Terminal 1 - Backend
cd backend
python run.py

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

---

## 🔍 Verify Connection

Test Neon connection:

```powershell
cd backend
python -c "from app import create_app; app = create_app(); print('✅ Connected to Neon!')"
```

---

## 📝 Neon Dashboard Features

After setup, you can:
- ✅ View tables in Neon dashboard
- ✅ Run SQL queries
- ✅ See database metrics
- ✅ Manage connections
- ✅ View logs

---

## 🎯 Advantages of Neon

1. **No Local Setup** - No PostgreSQL installation needed
2. **Free Tier** - Generous free tier for development
3. **Automatic Backups** - Your data is safe
4. **Scalable** - Grows with your needs
5. **Easy Management** - Web dashboard for everything

---

## ⚠️ Important Notes

1. **SSL Required** - Neon requires SSL connection (already handled)
2. **Connection String** - Use the full `DATABASE_URL` from Neon
3. **Password** - Keep your Neon password secure
4. **Free Tier Limits** - Check Neon's free tier limits

---

## 🔧 Troubleshooting

### Connection Error
- Check connection string is correct
- Verify SSL mode is set (`sslmode=require`)
- Check Neon project is active

### SSL Error
- Ensure `?sslmode=require` is in connection string
- Or add to config: `SSL_MODE=require`

### Timeout Error
- Check internet connection
- Verify Neon project is not paused
- Check firewall settings

---

## ✅ Quick Start

1. **Sign up at neon.tech**
2. **Create project**
3. **Copy connection string**
4. **Add to `backend/.env` as `DATABASE_URL`**
5. **Run `python database_setup.py`**
6. **Start application!**

**That's it!** Much easier than local PostgreSQL! 🚀

