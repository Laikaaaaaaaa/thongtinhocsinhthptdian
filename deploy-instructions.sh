#!/bin/bash
# Script tự động deploy THPT Dĩ An lên Heroku

echo "🚀 Starting THPT Dĩ An Heroku Deployment..."
echo "==========================================="
echo ""

# Step 1: Check current status
echo "📊 Current Git Status:"
git status --short
echo ""

# Step 2: Create GitHub repository URL
echo "🌐 GitHub Repository Setup:"
echo "Repository URL: https://github.com/abc23072009/thpt-di-an"
echo "You need to:"
echo "1. Go to https://github.com/new"
echo "2. Repository name: thpt-di-an"
echo "3. Description: THPT Dĩ An - Student Management System"
echo "4. Set to Public"
echo "5. Click 'Create repository'"
echo ""

# Step 3: Setup remote and push
echo "📤 Setting up Git remote..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/abc23072009/thpt-di-an.git

echo "📤 Pushing to GitHub..."
git branch -M main
echo ""

echo "⚠️  MANUAL STEP REQUIRED:"
echo "After creating the GitHub repository, run:"
echo "git push -u origin main"
echo ""

# Step 4: Heroku setup instructions
echo "🚀 Heroku Deployment Steps:"
echo "============================"
echo ""
echo "1. Go to https://dashboard.heroku.com/apps"
echo "2. Click 'New' → 'Create new app'"
echo "3. App name: thpt-di-an-2025"
echo "4. Region: United States"
echo "5. Click 'Create app'"
echo ""

echo "📊 Connect to GitHub:"
echo "1. In Heroku dashboard → Deploy tab"
echo "2. Deployment method: GitHub"
echo "3. Connect to GitHub and authorize"
echo "4. Search repository: thpt-di-an"
echo "5. Click 'Connect'"
echo ""

echo "💾 Add Database:"
echo "1. Resources tab → Add-ons"
echo "2. Search 'Heroku Postgres'"
echo "3. Select 'Heroku Postgres' Essential ($0/month)"
echo "4. Submit Order Form"
echo ""

echo "⚙️  Environment Variables (Settings → Config Vars):"
echo "SECRET_KEY = thpt-di-an-secret-key-2025-production"
echo "ADMIN_ACCOUNTS = abc23072009@gmail.com:admin123"
echo "SMTP_SERVER = smtp.gmail.com"
echo "SMTP_PORT = 587"
echo "SMTP_EMAIL = abc23072009@gmail.com"
echo "SMTP_PASSWORD = [Your Gmail App Password]"
echo "FLASK_ENV = production"
echo ""

echo "🚀 Deploy:"
echo "1. Deploy tab → Manual deploy"
echo "2. Select branch: main"
echo "3. Click 'Deploy Branch'"
echo "4. Wait for build to complete"
echo ""

echo "✅ Final Result:"
echo "Your app will be available at: https://thpt-di-an-2025.herokuapp.com"
echo "Admin panel: https://thpt-di-an-2025.herokuapp.com/admin"
echo ""

echo "🎯 Features Ready:"
echo "✅ Student management with PostgreSQL"
echo "✅ Excel/CSV/JSON export with auto-cleanup"
echo "✅ Real-time filtering and preview"
echo "✅ Email OTP authentication"
echo "✅ Responsive admin interface"
echo ""

echo "🔧 Need help with Gmail App Password?"
echo "1. Go to https://myaccount.google.com/security"
echo "2. 2-Step Verification → App passwords"
echo "3. Generate password for 'Mail'"
echo "4. Use this password for SMTP_PASSWORD"
echo ""

echo "📱 All done! Ready for Heroku deployment!"
