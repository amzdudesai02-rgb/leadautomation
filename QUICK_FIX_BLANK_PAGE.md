# 🔧 Quick Fix for Blank Page

## ✅ Fixes Applied

I've fixed several issues that could cause a blank page:

1. **AuthContext** - Better error handling, won't crash if backend is down
2. **Login API** - Correct response handling for token and user data
3. **ProtectedRoute** - Better loading state display

---

## 🚀 Quick Steps to Fix

### Step 1: Make Sure Backend is Running

```powershell
cd backend
python run.py
```

**Should see:**
```
🚀 Starting Lead Generation Tool Backend
📍 Running on: http://localhost:5000
```

### Step 2: Refresh Browser

1. Open: http://localhost:3000
2. Press **Ctrl+Shift+R** (hard refresh)
3. Or press **F5** to refresh

### Step 3: Check Browser Console

1. Press **F12** to open Developer Tools
2. Click **Console** tab
3. Look for any red errors

---

## 🎯 What Should Happen

1. **First Visit:** Should show login page with gradient background
2. **Login Form:** Username and Password fields visible
3. **After Login:** Redirects to dashboard

---

## 🐛 If Still Blank

### Check 1: Backend Running?
```powershell
# Test backend
curl http://localhost:5000/api/auth/login
# Should get response (even if error)
```

### Check 2: Frontend Running?
```powershell
cd frontend
npm run dev
# Should show: Local: http://localhost:3000/
```

### Check 3: Browser Console Errors?
- Press F12
- Check Console tab
- Look for:
  - Network errors
  - JavaScript errors
  - CORS errors

---

## 📝 Common Issues

### Issue: "Cannot connect to backend"
**Fix:** Start backend: `python run.py`

### Issue: CORS error
**Fix:** Backend CORS is configured, verify backend is running

### Issue: 404 on /api/auth/login
**Fix:** Check backend routes are registered

---

## ✅ Expected Result

You should see a **beautiful login page** with:
- Purple gradient background
- White login card
- Username field
- Password field
- Sign In button
- "Default credentials: admin / admin123" text

---

## 🎉 Try Now!

1. Make sure backend is running
2. Refresh browser (Ctrl+Shift+R)
3. You should see the login page!

**If still blank, check browser console (F12) for errors!**

