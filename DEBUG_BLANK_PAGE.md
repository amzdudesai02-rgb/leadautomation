# 🐛 Debug Blank Page Issue

## Current Status
- ✅ Frontend files exist
- ✅ Dependencies installed
- ✅ React and Material-UI installed
- ⚠️ Page still showing blank

---

## 🔍 Step-by-Step Debugging

### Step 1: Check Browser Console

1. **Open Developer Tools:**
   - Press **F12** or **Right-click → Inspect**
   - Click **Console** tab

2. **Look for errors:**
   - Red error messages
   - Failed imports
   - Network errors

3. **Common errors to check:**
   - `Cannot find module`
   - `Failed to fetch`
   - `CORS error`
   - `404 Not Found`

---

### Step 2: Check Network Tab

1. **Open Developer Tools (F12)**
2. **Click Network tab**
3. **Refresh page (F5)**
4. **Look for:**
   - Failed requests (red)
   - 404 errors
   - CORS errors

---

### Step 3: Verify Backend is Running

```powershell
# Terminal 1 - Backend
cd backend
python run.py
```

**Should see:**
```
🚀 Starting Lead Generation Tool Backend
📍 Running on: http://localhost:5000
```

---

### Step 4: Verify Frontend is Running

```powershell
# Terminal 2 - Frontend
cd frontend
npm run dev
```

**Should see:**
```
➜  Local:   http://localhost:3000/
```

---

### Step 5: Test Backend Connection

Open browser and go to:
```
http://localhost:5000/api/auth/login
```

**Should see:** JSON response (even if error)

---

### Step 6: Check for JavaScript Errors

**In browser console, look for:**

1. **Import errors:**
   ```
   Failed to resolve import "..." from "..."
   ```

2. **Module errors:**
   ```
   Cannot find module "..."
   ```

3. **Runtime errors:**
   ```
   Uncaught TypeError: ...
   ```

---

## 🔧 Quick Fixes

### Fix 1: Clear Browser Cache

1. Press **Ctrl+Shift+Delete**
2. Select **Cached images and files**
3. Click **Clear data**
4. Refresh page (**Ctrl+Shift+R**)

### Fix 2: Reinstall Dependencies

```powershell
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### Fix 3: Check Vite Config

Verify `frontend/vite.config.js` exists and has correct port.

### Fix 4: Check index.html

Verify `frontend/index.html` has:
```html
<div id="root"></div>
<script type="module" src="/src/main.jsx"></script>
```

---

## 🎯 Expected Console Output

**If working correctly, console should show:**
- No red errors
- Vite dev server messages
- React app loaded

**If broken, console might show:**
- Red error messages
- Failed network requests
- Module not found errors

---

## 📝 What to Report

If still blank, please share:

1. **Browser console errors** (F12 → Console)
2. **Network tab errors** (F12 → Network)
3. **Backend terminal output**
4. **Frontend terminal output**

---

## ✅ Quick Test

Try this in browser console (F12):

```javascript
// Check if React is loaded
console.log('React:', typeof React)

// Check if root element exists
console.log('Root:', document.getElementById('root'))

// Check localStorage
console.log('Token:', localStorage.getItem('token'))
```

---

## 🚀 Next Steps

1. **Check browser console** (F12)
2. **Share any errors** you see
3. **Verify backend is running**
4. **Try hard refresh** (Ctrl+Shift+R)

**The console errors will tell us exactly what's wrong!**

