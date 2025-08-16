#!/bin/bash
# Quick Heroku Deploy Script

echo "🚀 Starting Heroku deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

APP_NAME="thongtinhocsinh-app"

# Check if logged in to Heroku
echo -e "${BLUE}Checking Heroku login...${NC}"
if ! heroku auth:whoami &>/dev/null; then
    echo -e "${YELLOW}Please login to Heroku:${NC}"
    heroku login
fi

# Create app if doesn't exist
echo -e "${BLUE}Creating/verifying Heroku app...${NC}"
heroku create $APP_NAME --region ap 2>/dev/null || echo -e "${YELLOW}App already exists${NC}"

# Add PostgreSQL if not exists
echo -e "${BLUE}Adding PostgreSQL...${NC}"
heroku addons:create heroku-postgresql:mini -a $APP_NAME 2>/dev/null || echo -e "${YELLOW}PostgreSQL already exists${NC}"

# Set environment variables
echo -e "${BLUE}Setting environment variables...${NC}"
heroku config:set SECRET_KEY="thpt-di-an-secret-production-key-2025-$(date +%s)" -a $APP_NAME
heroku config:set FLASK_ENV="production" -a $APP_NAME

# Git setup and deploy
echo -e "${BLUE}Preparing Git repository...${NC}"
if [ ! -d ".git" ]; then
    git init
fi

heroku git:remote -a $APP_NAME

echo -e "${BLUE}Committing and pushing to Heroku...${NC}"
git add .
git commit -m "Deploy to Heroku - $(date)"
git push heroku main

# Add custom domains
echo -e "${BLUE}Adding custom domains...${NC}"
heroku domains:add thongtinhocsinh.site -a $APP_NAME 2>/dev/null || echo -e "${YELLOW}Domain already added or needs paid plan${NC}"
heroku domains:add www.thongtinhocsinh.site -a $APP_NAME 2>/dev/null || echo -e "${YELLOW}Domain already added or needs paid plan${NC}"

# Enable SSL
echo -e "${BLUE}Enabling SSL...${NC}"
heroku certs:auto:enable -a $APP_NAME 2>/dev/null || echo -e "${YELLOW}SSL needs paid plan${NC}"

echo -e "${GREEN}✅ Deployment complete!${NC}"
echo -e "${BLUE}App URL: ${NC}https://$APP_NAME.herokuapp.com"
echo -e "${BLUE}Custom Domain: ${NC}https://thongtinhocsinh.site ${YELLOW}(after DNS setup)${NC}"

echo -e "${YELLOW}Next steps:${NC}"
echo "1. Set email config: heroku config:set SMTP_EMAIL=your-email@gmail.com -a $APP_NAME"
echo "2. Set email password: heroku config:set SMTP_PASSWORD=your-app-password -a $APP_NAME"
echo "3. Configure DNS at your domain provider"
echo "4. Upgrade to paid plan: heroku ps:scale web=1:hobby -a $APP_NAME"

echo -e "${BLUE}DNS Configuration needed:${NC}"
heroku domains -a $APP_NAME
