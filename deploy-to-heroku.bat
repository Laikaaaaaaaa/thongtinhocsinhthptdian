@echo off
echo 🚀 Deploying THPT Di An to GitHub and Heroku...
echo.

echo 📁 Current directory:
cd /d "c:\Users\abc23\Desktop\CSDL-THPT DĨ AN"
echo %cd%
echo.

echo 📝 Adding all files to git...
git add .
echo.

echo 💬 Committing changes...
git commit -m "Ready for Heroku deployment - PostgreSQL support added"
echo.

echo 🌐 Setting up GitHub remote (if not exists)...
git remote remove origin 2>nul
git remote add origin https://github.com/abc23072009/thpt-di-an.git
echo.

echo 📤 Pushing to GitHub...
git branch -M main
git push -u origin main --force
echo.

echo ✅ Code pushed to GitHub successfully!
echo.
echo 🎯 Next steps:
echo 1. Go to https://dashboard.heroku.com/
echo 2. Create new app: thpt-di-an-2025
echo 3. Connect to GitHub repository: thpt-di-an
echo 4. Add Heroku Postgres add-on
echo 5. Configure environment variables
echo 6. Deploy from GitHub
echo.
echo 📖 See HEROKU-DEPLOY-GUIDE.md for detailed instructions
echo.
pause
