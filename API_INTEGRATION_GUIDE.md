# 🔌 API Integration Guide - Complete Overview

## 📊 Total APIs Used: **5 External APIs**

---

## 1. 🛒 Amazon Product Advertising API (PA-API 5.0)

### **Purpose:**
- Get product information from Amazon
- Analyze product prices and competition
- Calculate profit margins for QA analysis

### **How It Works:**
```python
# Location: backend/app/services/amazon_api_service.py

1. Uses AWS Signature Version 4 authentication
2. Searches products by keywords or ASIN
3. Gets product details: price, reviews, ratings
4. Calculates profit margins
5. Analyzes competition scores
```

### **Configuration:**
```env
AMAZON_API_KEY=your_access_key
AMAZON_SECRET_KEY=your_secret_key
AMAZON_ASSOCIATE_TAG=your_associate_tag
AMAZON_REGION=us-east-1
AMAZON_MARKETPLACE=www.amazon.com
```

### **Features:**
- ✅ Product search by keywords
- ✅ Get product details by ASIN
- ✅ Price comparison
- ✅ Review analysis
- ✅ Competition scoring

### **Used In:**
- QA Analysis service
- Brand research
- Profit margin calculation

---

## 2. 📧 Hunter.io Email Finder API

### **Purpose:**
- Find email addresses for sellers and brands
- Verify email addresses
- Get contact information

### **How It Works:**
```python
# Location: backend/app/services/email_finder_service.py

1. Takes domain and name (optional)
2. Searches Hunter.io database
3. Returns best match email with confidence score
4. Provides email verification
```

### **Configuration:**
```env
HUNTER_API_KEY=your_hunter_api_key
```

### **Features:**
- ✅ Email finder by domain + name
- ✅ Email verification
- ✅ Confidence scoring
- ✅ Contact information

### **Used In:**
- Seller scraping
- Brand research
- Lead generation

---

## 3. 🌐 Domain Validator Service (Free - No API Key)

### **Purpose:**
- Validate if domains exist
- Check if websites are accessible
- Verify DNS resolution

### **How It Works:**
```python
# Location: backend/app/services/domain_validator_service.py

1. Removes protocol (http://, https://)
2. Checks DNS resolution
3. Tests HTTP/HTTPS accessibility
4. Returns validation status
```

### **Configuration:**
```env
# No API key needed - uses DNS and HTTP requests
```

### **Features:**
- ✅ DNS validation
- ✅ HTTP accessibility check
- ✅ Domain format validation
- ✅ Free - no API key required

### **Used In:**
- Brand research
- Domain validation
- Website verification

---

## 4. 📊 Google Sheets API (Optional)

### **Purpose:**
- Backup data to Google Sheets
- Export data
- Data synchronization

### **How It Works:**
```python
# Uses gspread library

1. Authenticates with Google credentials
2. Reads/writes to Google Sheets
3. Syncs database data
```

### **Configuration:**
```env
GOOGLE_SHEETS_CREDENTIALS=path_to_credentials.json
GOOGLE_SHEETS_SHEET_ID=your_sheet_id
```

### **Features:**
- ✅ Data backup
- ✅ Data export
- ✅ Real-time sync (optional)

### **Used In:**
- Data backup service
- Export functionality

---

## 5. 📨 Gmail API (Optional)

### **Purpose:**
- Send automated reports
- Email notifications
- Send leads to managers

### **How It Works:**
```python
# Uses SMTP or Gmail API

1. Authenticates with Gmail
2. Sends emails with reports
3. Sends notifications
```

### **Configuration:**
```env
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
MANAGER_EMAILS=manager1@email.com,manager2@email.com
```

### **Features:**
- ✅ Automated email reports
- ✅ Daily/weekly summaries
- ✅ Lead notifications

### **Used In:**
- Reporting service
- Email automation
- Notifications

---

## 🔄 Internal API Endpoints (Your Backend)

### **Authentication APIs:**
```
POST /api/auth/register  - Register new user
POST /api/auth/login     - Login user
GET  /api/auth/me        - Get current user
POST /api/auth/logout    - Logout user
```

