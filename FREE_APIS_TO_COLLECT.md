# 🆓 Free APIs to Collect First - Priority Guide

## 🎯 Quick Summary

**Priority Order (Free APIs First):**
1. ✅ **Hunter.io** - Already collected! (25 free searches/month)
2. ✅ **Gmail** - Already collected! (Free SMTP)
3. ✅ **Google Sheets** - Credentials collected, just need Sheet ID (Free)
4. ⚠️ **Amazon PA-API** - Requires approval (Free tier available but needs signup)
5. 🔄 **Alternative Free APIs** - Listed below

---

## ✅ Already Collected (You're Good!)

### 1. **Hunter.io** ✅ DONE
- **Status:** ✅ API Key collected
- **Free Tier:** 25 searches/month
- **What it does:** Find and verify email addresses
- **Current Usage:** Used in brand research automation
- **Upgrade Needed:** Only if you exceed 25 searches/month

### 2. **Gmail** ✅ DONE
- **Status:** ✅ Credentials collected
- **Free Tier:** 500 emails/day (Gmail limit)
- **What it does:** Send automated reports and emails
- **Current Usage:** End of day reports, email notifications
- **Upgrade Needed:** Never (unless you need more than 500/day)

### 3. **Google Sheets API** ✅ ALMOST DONE
- **Status:** ✅ Credentials file collected
- **Free Tier:** Unlimited (within Google quotas)
- **What it does:** Backup data to Google Sheets
- **What's Missing:** Just need to create a Sheet and add Sheet ID
- **Setup Time:** 2 minutes

---

## ⚠️ Needs Collection (Free Options)

### 4. **Amazon PA-API** ⚠️ REQUIRES SIGNUP
- **Status:** ❌ Not collected yet
- **Free Tier:** Yes, but requires approval
- **What it does:** Get product data, prices, seller info
- **Why Important:** Needed for QA analysis automation
- **Difficulty:** Medium (requires Amazon Associates approval)

**How to Get (Free):**
1. Go to: https://affiliate-program.amazon.com/
2. Sign up for Associates Program (free)
3. Apply for Product Advertising API access
4. Wait for approval (1-3 days)
5. Get your credentials:
   - Access Key ID
   - Secret Access Key
   - Associate Tag

**Free Tier Limits:**
- Varies by approval level
- Usually 1 request per second
- No monthly limit (but rate limited)

---

## 🔄 Alternative Free APIs (If Amazon PA-API Takes Time)

### Option A: **RapidAPI - Amazon Product API** (Free Tier)
- **Status:** Not integrated yet
- **Free Tier:** 500 requests/month
- **What it does:** Similar to Amazon PA-API
- **Setup:** Sign up at rapidapi.com (free)
- **Pros:** Faster approval, easier setup
- **Cons:** Lower free tier limit

**How to Get:**
1. Go to: https://rapidapi.com/
2. Sign up (free)
3. Search for "Amazon Product API"
4. Subscribe to free tier
5. Get API key

---

### Option B: **Clearbit API** (Free Tier)
- **Status:** Not integrated yet
- **Free Tier:** 50 requests/month
- **What it does:** Company data, domain info, employee count
- **Use Case:** Enhanced brand research
- **Setup:** Sign up at clearbit.com (free)

**How to Get:**
1. Go to: https://clearbit.com/
2. Sign up for free account
3. Get API key from dashboard
4. Free tier: 50 requests/month

---

### Option C: **FullContact API** (Free Tier)
- **Status:** Not integrated yet
- **Free Tier:** 100 requests/month
- **What it does:** Person and company enrichment
- **Use Case:** Find contact info, social profiles
- **Setup:** Sign up at fullcontact.com (free)

**How to Get:**
1. Go to: https://www.fullcontact.com/
2. Sign up for free account
3. Get API key
4. Free tier: 100 requests/month

---

### Option D: **LinkedIn API** (Free Tier)
- **Status:** Not integrated yet
- **Free Tier:** Limited (requires LinkedIn Developer account)
- **What it does:** Company data, employee info
- **Use Case:** Find brand LinkedIn profiles
- **Setup:** Requires LinkedIn Developer account

**Note:** LinkedIn API has strict requirements and limited free tier.

---

## 📋 Recommended Collection Order

### **Phase 1: Complete Current Setup (5 minutes)**
1. ✅ Hunter.io - Already done!
2. ✅ Gmail - Already done!
3. ⚠️ **Google Sheets Sheet ID** - Just need to:
   - Create a Google Sheet
   - Share with service account (email in `credentials.json`)
   - Copy Sheet ID from URL
   - Add to `.env`: `GOOGLE_SHEETS_SHEET_ID=your_id`

### **Phase 2: Amazon PA-API (1-3 days wait)**
1. Sign up for Amazon Associates Program
2. Apply for PA-API access
3. Wait for approval
4. Get credentials
5. Add to `.env`

