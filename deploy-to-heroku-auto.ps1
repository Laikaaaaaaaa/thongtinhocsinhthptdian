# Heroku Deploy Script - thongtinhocsinh.site
# Chạy script này để deploy app lên Heroku

param(
    [string]$AppName = "thongtinhocsinh-app",
    [string]$Region = "ap"
)

Write-Host "=== HEROKU DEPLOYMENT SCRIPT ===" -ForegroundColor Green
Write-Host "App Name: $AppName" -ForegroundColor Yellow
Write-Host "Region: $Region" -ForegroundColor Yellow
Write-Host ""

# Kiểm tra Heroku CLI
Write-Host "Checking Heroku CLI..." -ForegroundColor Cyan
try {
    $herokuVersion = heroku --version
    Write-Host "✓ Heroku CLI found: $herokuVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Heroku CLI not found. Please install it first." -ForegroundColor Red
    Write-Host "Download from: https://devcenter.heroku.com/articles/heroku-cli" -ForegroundColor Yellow
    exit 1
}

# Đăng nhập Heroku
Write-Host "Logging into Heroku..." -ForegroundColor Cyan
try {
    heroku auth:whoami 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Please login to Heroku:" -ForegroundColor Yellow
        heroku login
    } else {
        Write-Host "✓ Already logged in to Heroku" -ForegroundColor Green
    }
} catch {
    Write-Host "Please login to Heroku:" -ForegroundColor Yellow
    heroku login
}

# Tạo ứng dụng Heroku
Write-Host "Creating Heroku app..." -ForegroundColor Cyan
try {
    heroku create $AppName --region $Region
    Write-Host "✓ App created successfully" -ForegroundColor Green
} catch {
    Write-Host "App might already exist or name taken. Continuing..." -ForegroundColor Yellow
}

# Thêm PostgreSQL
Write-Host "Adding PostgreSQL database..." -ForegroundColor Cyan
try {
    heroku addons:create heroku-postgresql:mini -a $AppName
    Write-Host "✓ PostgreSQL added" -ForegroundColor Green
} catch {
    Write-Host "PostgreSQL might already exist. Continuing..." -ForegroundColor Yellow
}

# Cấu hình biến môi trường
Write-Host "Setting environment variables..." -ForegroundColor Cyan
$configs = @{
    "SECRET_KEY" = "thpt-di-an-secret-production-key-2025-$(Get-Random)"
    "FLASK_ENV" = "production"
    "SMTP_SERVER" = "smtp.gmail.com"
    "SMTP_PORT" = "587"
}

foreach ($config in $configs.GetEnumerator()) {
    try {
        heroku config:set "$($config.Key)=$($config.Value)" -a $AppName
        Write-Host "✓ Set $($config.Key)" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to set $($config.Key)" -ForegroundColor Red
    }
}

# Nhắc nhở cấu hình email
Write-Host ""
Write-Host "⚠️  IMPORTANT: Set your email credentials:" -ForegroundColor Yellow
Write-Host "heroku config:set SMTP_EMAIL=your-email@gmail.com -a $AppName" -ForegroundColor White
Write-Host "heroku config:set SMTP_PASSWORD=your-app-password -a $AppName" -ForegroundColor White
Write-Host ""

# Khởi tạo Git và deploy
Write-Host "Initializing Git and deploying..." -ForegroundColor Cyan

# Kiểm tra Git
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
}

# Add Heroku remote
try {
    heroku git:remote -a $AppName
    Write-Host "✓ Heroku remote added" -ForegroundColor Green
} catch {
    Write-Host "Heroku remote might already exist" -ForegroundColor Yellow
}

# Add và commit files
git add .
git commit -m "Deploy to Heroku - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

# Push to Heroku
Write-Host "Pushing to Heroku (this may take a few minutes)..." -ForegroundColor Cyan
try {
    git push heroku main
    Write-Host "✓ Successfully deployed to Heroku!" -ForegroundColor Green
} catch {
    Write-Host "✗ Deployment failed. Check the logs above." -ForegroundColor Red
    exit 1
}

# Thêm custom domain
Write-Host "Adding custom domain..." -ForegroundColor Cyan
try {
    heroku domains:add thongtinhocsinh.site -a $AppName
    heroku domains:add www.thongtinhocsinh.site -a $AppName
    Write-Host "✓ Custom domains added" -ForegroundColor Green
} catch {
    Write-Host "Domain might already exist or need paid plan" -ForegroundColor Yellow
}

# Bật SSL
Write-Host "Enabling SSL..." -ForegroundColor Cyan
try {
    heroku certs:auto:enable -a $AppName
    Write-Host "✓ SSL enabled" -ForegroundColor Green
} catch {
    Write-Host "SSL might need paid plan" -ForegroundColor Yellow
}

# Hiển thị thông tin DNS
Write-Host ""
Write-Host "=== DNS CONFIGURATION NEEDED ===" -ForegroundColor Green
Write-Host "Run this command to get DNS targets:" -ForegroundColor Yellow
Write-Host "heroku domains -a $AppName" -ForegroundColor White
Write-Host ""
Write-Host "Then configure your DNS provider:" -ForegroundColor Yellow
Write-Host "1. A record: @ → (Heroku IP)" -ForegroundColor White
Write-Host "2. CNAME: www → $AppName.herokuapp.com" -ForegroundColor White
Write-Host ""

# Hiển thị kết quả
Write-Host "=== DEPLOYMENT COMPLETE ===" -ForegroundColor Green
Write-Host "App URL: https://$AppName.herokuapp.com" -ForegroundColor Cyan
Write-Host "Custom Domain: https://thongtinhocsinh.site (after DNS setup)" -ForegroundColor Cyan
Write-Host "Admin Panel: https://thongtinhocsinh.site/admin" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Set SMTP email credentials (see commands above)" -ForegroundColor White
Write-Host "2. Configure DNS at your domain provider" -ForegroundColor White
Write-Host "3. Upgrade to Hobby plan for custom domain: heroku ps:scale web=1:hobby -a $AppName" -ForegroundColor White
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "heroku logs --tail -a $AppName  # View logs" -ForegroundColor White
Write-Host "heroku open -a $AppName         # Open app" -ForegroundColor White
Write-Host "heroku restart -a $AppName      # Restart app" -ForegroundColor White
