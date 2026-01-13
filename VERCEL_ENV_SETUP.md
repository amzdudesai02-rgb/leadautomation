# 🔧 Vercel Environment Variable Setup

## ❌ Current Error

```
ERR_CONNECTION_REFUSED
localhost:5000/api/auth/login:1 Failed to load resource
```

**Problem:** Frontend is trying to connect to `localhost:5000` instead of your Render backend.

---

## ✅ Solution: Set VITE_API_URL in Vercel

### Step 1: Get Your Render Backend URL

1. Go to your Render Dashboard
2. Click on your backend service
3. Copy the URL (e.g., `https://lead-generation-backend-abc123.onrender.com`)

### Step 2: Add Environment Variable in Vercel

1. **Go to Vercel Dashboard**
   - Navigate to your project
   - Click **Settings** (top menu)
   - Click **Environment Variables** (left sidebar)

2. **Add New Variable**
   - Click **"+ Add New"** button
   - **Key:** `VITE_API_URL`
   - **Value:** `https://your-render-backend-url.onrender.com`
     - Replace with your actual Render URL!
   - **Environment:** Select all (Production, Preview, Development)
   - Click **Save**

3. **Redeploy**
   - Go to **Deployments** tab
   - Click **"..."** (three dots) on latest deployment
   - Click **"Redeploy"**
   - Or push a new commit to trigger auto-deploy

---

## 📋 Example

**In Vercel Environment Variables:**

```
Key: VITE_API_URL
Value: https://lead-generation-backend-abc123.onrender.com
```

**Important:** 
- ✅ Include `https://`
- ✅ No trailing slash `/`
- ✅ Use your actual Render URL

---

## 🔍 Verify It's Working

After redeploying, check:

1. **Browser Console** (F12)
   - Should see: `🔗 API Base URL: https://your-backend.onrender.com`
   - Should NOT see: `localhost:5000`

2. **Network Tab**
   - Login request should go to: `https://your-backend.onrender.com/api/auth/login`
   - NOT: `localhost:5000/api/auth/login`

---

## 🐛 Troubleshooting

### Still seeing `localhost:5000`?

1. **Check Environment Variable**
   - Go to Vercel → Settings → Environment Variables
   - Verify `VITE_API_URL` is set correctly
   - Make sure it's enabled for **Production**

2. **Redeploy**
   - Environment variables only apply to NEW deployments
   - You MUST redeploy after adding variables

3. **Check Build Logs**
   - In Vercel deployment logs
   - Look for environment variable warnings

### Still getting connection errors?

1. **Verify Backend is Running**
   - Visit: `https://your-backend.onrender.com/api/health`
   - Should return: `{"status": "healthy", ...}`

2. **Check CORS**
   - Make sure your Vercel URL is in backend `CORS_ORIGINS`
   - Format: `https://your-project.vercel.app`

---

## ✅ Quick Checklist

- [ ] Got Render backend URL
- [ ] Added `VITE_API_URL` in Vercel
- [ ] Set value to `https://your-backend.onrender.com`
- [ ] Enabled for Production environment
- [ ] Redeployed Vercel project
- [ ] Verified in browser console (no localhost)
- [ ] Tested login functionality

---

## 📝 Summary

**The Fix:**
1. Add `VITE_API_URL` = `https://your-render-backend.onrender.com` in Vercel
2. Redeploy
3. Test!

**Why it happened:**
- Vite environment variables must start with `VITE_`
- If not set, defaults to `localhost:5000`
- Production builds need the variable set in Vercel

