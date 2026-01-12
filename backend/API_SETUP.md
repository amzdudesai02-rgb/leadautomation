# API Setup Guide

This guide explains how to set up all required APIs for the Lead Generation Tool.

## Required APIs

### 1. Google Sheets API (Already Configured)
- **Status**: ✅ Already integrated
- **Cost**: Free
- **Setup**: 
  1. Go to [Google Cloud Console](https://console.cloud.google.com/)
  2. Create a new project or select existing
  3. Enable Google Sheets API and Google Drive API
  4. Create Service Account credentials
  5. Download JSON credentials file
  6. Set `GOOGLE_SHEETS_CREDENTIALS` in `.env` to path of credentials file
  7. Set `GOOGLE_SHEETS_SHEET_ID` to your Google Sheet ID

### 2. Amazon Product Advertising API (PA-API 5.0)
- **Status**: ⚠️ Needs Setup
- **Cost**: Free tier available, then pay-per-request
- **Setup**:
  1. Go to [Amazon Associates Central](https://affiliate-program.amazon.com/)
  2. Sign up for Amazon Associates account
  3. Apply for Product Advertising API access
  4. Once approved, get your:
     - Access Key ID
     - Secret Access Key
     - Associate Tag
  5. Add to `.env`:
     ```
     AMAZON_API_KEY=your-access-key-id
     AMAZON_SECRET_KEY=your-secret-access-key
     AMAZON_ASSOCIATE_TAG=your-associate-tag
     AMAZON_ENDPOINT=webservices.amazon.com
     AMAZON_REGION=us-east-1
     AMAZON_MARKETPLACE=www.amazon.com
     ```

### 3. Hunter.io Email Finder API
- **Status**: ⚠️ Optional but Recommended
- **Cost**: Free tier (25 searches/month), then $49/month
- **Setup**:
  1. Go to [Hunter.io](https://hunter.io/)
  2. Sign up for free account
  3. Get your API key from dashboard
  4. Add to `.env`:
     ```
     HUNTER_API_KEY=your-hunter-api-key
     ```

### 4. Gmail API (Optional)
- **Status**: ⚠️ Optional
- **Cost**: Free (2,000 emails/day)
- **Setup**:
  1. Enable Gmail API in Google Cloud Console
  2. Create OAuth 2.0 credentials
  3. Or use App Password for SMTP
  4. Add to `.env`:
     ```
     GMAIL_USER=your-email@gmail.com
     GMAIL_PASSWORD=your-app-password
     ```

## Environment Variables

Create a `.env` file in the `backend` directory with:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
PORT=5000

# Google Sheets
GOOGLE_SHEETS_CREDENTIALS=path/to/credentials.json
GOOGLE_SHEETS_SHEET_ID=your-sheet-id

# Amazon Product Advertising API
AMAZON_API_KEY=your-amazon-api-key
AMAZON_SECRET_KEY=your-amazon-secret-key
AMAZON_ASSOCIATE_TAG=your-associate-tag
AMAZON_ENDPOINT=webservices.amazon.com
AMAZON_REGION=us-east-1
AMAZON_MARKETPLACE=www.amazon.com

# Email Finder (Hunter.io)
HUNTER_API_KEY=your-hunter-api-key

# Gmail (Optional)
GMAIL_USER=your-email@gmail.com
GMAIL_PASSWORD=your-app-password

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Logging
LOG_LEVEL=INFO
```

## API Features Implemented

### ✅ Seller Scraper
- Web scraping with Selenium
- Email finding with Hunter.io
- Domain extraction

### ✅ Brand Researcher
- Domain validation
- Social media discovery
- Email finding
- Website scraping

### ✅ QA Analyzer
- Amazon product search
- Price extraction
- Profit margin calculation
- Competition scoring

## Testing APIs

### Test Amazon API
```python
from app.services.amazon_api_service import AmazonAPIService

amazon = AmazonAPIService()
products = amazon.search_products("laptop", item_count=5)
print(products)
```

### Test Email Finder
```python
from app.services.email_finder_service import EmailFinderService

email_finder = EmailFinderService()
email = email_finder.find_email("example.com", "John", "Doe")
print(email)
```

### Test Domain Validator
```python
from app.services.domain_validator_service import DomainValidatorService

validator = DomainValidatorService()
result = validator.validate_domain("example.com")
print(result)
```

## Troubleshooting

### Amazon API Issues
- Ensure Associate Tag is correct
- Check API credentials are valid
- Verify region and endpoint match
- Check API request limits

### Email Finder Issues
- Verify API key is correct
- Check free tier limits (25/month)
- Ensure domain is valid

### Google Sheets Issues
- Verify credentials file path
- Check sheet ID is correct
- Ensure service account has access
- Verify API is enabled in Google Cloud Console

## Cost Summary

| API | Free Tier | Paid Tier |
|-----|-----------|-----------|
| Google Sheets | ✅ Free | Free |
| Amazon PA-API | Limited | Pay-per-request |
| Hunter.io | 25/month | $49/month |
| Gmail API | 2,000/day | Free |

**Total Minimum Cost**: $0 (using free tiers)
**Recommended Setup**: ~$49/month (Hunter.io paid tier)

