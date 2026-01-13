# 🚨 URGENT: Fix Vercel Environment Variable

## ❌ Current Error

```
⚠️ WARNING: Using localhost API URL in production!
📍 Base URL: http://localhost:5000
```

**This means `VITE_API_URL` is NOT set in Vercel!**

---

## ✅ Step-by-Step Fix (5 Minutes)

### Step 1: Get Your Render Backend URL

1. Go to **https://dashboard.render.com**
2. Click on your **backend service** (e.g., "lead-generation-backend")
3. Copy the **URL** shown at the top
   - Example: `https://lead-generation-backend-abc123.onrender.com`
   - **IMPORTANT:** Copy the FULL URL including `https://`

### Step 2: Add Environment Variable in Vercel

1. Go to **https://vercel.com/dashboard**
2. Click on your **project** (leadautomation)
3. Click **Settings** (top menu bar)
4. Click **Environment Variables** (left sidebar)
5. Click **"+ Add New"** button
6. Fill in:
   - **Key:** `VITE_API_URL`
   - **Value:** `https://your-render-backend-url.onrender.com`
     - ⚠️ Replace with YOUR actual Render URL from Step 1!
   - **Environment:** Check **Production** (or select all)
7. Click **Save**

### Step 3: Redeploy (CRITICAL!)

**Environment variables only work on NEW deployments!**

**Option A: Manual Redeploy**
1. Go to **Deployments** tab
2. Find the latest deployment
3. Click **"..."** (three dots menu)
4. Click **"Redeploy"**
5. Wait for deployment to complete

**Option B: Trigger New Deploy**
- Push any commit to GitHub (or just make a small change)
- Vercel will auto-deploy with the new environment variable

---

## 🔍 Verify It's Set Correctly

### Check in Vercel:
1. Go to **Settings** → **Environment Variables**
2. You should see:
   ```
   VITE_API_URL = https://your-backend.onrender.com
   ```

### Check After Redeploy:
1. Open your Vercel site
2. Open Browser Console (F12)
3. You should see:
   ```
   🔗 API Base URL: https://your-backend.onrender.com
   ```
4. You should **NOT** see:
   ```
   ⚠️ WARNING: Using localhost API URL in production!
   ```

---

## 🐛 Still Not Working?

### Check 1: Variable Name
- ✅ Must be exactly: `VITE_API_URL`
- ❌ NOT: `API_URL` or `REACT_APP_API_URL`
- ❌ NOT: `VITE_API_BASE_URL`

### Check 2: Variable Value
- ✅ Must start with: `https://`
- ✅ Must be your Render backend URL
- ❌ NOT: `http://localhost:5000`
- ❌ NOT: Missing `https://`

### Check 3: Environment Scope
- ✅ Must be enabled for **Production**
- ✅ Or enable for all environments

### Check 4: Redeployed?
- ⚠️ **MUST redeploy after adding variable!**
- Old deployments don't have the variable
- Check deployment logs to see if variable is loaded

---

## 📋 Quick Checklist

- [ ] Got Render backend URL
- [ ] Added `VITE_API_URL` in Vercel Settings
- [ ] Set value to `https://your-backend.onrender.com`
- [ ] Enabled for Production
- [ ] Clicked Save
- [ ] Redeployed the project
- [ ] Checked browser console (no localhost warning)
- [ ] Tested login (should work now)

---

## 💡 Pro Tip

After setting the variable, you can verify it's being used:

1. Open your Vercel site
2. Press F12 (Developer Tools)
3. Go to **Console** tab
4. Look for: `🔗 API Base URL: https://...`
5. If you see `localhost:5000`, the variable isn't set or you need to redeploy

---

## ✅ Expected Result

After completing all steps:

**Browser Console:**
```
🔗 API Base URL: https://your-backend.onrender.com
```

**Network Tab (when logging in):**
- Request URL: `https://your-backend.onrender.com/api/auth/login`
- Status: `200 OK` (or `401` if wrong credentials, but NOT connection error)

---

## 🆘 Still Need Help?

If still not working after following all steps:

1. **Check Render Backend:**
   - Visit: `https://your-backend.onrender.com/api/health`
   - Should return: `{"status": "healthy", ...}`

2. **Check Vercel Build Logs:**
   - Go to Deployments → Latest → Build Logs
   - Look for environment variable warnings

3. **Verify CORS:**
   - Make sure your Vercel URL is in backend CORS_ORIGINS
   - Format: `https://your-project.vercel.app`