### **Phase 3: Alternative APIs (If Needed)**
1. RapidAPI (if Amazon takes too long)
2. Clearbit (for enhanced brand data)
3. FullContact (for contact enrichment)

---

## 🚀 Quick Start Guide

### Step 1: Complete Google Sheets Setup (2 minutes)

1. **Create Google Sheet:**
   - Go to: https://sheets.google.com
   - Create new spreadsheet
   - Name it: "Lead Generation Data"

2. **Share with Service Account:**
   - Click "Share" button
   - Get service account email from `backend/credentials.json`
   - Look for: `"client_email": "xxx@xxx.iam.gserviceaccount.com"`
   - Share sheet with that email (Editor access)

3. **Get Sheet ID:**
   - Look at URL: `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`
   - Copy the `SHEET_ID_HERE` part

4. **Add to `.env`:**
   ```env
   GOOGLE_SHEETS_SHEET_ID=your_sheet_id_here
   ```

**Done!** ✅ Google Sheets backup now works.

---

### Step 2: Amazon PA-API (When Ready)

1. **Sign Up:**
   - Go to: https://affiliate-program.amazon.com/
   - Click "Join Now for Free"
   - Complete signup

2. **Apply for PA-API:**
   - After Associates account approved
   - Go to: https://webservices.amazon.com/paapi5/documentation/register-for-product-advertising-api.html
   - Apply for API access
   - Wait 1-3 days for approval

3. **Get Credentials:**
   - Once approved, go to Associates Central
   - Navigate to Product Advertising API
   - Get:
     - Access Key ID
     - Secret Access Key
     - Associate Tag

4. **Add to `.env`:**
   ```env
   AMAZON_API_KEY=your_access_key_id
   AMAZON_SECRET_KEY=your_secret_access_key
   AMAZON_ASSOCIATE_TAG=your_associate_tag
   ```

**Done!** ✅ Amazon API now works.

---

## 💰 Cost Summary

| API | Free Tier | Paid Tier | When to Upgrade |
|-----|-----------|-----------|-----------------|
| **Hunter.io** | 25/month | $49/month (1,000) | If you need >25 searches/month |
| **Gmail** | 500/day | N/A | Never needed |
| **Google Sheets** | Unlimited* | N/A | Never needed |
| **Amazon PA-API** | Free** | Usage-based | If you exceed rate limits |
| **RapidAPI** | 500/month | $9/month (5,000) | If you need >500/month |
| **Clearbit** | 50/month | $99/month (1,000) | If you need >50/month |
| **FullContact** | 100/month | $99/month (1,000) | If you need >100/month |

*Within Google quotas (very generous)
**After approval, rate-limited but free

---

## 🎯 What You Should Do RIGHT NOW

### **Immediate (5 minutes):**
1. ✅ Complete Google Sheets setup (just need Sheet ID)
   - This enables data backup functionality

### **This Week:**
2. ⚠️ Sign up for Amazon PA-API
   - Start the approval process
   - Takes 1-3 days, so start early

### **If Amazon Takes Too Long:**
3. 🔄 Sign up for RapidAPI (backup option)
   - Faster approval
   - Can use while waiting for Amazon

---

## 📊 Current Status

### ✅ **Working Right Now:**
- Hunter.io (25 free searches/month)
- Gmail (500 emails/day)
- Database (PostgreSQL - Neon)

### ⚠️ **Needs 2-Minute Setup:**
- Google Sheets (just need Sheet ID)

### ⏳ **Needs Signup (Free):**
- Amazon PA-API (requires approval)

### 🔄 **Optional (Free Alternatives):**
- RapidAPI Amazon Product API
- Clearbit
- FullContact

---

## 🆘 Need Help?

**If you want me to:**
1. **Add Google Sheets Sheet ID** - Just provide the Sheet ID and I'll add it
2. **Integrate RapidAPI** - Tell me if you want this as backup
3. **Add other free APIs** - Tell me which one and I'll integrate it
4. **Help with Amazon signup** - I can guide you through the process

**Just tell me what you need!** 🚀

---

## 📝 Summary

**You Already Have:**
- ✅ Hunter.io (free tier)
- ✅ Gmail (free)
- ✅ Google Sheets credentials (just need Sheet ID)

**You Need:**
- ⚠️ Google Sheets Sheet ID (2 minutes)
- ⚠️ Amazon PA-API (1-3 days approval)

**Optional:**
- 🔄 RapidAPI (backup for Amazon)
- 🔄 Clearbit (enhanced brand data)
- 🔄 FullContact (contact enrichment)

**Total Cost: $0** (all free tiers) 💰

---

**Start with Google Sheets Sheet ID - it's the quickest win!** 🎯

