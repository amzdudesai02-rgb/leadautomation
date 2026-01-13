# 🤖 SmartScout Morning Automation Setup

## ✅ What's Implemented

**90% Automated Morning Setup** - Complete automation system that:

1. ✅ **Opens SmartScout** - Automated browser opens SmartScout platform
2. ✅ **Applies Filters** - Automatically applies configured filters
3. ✅ **Extracts 50-100 Brands** - Automatically extracts brand data
4. ✅ **Populates Google Sheets** - Automatically saves to Google Sheets
5. ✅ **Checks Duplicates** - Automatically detects and flags duplicates

---

## 📋 Setup Instructions

### Step 1: Add SmartScout Credentials

Add to `backend/.env`:

```env
# SmartScout Configuration
SMARTSCOUT_USERNAME=your_smartscout_email@example.com
SMARTSCOUT_PASSWORD=your_smartscout_password
SMARTSCOUT_URL=https://app.smartscout.com
```

### Step 2: Install ChromeDriver (if not already installed)

The automation uses Selenium with Chrome. Make sure ChromeDriver is installed:

**Windows:**
```bash
# Download from: https://chromedriver.chromium.org/
# Or use Chocolatey:
choco install chromedriver
```

**Mac:**
```bash
brew install chromedriver
```

**Linux:**
```bash
sudo apt-get install chromium-chromedriver
```

### Step 3: Configure Google Sheets

Make sure Google Sheets is configured:
1. Sheet ID is set in `.env`: `GOOGLE_SHEETS_SHEET_ID=your_sheet_id`
2. Credentials file exists: `backend/credentials.json`
3. Sheet has "Brands" worksheet

### Step 4: Test the Automation

**Via API:**
```bash
POST /api/automation/morning-setup
{
  "smartscout_enabled": true,
  "brand_count": 100
}
```

**Via Python:**
```python
from app.services.automation_service import AutomationService

service = AutomationService()
result = service.morning_setup(smartscout_enabled=True, brand_count=100)
print(result)
```

---

## 🎯 How It Works

### 1. **Bot Opens SmartScout**
- Uses Selenium WebDriver
- Opens Chrome browser (can run headless)
- Navigates to SmartScout URL
- Logs in automatically

### 2. **Bot Applies Filters**
- Clicks filter button/panel
- Applies configured filters:
  - Country (default: US)
  - Min/Max Revenue
  - Product Count
  - Category
- Clicks "Apply Filters"

### 3. **Bot Extracts Brands**
- Scrolls through brand list
- Extracts for each brand:
  - Name
  - Domain
  - Revenue
  - Product Count
  - Category
  - Country
  - Brand URL
- Continues until target count (50-100) reached

### 4. **Bot Populates Google Sheets**
- Saves each brand to "Brands" worksheet
- Includes all extracted data
- Timestamps each entry

### 5. **Bot Checks Duplicates**
- Scans Google Sheets for duplicates
- Flags duplicate rows (highlights in yellow)
- Reports duplicate count

---

## ⚙️ Configuration Options

### Customize Filters

Edit `backend/app/services/automation_service.py`:

```python
filters = {
    'country': 'US',           # Change country
    'min_products': 1,         # Minimum products
    'min_revenue': 10000,      # Minimum revenue
    'max_revenue': 1000000,    # Maximum revenue
    'category': 'Electronics'  # Category filter
}
```

### Customize Brand Count

Default: 100 brands
- Minimum: 50
- Maximum: 500 (adjust based on SmartScout limits)

### Schedule Automation

Already configured in `backend/app/tasks/scheduler.py`:
- **Runs daily at 9:00 AM**
- Can be triggered manually via API

---

## 🔧 Troubleshooting

### Issue: ChromeDriver Not Found

**Solution:**
```bash
# Download ChromeDriver matching your Chrome version
# Place in PATH or same directory as script
```

### Issue: Login Fails

**Check:**
1. Credentials are correct in `.env`
2. SmartScout URL is correct
3. Account is not locked/suspended

### Issue: Filters Not Applying

**Solution:**
- SmartScout interface may have changed
- Update selectors in `smartscout_scraper.py`
- Check browser console for errors

### Issue: Brands Not Extracting

**Check:**
1. Filters are working (brands visible on page)
2. Selectors match SmartScout HTML structure
3. Page has loaded completely

### Issue: Google Sheets Not Populating

**Check:**
1. `GOOGLE_SHEETS_SHEET_ID` is set
2. `credentials.json` is valid
3. Sheet has "Brands" worksheet
4. Service account has write access

---

## 📊 Expected Results

After running automation:

**Google Sheets "Brands" Worksheet:**
```
| Name          | Domain              | Revenue | Products | Category   | Country | Extracted At        |
|---------------|---------------------|---------|----------|------------|---------|---------------------|
| Brand Name 1  | brand1.com          | $50K    | 25       | Electronics| US      | 2026-01-12 09:00:00|
| Brand Name 2  | brand2.com          | $100K   | 50       | Clothing   | US      | 2026-01-12 09:00:15|
| ...           | ...                 | ...     | ...      | ...        | ...     | ...                 |
```

**Duplicate Detection:**
- Duplicate rows highlighted in yellow
- Report shows duplicate count

---

## 🚀 Usage Examples

### Run via Frontend

Add button in Dashboard to trigger:
```javascript
const runMorningSetup = async () => {
  const response = await api.post('/api/automation/morning-setup', {
    smartscout_enabled: true,
    brand_count: 100
  });
  console.log(response.data);
};
```

### Run via Cron/Scheduled Task

Already scheduled for 9:00 AM daily.

### Run Manually

```bash
curl -X POST http://localhost:5000/api/automation/morning-setup \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"smartscout_enabled": true, "brand_count": 100}'
```

---

## 📝 Notes

- **Headless Mode**: Set `headless=True` in `_setup_driver()` for production
- **Rate Limiting**: SmartScout may have rate limits - adjust delays if needed
- **Error Handling**: Automation continues even if some brands fail
- **Logging**: All actions logged for debugging

---

## ✅ Summary

**What You Get:**
- ✅ Fully automated morning setup
- ✅ 50-100 brands extracted automatically
- ✅ Google Sheets populated automatically
- ✅ Duplicates detected and flagged automatically
- ✅ Runs daily at 9:00 AM (or on-demand)

**Time Saved:**
- **Before:** 30-60 minutes manual work
- **After:** 5 minutes (just verify results)
- **Automation:** 90% automated! 🎉

