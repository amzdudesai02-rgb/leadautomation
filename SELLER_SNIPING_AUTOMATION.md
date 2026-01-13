# 🎯 Seller Sniping Automation - 70% Automated

## ✅ What's Implemented

**70% Automated Seller Sniping** - Hybrid approach that combines automation with human selection:

1. ✅ **Bot Scrapes Seller Storefronts** - Automatically extracts all brand names
2. ✅ **Bot Extracts All Brand Names** - Comprehensive brand extraction from products
3. ✅ **Bot Cross-Checks with Database** - Identifies new vs existing brands
4. ✅ **Bot Adds New Brands to Research Queue** - Automatically queues for research
5. ✅ **Human Selection & Verification** - Select sellers to target, verify brand quality

---

## 🤖 What Automation Does (70%)

### 1. Bot Scrapes Target Seller Storefronts

**Automated Process:**
- ✅ Navigates to seller storefront URL
- ✅ Scrapes multiple pages (up to 10 pages)
- ✅ Extracts product information
- ✅ Handles pagination automatically
- ✅ Waits for page loads

**Pages Scraped:**
- Seller storefront homepage
- Product listing pages
- Multiple pages if available

---

### 2. Bot Extracts All Brand Names

**Extraction Methods:**

#### Method 1: Brand Links & Attributes
- Extracts from brand links (`/s?k=` links)
- Extracts from data attributes (`data-brand`)
- Extracts from brand spans and elements

#### Method 2: Product Titles
- Extracts brand from product titles
- Brand usually appears as first 1-3 words
- Filters out common non-brand words

#### Method 3: HTML Source Analysis
- Searches for brand patterns in HTML
- Looks for `data-brand`, `brandName`, etc.
- Uses regex patterns to find brands

**Brand Filtering:**
- Filters out common words (Amazon, Seller, Store, etc.)
- Filters out URLs and emails
- Filters out numbers-only text
- Validates brand name format

---

### 3. Bot Cross-Checks with Database

**Cross-Check Process:**
- ✅ Gets all existing brands from database
- ✅ Compares extracted brands with existing
- ✅ Identifies new brands (not in database)
- ✅ Identifies existing brands (already in database)
- ✅ Fuzzy matching for similar brand names

**Results:**
- **New Brands:** Brands not found in database
- **Existing Brands:** Brands already in database
- **Similar Brands:** Brands with similar names (flagged)

---

### 4. Bot Adds New Brands to Research Queue

**Queue Management:**
- ✅ Adds only new brands to queue
- ✅ Skips existing brands
- ✅ Sets priority level
- ✅ Tracks source (seller_sniping)
- ✅ Stores metadata (seller URL, extraction date)

**Queue Status:**
- `pending` - Waiting for research
- `in_progress` - Currently being researched
- `completed` - Research finished
- `skipped` - Manually skipped

---

## 👤 What Human Does (30%)

### 1. Select Which Sellers to Target

**Human Selection:**
- Choose seller URLs to snipe
- Select based on criteria:
  - Seller reputation
  - Product categories
  - Seller performance
  - Strategic value

**Selection Criteria:**
- High-performing sellers
- Niche market sellers
- Competitor sellers
- Strategic targets

---

### 2. Verify Brand Quality

**Quality Verification:**
- ✅ Review extracted brand names
- ✅ Verify brand names are correct
- ✅ Remove false positives
- ✅ Correct misspellings
- ✅ Merge duplicate entries

**Quality Checks:**
- Brand name accuracy
- Brand relevance
- Brand legitimacy
- Brand uniqueness

---

## 📊 Data Structure

### Seller Sniping Result:

```json
{
  "success": true,
  "automation_percentage": 70,
  "seller_url": "https://www.amazon.com/s?me=SELLER_ID",
  "brands_found": 45,
  "brands_list": [
    "Brand Name 1",
    "Brand Name 2",
    "Brand Name 3"
  ],
  "new_brands": [
    "Brand Name 1",
    "Brand Name 3"
  ],
  "existing_brands": [
    "Brand Name 2"
  ],
  "brands_queued": [
    "Brand Name 1",
    "Brand Name 3"
  ],
  "needs_human_review": true,
  "human_tasks": [
    "Review extracted brands for quality",
    "Select which brands to research",
    "Verify brand names are correct",
    "Approve brands for research queue"
  ],
  "created_at": "2026-01-12 11:00:00"
}
```

