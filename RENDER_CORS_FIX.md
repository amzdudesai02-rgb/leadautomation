# 🔧 Render CORS Configuration Fix

## ❌ Current Error

```
Access to XMLHttpRequest at 'https://leadautomation-c73n.onrender.com/api/auth/login' 
from origin 'https://leadautomation.vercel.app' has been blocked by CORS policy: 
Response to preflight request doesn't pass access control check: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

**Problem:** Backend CORS not allowing requests from Vercel frontend.

---

## ✅ Solution: Add Vercel URL to Render Environment Variables

### Step 1: Add CORS_ORIGINS in Render

1. Go to **Render Dashboard** → Your backend service
2. Click **Environment** (left sidebar)
3. Click **"+ Add Environment Variable"**
4. Add:
   - **Key:** `CORS_ORIGINS`
   - **Value:** `https://leadautomation.vercel.app,http://localhost:3000,http://localhost:5173`
   - **Important:** Replace `leadautomation.vercel.app` with YOUR actual Vercel URL if different!
5. Click **Save Changes**

### Step 2: Redeploy Backend

1. Go to **Manual Deploy** section
2. Click **"Clear build cache & deploy"**
3. Wait for deployment to complete

---

## 📋 Alternative: Update Code (Already Done)

The code has been updated to include your Vercel URL (`https://leadautomation.vercel.app`), but you still need to:

1. **Add CORS_ORIGINS in Render** (see Step 1 above)
2. **Redeploy** (see Step 2 above)

---

## 🔍 Verify It's Working

After redeploying:

1. **Test Health Check:**
   ```
   https://leadautomation-c73n.onrender.com/api/health
   ```
   Should return: `{"status": "healthy", ...}`

2. **Test from Frontend:**
   - Open your Vercel site
   - Try logging in
   - Check browser console (should NOT see CORS error)

3. **Check Network Tab:**
   - Login request should return `200` or `401` (not CORS error)
   - Response headers should include: `Access-Control-Allow-Origin: https://leadautomation.vercel.app`

---

## 🐛 Still Not Working?

### Check 1: Vercel URL is Correct
- Verify your actual Vercel URL
- It should match exactly (including `https://`)

### Check 2: Environment Variable Format
- ✅ Correct: `https://leadautomation.vercel.app,http://localhost:3000`
- ❌ Wrong: `https://leadautomation.vercel.app/` (no trailing slash)
- ❌ Wrong: `leadautomation.vercel.app` (missing https://)

### Check 3: Redeployed?
- ⚠️ **MUST redeploy after adding environment variable!**
- Old deployments don't have the variable

### Check 4: Check Backend Logs
- In Render → Logs
- Look for CORS-related errors
- Check if the environment variable is being read

---

## 📝 Summary

**The Fix:**
1. Add `CORS_ORIGINS` environment variable in Render
2. Set value to: `https://leadautomation.vercel.app,http://localhost:3000`
3. Redeploy backend
4. Test login from Vercel frontend

**Why it happened:**
- CORS needs explicit origin allowlist
- Wildcard patterns don't work the same way
- Preflight (OPTIONS) requests need proper handling

---

## ✅ Expected Result

After completing all steps:

**Browser Console:**
- ✅ No CORS errors
- ✅ Login request succeeds (or returns 401 for wrong credentials)

**Network Tab:**
- ✅ Response includes: `Access-Control-Allow-Origin: https://leadautomation.vercel.app`
- ✅ Status: `200 OK` or `401 Unauthorized` (NOT CORS error)

