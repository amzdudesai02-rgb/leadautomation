# ✅ Neon Database Setup - Complete Guide

## 🎯 What You Need to Do

### Option 1: Use Neon (Recommended - Easiest!)

**No local PostgreSQL needed!**

1. **Sign up at Neon:** https://neon.tech/
2. **Create project**
3. **Copy connection string**
4. **Add to `backend/.env`**
5. **Run setup**

**That's it!** ✅

---

### Option 2: Use Local PostgreSQL

If you prefer local database:
1. Create database in pgAdmin
2. Configure `.env` with local credentials
3. Run setup

---

## 🚀 Neon Setup (5 Steps)

### Step 1: Create Neon Account

1. Visit: **https://neon.tech/**
2. Click **"Sign Up"** (free)
3. Sign up with GitHub, Google, or email

### Step 2: Create Project

1. Click **"Create Project"**
2. Choose:
   - **Name:** Lead Generation Tool
   - **Region:** Choose closest to you
   - **PostgreSQL Version:** 16 (latest)
3. Click **"Create Project"**

### Step 3: Get Connection String

1. In your project dashboard
2. Click **"Connection Details"** or find **"Connection String"**
3. Copy the **full connection string**

**Example:**
```
postgresql://username:password@ep-cool-darkness-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### Step 4: Configure Application

**Create `backend/.env` file:**

```env
# Neon Database Connection String
DATABASE_URL=postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require

# Flask
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
PORT=5000

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=86400

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Logging
LOG_LEVEL=INFO

# Scheduler
ENABLE_SCHEDULER=true
```

**⚠️ Replace the DATABASE_URL with your actual Neon connection string!**

### Step 5: Setup Database

```powershell
cd backend
pip install -r requirements.txt
python database_setup.py
```

**Expected output:**
```
Testing database connection...
✅ Connected to database!

Creating database tables...
✅ All tables created!
✅ Admin user created!

Default Admin Credentials:
   Username: admin
   Password: admin123
```

---

## ✅ Verify Setup

### Check in Neon Dashboard:

1. Go to Neon dashboard
2. Click your project
3. Go to **"SQL Editor"** or **"Tables"**
4. Run: `SELECT * FROM users;`
5. Should see admin user

### Check in Application:

1. Start backend: `python run.py`
2. Start frontend: `npm run dev`
3. Login at http://localhost:3000
4. Username: `admin`, Password: `admin123`

---

## 🎨 Neon Dashboard Features

- ✅ **SQL Editor** - Run queries directly
- ✅ **Tables View** - See all your tables
- ✅ **Connection Info** - Manage connections
- ✅ **Metrics** - Database performance
- ✅ **Backups** - Automatic backups

---

## 🔧 Troubleshooting

### "Connection failed"
- Check connection string is correct
- Verify `?sslmode=require` is included
- Check Neon project is active (not paused)

### "SSL error"
- Ensure `sslmode=require` in connection string
- Neon requires SSL connection

### "Authentication failed"
- Verify username/password in connection string
- Check credentials in Neon dashboard

---

## 📊 Database Tables Created

After running `database_setup.py`, you'll have:

1. **users** - User accounts
2. **sellers** - Seller data
3. **brands** - Brand data
4. **qa_analyses** - QA analysis results
5. **audit_logs** - Activity logs

All visible in Neon dashboard! ✅

---

## 🎯 Advantages of Neon

| Feature | Neon | Local PostgreSQL |
|---------|------|------------------|
| Setup Time | 2 minutes | 30+ minutes |
| Installation | None needed | Required |
| Backups | Automatic | Manual |
| Access | Anywhere | Local only |
| Cost | Free tier | Free |
| Management | Web dashboard | Command line |

---

## ✅ Quick Checklist

- [ ] Neon account created
- [ ] Project created
- [ ] Connection string copied
- [ ] `.env` file created with DATABASE_URL
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database setup run (`python database_setup.py`)
- [ ] Tables visible in Neon dashboard
- [ ] Application running

---

## 🚀 You're Ready!

Once setup is complete:
1. Your database is in the cloud
2. Accessible from anywhere
3. Automatic backups enabled
4. Professional setup complete!

**Start using your Lead Generation Tool!** 🎉

