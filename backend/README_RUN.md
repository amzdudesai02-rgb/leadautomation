# How to Run Backend - Fixed Instructions

## ✅ Correct Way to Run Backend

### Option 1: Using run.py (Recommended)
```bash
cd backend
python run.py
```

### Option 2: Using Python Module
```bash
cd backend
python -m app.main
```

### Option 3: Using Flask CLI
```bash
cd backend
set FLASK_APP=app.main
flask run
```

---

## ❌ Wrong Way (Will Cause Error)

**Don't run:**
```bash
python app/main.py
```

This causes `ModuleNotFoundError: No module named 'app'`

---

## 🔧 Why This Happens

When you run `python app/main.py` from the `backend` directory, Python doesn't recognize `app` as a module because it's not in the Python path.

The `run.py` file fixes this by:
1. Adding the backend directory to Python path
2. Properly importing the app module
3. Starting the Flask server

---

## ✅ Quick Start

1. **Navigate to backend:**
   ```bash
   cd backend
   ```

2. **Install dependencies (first time only):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python run.py
   ```

4. **You should see:**
   ```
   ==================================================
   🚀 Starting Lead Generation Tool Backend
   ==================================================
   📍 Running on: http://localhost:5000
   🔧 Debug mode: True
   ==================================================
   
   * Running on http://0.0.0.0:5000
   ```

---

## 🎯 That's It!

Backend is now running correctly! ✅

