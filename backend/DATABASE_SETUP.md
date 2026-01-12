# PostgreSQL Database Setup Guide

## Prerequisites

1. **Install PostgreSQL**
   - Download from: https://www.postgresql.org/download/
   - Or use Docker: `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres`

2. **Create Database**
   ```sql
   CREATE DATABASE lead_generation;
   ```

## Configuration

Add to `backend/.env`:

```env
# PostgreSQL Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lead_generation
DB_USER=postgres
DB_PASSWORD=postgres

# Or use full DATABASE_URL
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/lead_generation
```

## Setup Database

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Run Setup Script
```bash
python database_setup.py
```

This will:
- ✅ Create all database tables
- ✅ Create default admin user
  - Username: `admin`
  - Password: `admin123`

### Step 3: Change Admin Password
After first login, change the admin password!

## Database Tables Created

1. **users** - User accounts and authentication
2. **sellers** - Seller information
3. **brands** - Brand information
4. **qa_analyses** - QA analysis results
5. **audit_logs** - User activity logs

## Migrations (Optional)

If you want to use Flask-Migrate for migrations:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Verify Setup

```bash
python run.py
```

Check logs for: `✅ Database tables created successfully!`

## Troubleshooting

### Connection Error
- Check PostgreSQL is running
- Verify credentials in `.env`
- Check firewall settings

### Table Creation Error
- Ensure database exists
- Check user has CREATE privileges
- Verify connection string

## Default Admin Account

**Username:** admin  
**Password:** admin123

⚠️ **Change this password immediately after first login!**

