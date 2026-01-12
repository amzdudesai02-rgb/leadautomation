# 📊 Google Sheets API Setup (10 Minutes)

## 🎯 Goal: Get Google Sheets API Credentials

**Time:** 10 minutes  
**Difficulty:** Medium  
**Cost:** FREE

---

## 📋 Step-by-Step

### **Step 1: Create Google Cloud Project**

1. Go to: https://console.cloud.google.com/
2. Click **"Select a project"** (top bar)
3. Click **"New Project"**
4. Project name: **"Lead Generation Tool"**
5. Click **"Create"**
6. Wait for project to be created
7. Select the new project

---

### **Step 2: Enable Google Sheets API**

1. In Google Cloud Console, go to **"APIs & Services"** → **"Library"**
2. Search for: **"Google Sheets API"**
3. Click on **"Google Sheets API"**
4. Click **"Enable"** button
5. Wait for it to enable

**✅ Done when:** Shows "API enabled"

---

### **Step 3: Create Service Account**

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** (top bar)
3. Select **"Service Account"**
4. Fill in:
   - **Service account name:** `lead-gen-tool`
   - **Service account ID:** (auto-filled)
   - **Description:** `Service account for Lead Generation Tool`
5. Click **"Create and Continue"**
6. Skip role assignment → Click **"Continue"**
7. Skip grant access → Click **"Done"**

---

### **Step 4: Create JSON Key**

1. In Credentials page, find your service account
2. Click on the service account email
3. Go to **"Keys"** tab
4. Click **"Add Key"** → **"Create New Key"**
5. Select **"JSON"**
6. Click **"Create"**
7. **JSON file downloads automatically**

---

### **Step 5: Save Credentials File**

1. **Move downloaded file** to `backend/` folder
2. **Rename it to:** `credentials.json` (or keep original name)
3. **Remember the filename!**

**Example location:**
```
backend/credentials.json
```

---

### **Step 6: Add to `.env`**

Edit `backend/.env` and add:

```env
# Google Sheets API
GOOGLE_SHEETS_CREDENTIALS=backend/credentials.json
GOOGLE_SHEETS_SHEET_ID=your_sheet_id_here
```

**Note:** `GOOGLE_SHEETS_SHEET_ID` - you'll create a sheet later and get the ID

---

## 📝 Create Google Sheet (Optional - Later)

**When you're ready to use it:**

1. Go to: https://sheets.google.com/
2. Create new spreadsheet
3. Name it: "Lead Generation Data"
4. Share with service account email:
   - Click **"Share"** button
   - Add service account email (from credentials.json)
   - Give **"Editor"** access
5. Get Sheet ID from URL:
   ```
   https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
   ```
6. Copy `SHEET_ID_HERE` and add to `.env`

---

## ✅ Verification

**Test it:**

```python
# In Python console
import gspread
from google.oauth2.service_account import Credentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = Credentials.from_service_account_file('backend/credentials.json', scopes=scope)
client = gspread.authorize(creds)

print("✅ Google Sheets API working!")
```

---

## 🎯 Quick Checklist

- [ ] Created Google Cloud project
- [ ] Enabled Google Sheets API
- [ ] Created Service Account
- [ ] Created JSON key
- [ ] Downloaded credentials.json
- [ ] Moved file to backend/ folder
- [ ] Added GOOGLE_SHEETS_CREDENTIALS to .env
- [ ] Tested (optional)

---

## 🆘 Troubleshooting

### **"API not enabled":**
- Go back to APIs & Services → Library
- Search "Google Sheets API"
- Make sure it's enabled

### **"Invalid credentials":**
- Check file path in .env is correct
- Make sure file exists in backend/ folder
- Verify JSON file is not corrupted

### **"Permission denied":**
- Share Google Sheet with service account email
- Give "Editor" access

---

## ✅ Done!

**Your Google Sheets API is now configured!**

**Next:** Sign up for Amazon PA-API (you'll do this)

**See:** `COLLECT_ALL_APIS.md` for complete guide

