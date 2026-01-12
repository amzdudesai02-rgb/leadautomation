# How to Run Backend and Frontend

## Prerequisites

1. **Python 3.8+** installed
2. **Node.js 16+** and npm installed
3. **Google Sheets API** credentials (optional for testing)

---

## 🐍 Backend Setup & Run

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

**If you get errors, try:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Create Environment File
Create a file named `.env` in the `backend` folder:

```env
SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development
PORT=5000

# Google Sheets (Optional for testing)
GOOGLE_SHEETS_CREDENTIALS=
GOOGLE_SHEETS_SHEET_ID=

# Amazon API (Optional for testing)
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

### Step 4: Run Backend Server
```bash
python run.py
```

**Important:** Use `run.py` instead of `app/main.py` to avoid import errors!

**You should see:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

✅ **Backend is now running on `http://localhost:5000`**

---

## ⚛️ Frontend Setup & Run

### Step 1: Open New Terminal/Command Prompt
Keep the backend running, open a **new terminal window**.

### Step 2: Navigate to Frontend Directory
```bash
cd frontend
```

### Step 3: Install Node Dependencies
```bash
npm install
```

**This may take a few minutes the first time.**

### Step 4: Run Frontend Development Server
```bash
npm run dev
```

**You should see:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

✅ **Frontend is now running on `http://localhost:3000`**

---

## 🌐 Access the Application

1. **Open your browser**
2. **Go to:** `http://localhost:3000`
3. **You should see the Lead Generation Tool dashboard!**

---

## 📋 Quick Start Commands

### Option 1: Run Separately (Recommended)

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Option 2: Using Scripts (Windows)

Create `start-backend.bat`:
```batch
@echo off
cd backend
pip install -r requirements.txt
python app/main.py
pause
```

Create `start-frontend.bat`:
```batch
@echo off
cd frontend
npm install
npm run dev
pause
```

Then double-click both files!

---

## 🔍 Verify Everything is Working

### Test Backend API
Open browser or use curl:
```bash
curl http://localhost:5000/api/sellers
```

Should return:
```json
{
  "success": true,
  "data": [],
  "page": 1,
  "limit": 50
}
```

### Test Frontend
1. Open `http://localhost:3000`
2. You should see the dashboard
3. Try navigating to different pages

---

## ⚠️ Common Issues & Solutions

### Backend Issues

**Issue: Module not found**
```bash
pip install -r requirements.txt
```

**Issue: Port 5000 already in use**
- Change `PORT=5001` in `.env` file
- Or kill the process using port 5000

**Issue: Import errors**
```bash
# Make sure you're in backend directory
cd backend
python app/main.py
```

### Frontend Issues

**Issue: npm install fails**
```bash
# Clear cache and try again
npm cache clean --force
npm install
```

**Issue: Port 3000 already in use**
- Vite will automatically use next available port (3001, 3002, etc.)
- Or change port in `vite.config.js`

**Issue: Cannot connect to backend**
- Make sure backend is running on port 5000
- Check `CORS_ORIGINS` in backend `.env` includes `http://localhost:3000`

**Issue: API calls failing**
- Check backend is running: `http://localhost:5000`
- Check browser console for errors
- Verify CORS settings

---

## 🛑 Stopping the Servers

### Stop Backend
- Press `Ctrl + C` in the backend terminal

### Stop Frontend
- Press `Ctrl + C` in the frontend terminal

---

## 📊 Development Workflow

1. **Start Backend** (Terminal 1)
   ```bash
   cd backend
   python app/main.py
   ```

2. **Start Frontend** (Terminal 2)
   ```bash
   cd frontend
   npm run dev
   ```

3. **Make Changes**
   - Backend: Changes auto-reload (Flask debug mode)
   - Frontend: Changes auto-reload (Vite HMR)

4. **Test in Browser**
   - Open `http://localhost:3000`
   - Test all features

---

## 🚀 Production Build

### Build Frontend for Production
```bash
cd frontend
npm run build
```

This creates optimized files in `frontend/dist/`

### Run Production Backend
```bash
cd backend
# Set FLASK_ENV=production in .env
python app/main.py
```

---

## 📝 Summary

**Backend:**
1. `cd backend`
2. `pip install -r requirements.txt`
3. Create `.env` file
4. `python app/main.py`
5. ✅ Running on `http://localhost:5000`

**Frontend:**
1. `cd frontend` (new terminal)
2. `npm install`
3. `npm run dev`
4. ✅ Running on `http://localhost:3000`

**Access:** Open `http://localhost:3000` in your browser!

---

## 🎯 Next Steps After Running

1. ✅ Test Seller Sniping
2. ✅ Test Brand Research
3. ✅ Test QA Analysis
4. ✅ Check Dashboard Metrics
5. ✅ Test Automation Endpoints

Happy coding! 🚀

