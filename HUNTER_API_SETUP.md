# 📧 Hunter.io API Setup Guide

## 🎯 For Your Lead Generation Tool

Based on your application, select these goals:

### ✅ **Select These Options:**

1. **"Find email addresses"** ✅
   - **Why:** Your tool needs to find emails for sellers and brands
   - **Use case:** Seller scraping, brand research

2. **"Integrate via API"** ✅
   - **Why:** Your backend uses Hunter.io API to find emails
   - **Use case:** Automated email finding in your application

### ⚠️ **Optional (But Useful):**

3. **"Verify email addresses"** ✅
   - **Why:** Verify emails before saving to database
   - **Use case:** Data quality assurance

---

## 📋 Setup Steps

### Step 1: Complete Hunter.io Onboarding

1. **Select goals:**
   - ✅ Find email addresses
   - ✅ Integrate via API
   - ✅ Verify email addresses (optional)

2. **Click "Continue →"**

3. **Complete your profile** (if asked)

### Step 2: Get Your API Key

1. **Go to:** https://hunter.io/api-keys
2. **Or:** Dashboard → Settings → API Keys
3. **Copy your API key**

**It looks like:**
```
abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
```

### Step 3: Add to Your Application

**Edit `backend/.env` file:**

```env
# Hunter.io Email Finder API
HUNTER_API_KEY=your_api_key_here
```

**Replace `your_api_key_here` with your actual API key!**

### Step 4: Restart Backend

```powershell
cd backend
python run.py
```

---

## 🔍 How It Works in Your App

### **Seller Scraping:**
```
1. User enters Amazon seller URL
2. Backend scrapes seller info
3. Hunter.io API finds seller email
4. Email saved to database
```

### **Brand Research:**
```
1. User enters brand name
2. Domain Validator checks brand domain
3. Hunter.io API finds contact email
4. Email saved to database
```

---

## 💰 Hunter.io Pricing

### **Free Tier:**
- ✅ 25 email searches/month
- ✅ Basic features
- ✅ Perfect for testing

### **Paid Plans:**
- **Starter:** $49/month - 1,000 searches
- **Growth:** $149/month - 10,000 searches
- **Pro:** $499/month - 50,000 searches

**Start with free tier to test!**

---

## 🧪 Test Your API Key

**After adding to `.env`, test it:**

```python
# In Python console
from app.services.email_finder_service import EmailFinderService

service = EmailFinderService()
result = service.find_email('amazon.com', 'Jeff', 'Bezos')
print(result)
```

**Or test via API:**
```bash
curl "https://api.hunter.io/v2/email-finder?domain=amazon.com&api_key=YOUR_KEY"
```

---

## ✅ Verification

**Check if API key works:**

1. **Start backend:** `python run.py`
2. **Try scraping a seller** in your app
3. **Check logs** for Hunter.io API calls
4. **Verify email** appears in database

---

## 🎯 Quick Checklist

- [ ] Selected "Find email addresses" goal
- [ ] Selected "Integrate via API" goal
- [ ] Got API key from Hunter.io dashboard
- [ ] Added `HUNTER_API_KEY` to `backend/.env`
- [ ] Restarted backend server
- [ ] Tested email finding feature

---

## 🆘 Troubleshooting

### **"API key not configured"**
- Check `HUNTER_API_KEY` in `.env` file
- Verify no extra spaces
- Restart backend

### **"API quota exceeded"**
- Free tier: 25 searches/month
- Upgrade plan or wait for reset

### **"Invalid API key"**
- Verify key is correct
- Check for typos
- Get new key from dashboard

---

## 📝 Next Steps

1. **Complete Hunter.io setup** (select goals)
2. **Get API key** from dashboard
3. **Add to `.env`** file
4. **Restart backend**
5. **Start using email finding!**

**Your Lead Generation Tool will automatically use Hunter.io to find emails!** 🚀

