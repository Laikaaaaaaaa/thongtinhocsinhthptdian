# Script tự động cấu hình Heroku qua API
# Chạy script này sau khi đã tạo app trên web

$APP_NAME = "csdl-thptdian"
$HEROKU_EMAIL = "abc23072009@gmail.com"

Write-Host "🚀 Auto-configuring Heroku app: $APP_NAME" -ForegroundColor Green

# Cấu hình Environment Variables qua web form data
$configVars = @{
    "SECRET_KEY" = "thpt-di-an-secret-production-key-2025-$(Get-Date -Format 'yyyyMMddHHmmss')"
    "FLASK_ENV" = "production"
    "SMTP_SERVER" = "smtp.gmail.com"
    "SMTP_PORT" = "587"
    "SMTP_EMAIL" = "abc23072009@gmail.com"
}

Write-Host "📝 Environment variables to set:" -ForegroundColor Yellow
foreach ($var in $configVars.GetEnumerator()) {
    Write-Host "   $($var.Key) = $($var.Value)" -ForegroundColor White
}

Write-Host ""
Write-Host "⚠️  MANUAL STEPS NEEDED:" -ForegroundColor Red
Write-Host "1. Go to: https://dashboard.heroku.com/apps/$APP_NAME/settings" -ForegroundColor White
Write-Host "2. Click 'Reveal Config Vars'" -ForegroundColor White
Write-Host "3. Add the variables shown above" -ForegroundColor White
Write-Host "4. Add SMTP_PASSWORD with your Gmail App Password" -ForegroundColor White
Write-Host ""

# Mở các trang cần thiết
Write-Host "🌐 Opening required pages..." -ForegroundColor Cyan

# Mở trang Settings để config vars
Start-Process "https://dashboard.heroku.com/apps/$APP_NAME/settings"
Start-Sleep 2

# Mở trang Resources để add PostgreSQL
Start-Process "https://dashboard.heroku.com/apps/$APP_NAME/resources"
Start-Sleep 2

# Mở trang Deploy để deploy
Start-Process "https://dashboard.heroku.com/apps/$APP_NAME/deploy"
Start-Sleep 2

Write-Host ""
Write-Host "✅ DEPLOYMENT CHECKLIST:" -ForegroundColor Green
Write-Host ""
Write-Host "📋 TAB 1 - DEPLOY:" -ForegroundColor Yellow
Write-Host "   ✅ Scroll to 'Manual deploy'" -ForegroundColor White
Write-Host "   ✅ Select branch 'main'" -ForegroundColor White
Write-Host "   ✅ Click 'Deploy Branch'" -ForegroundColor White
Write-Host ""
Write-Host "📋 TAB 2 - RESOURCES:" -ForegroundColor Yellow  
Write-Host "   ✅ Search 'postgres'" -ForegroundColor White
Write-Host "   ✅ Add 'Heroku Postgres' (free)" -ForegroundColor White
Write-Host "   ✅ Submit order form" -ForegroundColor White
Write-Host ""
Write-Host "📋 TAB 3 - SETTINGS:" -ForegroundColor Yellow
Write-Host "   ✅ Click 'Reveal Config Vars'" -ForegroundColor White
Write-Host "   ✅ Add all environment variables listed above" -ForegroundColor White
Write-Host "   ✅ Add SMTP_PASSWORD = [Gmail App Password]" -ForegroundColor White
Write-Host ""
Write-Host "🔗 After deployment completes:" -ForegroundColor Cyan
Write-Host "   App URL: https://$APP_NAME.herokuapp.com" -ForegroundColor White
Write-Host ""

# Tạo Gmail App Password instructions
Write-Host "📧 Gmail App Password Setup:" -ForegroundColor Magenta
Write-Host "   1. Go to: https://myaccount.google.com/security" -ForegroundColor White
Write-Host "   2. Enable 2-Step Verification if not enabled" -ForegroundColor White
Write-Host "   3. Go to 'App passwords'" -ForegroundColor White
Write-Host "   4. Generate password for 'Mail'" -ForegroundColor White
Write-Host "   5. Use that password in SMTP_PASSWORD config var" -ForegroundColor White

Start-Process "https://myaccount.google.com/security"

Write-Host ""
Write-Host "⏳ Waiting for you to complete the deployment..." -ForegroundColor Yellow
Write-Host "Press any key when deployment is complete to continue with domain setup..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "🌐 Starting domain configuration..." -ForegroundColor Green
