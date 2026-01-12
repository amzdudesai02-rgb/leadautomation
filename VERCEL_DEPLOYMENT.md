# 🚀 Vercel Frontend Deployment Guide

## ✅ Current Vercel Settings (From Image)

Your configuration looks correct:
- **Framework Preset:** Vite ✅
- **Root Directory:** frontend ✅
- **Build Command:** `npm run build` ✅ (default)
- **Output Directory:** `dist` ✅ (default)
- **Install Command:** `npm install` ✅ (default)

---

## 🔧 Required Environment Variables

**IMPORTANT:** You need to add the backend API URL!

### In Vercel Dashboard:

1. Go to **Environment Variables** section
2. Click **"+ Add More"**
3. Add this variable:

```
Key: VITE_API_URL
Value: https://your-render-backend-url.onrender.com
```

**Replace `your-render-backend-url` with your actual Render backend URL!**

Example:
```
VITE_API_URL=https://lead-generation-backend-abc123.onrender.com
```

---

## 📋 Step-by-Step Deployment

### 1. **Add Environment Variable**
- In the Environment Variables section
- Add: `VITE_API_URL` = `https://your-render-backend-url.onrender.com`

### 2. **Remove Example Variable** (if present)
- Remove `EXAMPLE_NAME` if it's just an example

### 3. **Click "Deploy"**
- Vercel will build and deploy your frontend
- First deployment may take 2-3 minutes

---

## 🔗 After Deployment

1. **Get Your Frontend URL**
   - Vercel will provide: `https://your-project.vercel.app`

2. **Update Backend CORS**
   - In Render backend, add your Vercel URL to CORS origins
   - Environment variable: `CORS_ORIGINS`
   - Value: `https://your-project.vercel.app`

3. **Test the Connection**
   - Visit your Vercel URL
   - Try logging in
   - Check browser console for API errors

---

## 🐛 Troubleshooting

### **CORS Errors**
- Make sure your Render backend has the Vercel URL in `CORS_ORIGINS`
- Format: `https://your-project.vercel.app`

### **API Connection Failed**
- Verify `VITE_API_URL` is set correctly in Vercel
- Check that your Render backend is running
- Test backend URL directly: `https://your-backend.onrender.com/api/health`

### **Build Fails**
- Check Vercel build logs
- Ensure all dependencies are in `package.json`
- Verify Node.js version (Vercel auto-detects)

---

## ✅ Summary

**Before Deploying:**
1. ✅ Set `VITE_API_URL` environment variable
2. ✅ Remove example variables
3. ✅ Verify Root Directory is `frontend`

**After Deploying:**
1. ✅ Get your Vercel URL
2. ✅ Add Vercel URL to backend CORS
3. ✅ Test the application

---

## 📝 Quick Reference

**Vercel Settings:**
- Root Directory: `frontend`
- Build Command: `npm run build`
- Output Directory: `dist`
- Framework: Vite

**Required Env Var:**
- `VITE_API_URL` = Your Render backend URL

