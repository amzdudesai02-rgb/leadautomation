# PostgreSQL Database Setup Script for Windows
# This script helps you set up the database

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PostgreSQL Database Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if PostgreSQL is running
$pgServices = Get-Service -Name postgresql* -ErrorAction SilentlyContinue
if ($pgServices) {
    Write-Host "✅ PostgreSQL services found:" -ForegroundColor Green
    $pgServices | ForEach-Object { Write-Host "   - $($_.Name): $($_.Status)" -ForegroundColor Yellow }
} else {
    Write-Host "❌ PostgreSQL services not found" -ForegroundColor Red
    Write-Host "Please install PostgreSQL first" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "Step 1: Create Database" -ForegroundColor Cyan
Write-Host "----------------------" -ForegroundColor Cyan
Write-Host ""
Write-Host "You need to create the database manually:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Option A: Using pgAdmin (Recommended)" -ForegroundColor Green
Write-Host "  1. Open pgAdmin 4 from Start Menu" -ForegroundColor White
Write-Host "  2. Connect to PostgreSQL server" -ForegroundColor White
Write-Host "  3. Right-click 'Databases' → Create → Database" -ForegroundColor White
Write-Host "  4. Name: lead_generation" -ForegroundColor White
Write-Host "  5. Click Save" -ForegroundColor White
Write-Host ""
Write-Host "Option B: Using Command Line" -ForegroundColor Green
Write-Host "  psql -U postgres" -ForegroundColor White
Write-Host "  CREATE DATABASE lead_generation;" -ForegroundColor White
Write-Host "  \q" -ForegroundColor White
Write-Host ""

Write-Host "Step 2: Configure .env File" -ForegroundColor Cyan
Write-Host "----------------------------" -ForegroundColor Cyan
Write-Host ""
Write-Host "Edit backend/.env and set:" -ForegroundColor Yellow
Write-Host "  DB_PASSWORD=your_postgres_password" -ForegroundColor White
Write-Host ""

$createEnv = Read-Host "Do you want to create/update .env file? (y/n)"
if ($createEnv -eq 'y' -or $createEnv -eq 'Y') {
    $dbPassword = Read-Host "Enter PostgreSQL password for 'postgres' user" -AsSecureString
    $dbPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPassword))
    
    $envContent = @"
SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development
PORT=5000

# PostgreSQL Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lead_generation
DB_USER=postgres
DB_PASSWORD=$dbPasswordPlain

# JWT
JWT_SECRET_KEY=dev-jwt-secret-key-change-this
JWT_ACCESS_TOKEN_EXPIRES=86400

# Amazon API (Optional)
AMAZON_API_KEY=
AMAZON_SECRET_KEY=
AMAZON_ASSOCIATE_TAG=

# Email Finder (Optional)
HUNTER_API_KEY=

# Gmail (Optional)
GMAIL_USER=
GMAIL_PASSWORD=

# Scheduler
ENABLE_SCHEDULER=true

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Logging
LOG_LEVEL=INFO
"@
    
    $envPath = "backend\.env"
    $envContent | Out-File -FilePath $envPath -Encoding UTF8
    Write-Host "✅ Created backend/.env file" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 3: Test Database Connection" -ForegroundColor Cyan
Write-Host "---------------------------------" -ForegroundColor Cyan
Write-Host ""
Write-Host "After creating the database, run:" -ForegroundColor Yellow
Write-Host "  cd backend" -ForegroundColor White
Write-Host "  python database_setup.py" -ForegroundColor White
Write-Host ""
Write-Host "This will create all tables and admin user!" -ForegroundColor Green
Write-Host ""