---

## 🚀 Usage

### Via API:

```bash
POST /api/sellers/snipe
{
  "url": "https://www.amazon.com/s?me=SELLER_ID",
  "auto_queue": true
}
```

### Response:

```json
{
  "success": true,
  "message": "Seller sniping completed (70% Automated)",
  "automation_percentage": 70,
  "data": {
    "brands_found": 45,
    "new_brands": 30,
    "existing_brands": 15,
    "brands_queued": 30
  }
}
```

### Via Python:

```python
from app.services.seller_service import SellerService

service = SellerService()
result = service.snipe_seller(
    seller_url="https://www.amazon.com/s?me=SELLER_ID",
    auto_queue=True
)
print(f"Found {result['brands_found']} brands")
print(f"New brands: {len(result['new_brands'])}")
```

---

## 🔧 Configuration

### Adjust Page Limit:

Edit `backend/app/scrapers/seller_scraper.py`:

```python
brands = scraper.extract_brands_from_storefront(url, max_pages=10)  # Change 10 to desired limit
```

### Enable/Disable Auto-Queue:

```python
# Auto-queue enabled (default)
result = service.snipe_seller(url, auto_queue=True)

# Manual queue (human selects brands)
result = service.snipe_seller(url, auto_queue=False)
```

---

## 📋 Workflow

### Step 1: Human Selects Sellers (5 minutes)
- Identify target sellers
- Collect seller URLs
- Prioritize sellers

### Step 2: Bot Scrapes Storefronts (Automated)
- Bot navigates to seller URL
- Bot scrapes multiple pages
- Bot extracts all brand names

### Step 3: Bot Cross-Checks Database (Automated)
- Bot compares with existing brands
- Bot identifies new brands
- Bot flags existing brands

### Step 4: Bot Adds to Queue (Automated)
- Bot adds new brands to research queue
- Bot sets priority and metadata
- Bot skips existing brands

### Step 5: Human Verifies Quality (10 minutes)
- Review extracted brands
- Verify brand names
- Remove false positives
- Approve for research

**Total Time: ~15 minutes** (vs 30 minutes manual)

---

## 🎯 Expected Results

### Example Output:

**Seller Storefront Analysis:**
- **Brands Found:** 45 unique brands
- **New Brands:** 30 brands (not in database)
- **Existing Brands:** 15 brands (already in database)
- **Queued for Research:** 30 brands

**Brand Extraction:**
- Extracted from product titles
- Extracted from brand links
- Extracted from HTML attributes
- Filtered and deduplicated

---

## 🐛 Troubleshooting

### Issue: No Brands Found

**Solutions:**
- Check seller URL is correct
- Verify seller has products listed
- Check if storefront is accessible
- Try increasing page limit

### Issue: Too Many False Positives

**Solutions:**
- Adjust brand filtering logic
- Improve `_is_likely_brand_name()` function
- Add more exclusion words
- Enhance brand validation

### Issue: Brands Not Extracting

**Solutions:**
- Check Amazon page structure changed
- Update CSS selectors
- Verify Selenium is working
- Check page load timing

### Issue: Database Cross-Check Slow

**Solutions:**
- Optimize database queries
- Add caching for brand names
- Use batch lookups
- Index brand name column

---

## 📝 Summary

**Automation Benefits:**
- ✅ 70% automated seller sniping
- ✅ Automatic brand extraction
- ✅ Database cross-checking
- ✅ Research queue management
- ✅ Multi-page scraping

**Human Tasks:**
- Select sellers to target
- Verify brand quality
- Approve for research

**Time Saved:**
- **Before:** 30 minutes manual work
- **After:** 15 minutes (5 min selection + 10 min verification)
- **Efficiency:** 2x faster

---

## 🚀 Next Steps

1. **Select Sellers:**
   - Identify target sellers
   - Collect seller URLs

2. **Run Sniping:**
   ```bash
   POST /api/sellers/snipe
   {"url": "seller_url"}
   ```

3. **Review Results:**
   - Check extracted brands
   - Verify quality
   - Approve for research

4. **Brands Auto-Queued:**
   - New brands added to research queue
   - Ready for brand research automation

---

**Built for efficient seller sniping with 70% automation! 🎉**

