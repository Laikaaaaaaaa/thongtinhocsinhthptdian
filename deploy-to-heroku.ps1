# PowerShell script để deploy THPT Dĩ An lên Heroku
Write-Host "🚀 Deploying THPT Dĩ An to GitHub and Heroku..." -ForegroundColor Green
Write-Host ""

# Change to project directory
Set-Location "c:\Users\abc23\Desktop\CSDL-THPT DĨ AN"
Write-Host "📁 Working directory: $(Get-Location)" -ForegroundColor Yellow
Write-Host ""

# Add and commit all changes
Write-Host "📝 Adding all files to git..." -ForegroundColor Yellow
git add .

Write-Host "💬 Committing changes..." -ForegroundColor Yellow
git commit -m "Ready for Heroku deployment - Full PostgreSQL support"

# Setup GitHub remote
Write-Host "🌐 Setting up GitHub remote..." -ForegroundColor Yellow
try {
    git remote remove origin 2>$null
} catch {}
git remote add origin https://github.com/abc23072009/thpt-di-an.git

# Push to GitHub
Write-Host "📤 Pushing to GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main --force

Write-Host ""
Write-Host "✅ Code successfully pushed to GitHub!" -ForegroundColor Green
Write-Host ""

Write-Host "🎯 Next steps for Heroku deployment:" -ForegroundColor Cyan
Write-Host "1. Go to https://dashboard.heroku.com/" -ForegroundColor White
Write-Host "2. Click 'New' → 'Create new app'" -ForegroundColor White
Write-Host "3. App name: thpt-di-an-2025" -ForegroundColor White
Write-Host "4. Connect to GitHub repository: thpt-di-an" -ForegroundColor White
Write-Host "5. Add Heroku Postgres add-on (Essential plan - FREE)" -ForegroundColor White
Write-Host "6. Configure environment variables in Settings → Config Vars:" -ForegroundColor White
Write-Host "   - SECRET_KEY: thpt-di-an-secret-key-2025-production" -ForegroundColor Gray
Write-Host "   - ADMIN_ACCOUNTS: abc23072009@gmail.com:admin123" -ForegroundColor Gray
Write-Host "   - SMTP_EMAIL: abc23072009@gmail.com" -ForegroundColor Gray
Write-Host "   - SMTP_PASSWORD: [Your Gmail App Password]" -ForegroundColor Gray
Write-Host "7. Deploy from GitHub main branch" -ForegroundColor White
Write-Host ""

Write-Host "📖 See HEROKU-DEPLOY-GUIDE.md for detailed step-by-step instructions" -ForegroundColor Magenta
Write-Host ""

Write-Host "🌐 After deployment, your app will be available at:" -ForegroundColor Green
Write-Host "https://thpt-di-an-2025.herokuapp.com/" -ForegroundColor Blue
Write-Host ""

Read-Host "Press Enter to continue..."
