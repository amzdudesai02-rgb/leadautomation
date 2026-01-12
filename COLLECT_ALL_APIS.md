# 🔑 Collect All API Keys - Complete Guide

## 📋 API Collection Checklist

Collect all API keys first, then configure Amazon PA-API last!

---

## ✅ Already Collected

1. **Hunter.io API** ✅
   - Key: `7c7f121c20fe6a4ab540820c3d79c3db35b9844b`
   - Status: Configured in `.env`

---

## 📝 APIs to Collect (In Order)

### 🥇 **#1: Gmail API** (Free & Easy)

**Why First:** Simple setup, free, useful for reports

**Steps:**
1. Go to: https://myaccount.google.com/
2. Go to **Security** → **2-Step Verification** (enable if not enabled)
3. Go to **Security** → **App Passwords**
4. Create app password for "Mail"
5. Copy the 16-character password

**What You'll Get:**
- Gmail username (your email)
- App password (16 characters)

**Save These:**
```
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=your_app_password_16chars
```

**Time:** 5 minutes

---

### 🥈 **#2: Google Sheets API** (Free & Easy)

**Why Second:** Free, useful for data backup

**Steps:**
1. Go to: https://console.cloud.google.com/
2. Create new project (or select existing)
3. Enable **Google Sheets API**:
   - Go to **APIs & Services** → **Library**
   - Search "Google Sheets API"
   - Click **Enable**
4. Create credentials:
   - Go to **APIs & Services** → **Credentials**
   - Click **Create Credentials** → **Service Account**
   - Name it (e.g., "lead-gen-tool")
   - Click **Create and Continue**
   - Skip role assignment → **Continue** → **Done**
5. Click on service account → **Keys** tab
6. Click **Add Key** → **Create New Key** → **JSON**
7. Download JSON file

**What You'll Get:**
- JSON credentials file (save it in `backend/` folder)

**Save This:**
```
GOOGLE_SHEETS_CREDENTIALS=backend/credentials.json
GOOGLE_SHEETS_SHEET_ID=your_sheet_id (create later)
```

**Time:** 10 minutes

---

### 🥉 **#3: Amazon PA-API** (Do This LAST)

**Why Last:** Requires sales to maintain, most complex

**Steps:**
1. Go to: https://affiliate-program.amazon.com/
2. Sign up for Amazon Associates
3. Complete registration
4. Go to **Product Advertising API** section
5. Request API credentials
6. Get credentials:
   - Access Key ID
   - Secret Access Key
   - Associate Tag

**What You'll Get:**
- Access Key ID
- Secret Access Key
- Associate Tag

**Save These:**
```
AMAZON_API_KEY=your_access_key
AMAZON_SECRET_KEY=your_secret_key
AMAZON_ASSOCIATE_TAG=your_associate_tag
```

**Time:** 15-20 minutes (includes approval wait)

**Note:** Do this AFTER collecting other APIs!

---

## 📊 Collection Order Summary

| # | API | Time | Difficulty | Status |
|---|-----|------|------------|--------|
| ✅ | Hunter.io | Done | Easy | ✅ Collected |
| 1 | Gmail API | 5 min | Easy | ⏳ Collect |
| 2 | Google Sheets | 10 min | Medium | ⏳ Collect |
| 3 | Amazon PA-API | 15-20 min | Hard | ⏳ Collect Last |

---

## 🎯 Quick Collection Guide

### **Step 1: Gmail API (5 minutes)**

1. **Enable 2-Step Verification:**
   - https://myaccount.google.com/security
   - Enable if not already enabled

2. **Create App Password:**
   - Security → App Passwords
   - Select "Mail" → Generate
   - Copy 16-character password

3. **Save:**
   ```
   GMAIL_USER=your_email@gmail.com
   GMAIL_PASSWORD=xxxx xxxx xxxx xxxx
   ```

---

### **Step 2: Google Sheets API (10 minutes)**

1. **Go to Google Cloud Console:**
   - https://console.cloud.google.com/

2. **Create Project:**
   - Click "New Project"
   - Name: "Lead Generation Tool"
   - Create

3. **Enable Google Sheets API:**
   - APIs & Services → Library
   - Search "Google Sheets API"
   - Enable

4. **Create Service Account:**
   - APIs & Services → Credentials
   - Create Credentials → Service Account
   - Name: "lead-gen-tool"
   - Create → Continue → Done

5. **Create Key:**
   - Click service account → Keys tab
   - Add Key → Create New Key → JSON
   - Download file

6. **Save file as:** `backend/credentials.json`

7. **Save to .env:**
   ```
   GOOGLE_SHEETS_CREDENTIALS=backend/credentials.json
   ```

---

### **Step 3: Amazon PA-API (15-20 minutes) - DO LAST**

1. **Sign up:**
   - https://affiliate-program.amazon.com/
   - Complete registration

2. **Get API Credentials:**
   - Go to Product Advertising API section
   - Request credentials
   - Get Access Key, Secret Key, Associate Tag

3. **Save:**
   ```
   AMAZON_API_KEY=your_access_key
   AMAZON_SECRET_KEY=your_secret_key
   AMAZON_ASSOCIATE_TAG=your_associate_tag
   ```

---

## 📝 Collection Checklist

### **Gmail API:**
- [ ] Enabled 2-Step Verification
- [ ] Created App Password
- [ ] Copied 16-character password
- [ ] Saved GMAIL_USER
- [ ] Saved GMAIL_PASSWORD

### **Google Sheets API:**
- [ ] Created Google Cloud project
- [ ] Enabled Google Sheets API
- [ ] Created Service Account
- [ ] Downloaded JSON credentials file
- [ ] Saved file to backend/ folder
- [ ] Saved GOOGLE_SHEETS_CREDENTIALS path

### **Amazon PA-API:**
- [ ] Signed up for Amazon Associates
- [ ] Got Access Key ID
- [ ] Got Secret Access Key
- [ ] Got Associate Tag
- [ ] Saved all three credentials

---

## 🔧 After Collecting All APIs

### **Step 1: Update `.env` File**

Add all collected API keys to `backend/.env`:

```env
# Hunter.io (Already done ✅)
HUNTER_API_KEY=7c7f121c20fe6a4ab540820c3d79c3db35b9844b

# Gmail API
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
MANAGER_EMAILS=manager1@email.com,manager2@email.com

# Google Sheets API
GOOGLE_SHEETS_CREDENTIALS=backend/credentials.json
GOOGLE_SHEETS_SHEET_ID=your_sheet_id

# Amazon PA-API (Do this last!)
AMAZON_API_KEY=your_access_key
AMAZON_SECRET_KEY=your_secret_key
AMAZON_ASSOCIATE_TAG=your_associate_tag
```

### **Step 2: Restart Backend**

```powershell
cd backend
python run.py
```

---

## ✅ Summary

**Collection Order:**
1. ✅ Hunter.io - DONE
2. ⏳ Gmail API - Collect next (5 min)
3. ⏳ Google Sheets API - Collect second (10 min)
4. ⏳ Amazon PA-API - Collect LAST (15-20 min)

**Why This Order:**
- Gmail & Google Sheets: Easy, free, no requirements
- Amazon PA-API: Requires sales, do last

**After Collecting:**
- Add all keys to `.env`
- Restart backend
- All APIs will work automatically!

---

## 🎯 Next Steps

1. **Collect Gmail API** (5 minutes)
2. **Collect Google Sheets API** (10 minutes)
3. **Sign up for Amazon PA-API** (you'll do this)
4. **Add all to `.env`** (after collecting)
5. **Restart backend** (to activate all APIs)

**Start with Gmail API - it's the easiest!** 🚀