### **Seller APIs:**
```
GET    /api/sellers           - Get all sellers
GET    /api/sellers/:id       - Get seller by ID
POST   /api/sellers/scrape    - Scrape seller from Amazon
PUT    /api/sellers/:id       - Update seller
DELETE /api/sellers/:id       - Delete seller
```

### **Brand APIs:**
```
GET  /api/brands           - Get all brands
GET  /api/brands/:id        - Get brand by ID
POST /api/brands/research   - Research brand information
```

### **QA Analysis APIs:**
```
POST /api/qa/analyze           - Analyze brand for QA
GET  /api/qa/metrics/:brand_id - Get QA metrics
```

### **Automation APIs:**
```
POST /api/automation/morning-setup  - Morning automation
POST /api/automation/end-of-day      - End of day automation
```

---

## 📋 API Workflow

### **Seller Scraping Flow:**
```
1. User enters Amazon seller URL
2. Backend scrapes seller page (Selenium)
3. Email Finder API finds seller email
4. Domain Validator checks seller website
5. Data saved to PostgreSQL
```

### **Brand Research Flow:**
```
1. User enters brand name
2. Domain Validator checks brand domain
3. Email Finder finds brand contact email
4. Amazon API searches brand products
5. Data saved to PostgreSQL
```

### **QA Analysis Flow:**
```
1. User selects brand
2. Amazon API searches brand products
3. Calculates profit margins
4. Analyzes competition
5. Generates QA report
6. Saves to database
```

---

## 🔑 API Keys Setup

### **Required APIs (Core Features):**
1. ❌ **Amazon API** - Optional (for QA analysis)
2. ❌ **Hunter.io** - Optional (for email finding)
3. ✅ **Domain Validator** - Free, no key needed

### **Optional APIs (Additional Features):**
4. ❌ **Google Sheets** - Optional (for backup)
5. ❌ **Gmail** - Optional (for email reports)

---

## 💰 API Costs

| API | Free Tier | Paid Plans |
|-----|-----------|------------|
| **Amazon PA-API** | Limited | Pay per request |
| **Hunter.io** | 25 searches/month | $49+/month |
| **Domain Validator** | ✅ Free | N/A |
| **Google Sheets** | ✅ Free | Free |
| **Gmail** | ✅ Free | Free |

---

## 🚀 How APIs Work Together

```
┌─────────────────┐
│  User Action    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Frontend (React)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Backend (Flask) │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌──────────────┐
│Database │ │ External APIs│
│(PostgreSQL)│ │ (Amazon, Hunter)│
└─────────┘ └──────────────┘
```

---

## 📝 API Usage Examples

### **Example 1: Scrape Seller**
```javascript
// Frontend
POST /api/sellers/scrape
{ "url": "https://amazon.com/seller/..." }

// Backend Flow:
1. Scrape seller page → Get seller info
2. Hunter.io API → Find email
3. Domain Validator → Check website
4. Save to database
```

### **Example 2: Research Brand**
```javascript
// Frontend
POST /api/brands/research
{ "brand_name": "Nike" }

// Backend Flow:
1. Domain Validator → Check nike.com
2. Hunter.io API → Find contact email
3. Amazon API → Search Nike products
4. Save to database
```

### **Example 3: QA Analysis**
```javascript
// Frontend
POST /api/qa/analyze
{ "brand_id": 123 }

// Backend Flow:
1. Get brand from database
2. Amazon API → Search products
3. Calculate profit margins
4. Analyze competition
5. Save analysis
```

---

## ✅ Summary

**Total APIs: 5**
- 1 Required (Domain Validator - Free)
- 2 Optional for core features (Amazon, Hunter.io)
- 2 Optional for extra features (Google Sheets, Gmail)

**All APIs are configured in `backend/.env` file!**

---

## 🎯 Next Steps

1. **Get API Keys:**
   - Amazon PA-API: https://affiliate-program.amazon.com/
   - Hunter.io: https://hunter.io/

2. **Add to `.env`:**
   ```env
   AMAZON_API_KEY=your_key
   HUNTER_API_KEY=your_key
   ```

3. **Start Using:**
   - APIs work automatically when configured
   - Features work without APIs (limited functionality)

**Your application works without API keys, but with limited features!**

