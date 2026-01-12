# 🚀 Lead Generation Tool

A professional lead generation automation tool for Amazon sellers, brand research, and QA analysis.

## ✨ Features

- 🔍 **Seller Sniping** - Automatically scrape and collect seller information from Amazon
- 🏢 **Brand Research** - Research brands, find contact information, validate domains
- 📊 **QA Analysis** - Analyze brands for profitability and competition
- 🔐 **Secure Authentication** - JWT-based authentication with PostgreSQL
- 📧 **Email Integration** - Hunter.io for email finding, Gmail for reports
- 📈 **Dashboard** - Professional UI with Material-UI components
- 🔄 **Automation** - Scheduled tasks and automated reporting

## 🛠️ Tech Stack

### Frontend
- React.js
- Material-UI
- Vite
- Axios
- React Router

### Backend
- Python (Flask)
- PostgreSQL (Neon Database)
- SQLAlchemy
- JWT Authentication
- Selenium (Web Scraping)

### APIs Integrated
- Hunter.io (Email Finder)
- Amazon Product Advertising API (PA-API 5.0)
- Gmail API (Email Reports)
- Google Sheets API (Data Backup)

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL (or Neon Database)
- API Keys (see Setup section)

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/amzdudesai02-rgb/leadautomation.git
cd leadautomation
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create `backend/.env` file:
```env
# Database
DATABASE_URL=your_neon_database_url

# JWT
JWT_SECRET_KEY=your_secret_key
SECRET_KEY=your_secret_key

# APIs (Optional)
HUNTER_API_KEY=your_hunter_key
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
GOOGLE_SHEETS_CREDENTIALS=backend/credentials.json
AMAZON_API_KEY=your_amazon_key
AMAZON_SECRET_KEY=your_amazon_secret
AMAZON_ASSOCIATE_TAG=your_associate_tag
```

Setup database:
```bash
python database_setup.py
```

Start backend:
```bash
python run.py
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 4. Access Application

- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- Default Login: `admin` / `admin123`

## 📚 Documentation

- [API Integration Guide](API_INTEGRATION_GUIDE.md)
- [Database Setup](POSTGRESQL_SETUP.md)
- [Neon Database Setup](NEON_SETUP_STEPS.md)
- [Complete Setup Guide](COMPLETE_SETUP_GUIDE.md)

## 🔐 Security

- Never commit `.env` files
- Never commit `credentials.json`
- Use environment variables for all secrets
- Change default admin password after first login

## 📝 License

This project is private and proprietary.

## 👤 Author

amzdudesai02-rgb

## 🔗 Links

- Repository: https://github.com/amzdudesai02-rgb/leadautomation
- Issues: https://github.com/amzdudesai02-rgb/leadautomation/issues

## ⚠️ Important Notes

- This tool is for legitimate lead generation purposes only
- Respect Amazon's terms of service
- Use APIs responsibly and within rate limits
- Keep your API keys secure

---

**Built with ❤️ for efficient lead generation**
