# 🔧 Troubleshoot Blank Page - Step by Step

## ⚠️ Still Seeing Blank Page?

Follow these steps to find the issue:

---

## Step 1: Check Browser Console (CRITICAL!)

1. **Open Developer Tools:**
   - Press **F12**
   - Or **Right-click → Inspect**

2. **Click Console Tab**

3. **Look for RED errors**

4. **Copy any errors you see** and share them

**Common errors:**
- `Failed to fetch`
- `Cannot find module`
- `CORS policy`
- `Uncaught TypeError`

---

## Step 2: Verify Backend is Running

**Open Terminal 1:**
```powershell
cd backend
python run.py
```

**Should see:**
```
🚀 Starting Lead Generation Tool Backend
📍 Running on: http://localhost:5000
```

**If not running, start it!**

---

## Step 3: Verify Frontend is Running

**Open Terminal 2:**
```powershell
cd frontend
npm run dev
```

**Should see:**
```
➜  Local:   http://localhost:3000/
```

**If not running, start it!**

---

## Step 4: Test Simple Version

**Temporarily test if React works:**

1. **Edit `frontend/src/main.jsx`:**
   ```jsx
   import React from 'react'
   import ReactDOM from 'react-dom/client'

   ReactDOM.createRoot(document.getElementById('root')).render(
     <div style={{padding: '50px', background: '#667eea', color: 'white'}}>
       <h1>React Works!</h1>
     </div>
   )
   ```

2. **Save and refresh browser**

3. **If you see "React Works!"** → React is fine, issue is in App component
4. **If still blank** → React/Vite issue

---

## Step 5: Check Network Tab

1. **Open Developer Tools (F12)**
2. **Click Network tab**
3. **Refresh page (F5)**
4. **Look for:**
   - Failed requests (red)
   - 404 errors
   - CORS errors

---

## Step 6: Clear Everything

```powershell
# Clear browser cache
# Press Ctrl+Shift+Delete → Clear cache

# Reinstall frontend dependencies
cd frontend
rm -rf node_modules
npm install
npm run dev
```

---

## 🎯 Quick Diagnostic

**Run this in browser console (F12):**

```javascript
// Check if React loaded
console.log('React:', typeof React)

// Check root element
console.log('Root:', document.getElementById('root'))

// Check for errors
console.log('Errors:', window.errors)
```

---

## 📝 What to Share

If still blank, please share:

1. **Browser console errors** (F12 → Console)
2. **Network tab errors** (F12 → Network)
3. **Backend terminal output**
4. **Frontend terminal output**

---

## ✅ Expected Behavior

**If working:**
- Login page with purple gradient
- Username and password fields
- Sign In button

**If broken:**
- Blank white page
- Console errors
- Network errors

---

## 🚀 Most Likely Fixes

1. **Backend not running** → Start it!
2. **JavaScript error** → Check console (F12)
3. **CORS error** → Backend CORS configured, verify backend running
4. **Import error** → Run `npm install` in frontend folder

**Check the browser console (F12) - that will tell us exactly what's wrong!**

