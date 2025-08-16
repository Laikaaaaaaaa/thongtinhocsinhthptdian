#!/bin/bash

# SSL Setup Script for THPT Di An Management System
# This script helps you obtain SSL certificates from Let's Encrypt

set -e

DOMAIN="thptdian.edu.vn"
EMAIL="admin@thptdian.edu.vn"  # Change this to your actual email
STAGING=0  # Set to 1 for testing

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔒 SSL Setup for THPT Di An Management System${NC}"
echo "=================================================="

# Check if domain and email are provided
if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    echo -e "${RED}❌ Please set DOMAIN and EMAIL variables in this script${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Configuration:${NC}"
echo "Domain: $DOMAIN"
echo "Email: $EMAIL"
echo "Staging: $([ $STAGING -eq 1 ] && echo 'Yes (Testing)' || echo 'No (Production)')"
echo ""

# Create necessary directories
echo -e "${YELLOW}📁 Creating directories...${NC}"
mkdir -p ./certbot/conf
mkdir -p ./certbot/www

# Check if certificates already exist
if [ -d "./certbot/conf/live/$DOMAIN" ]; then
    echo -e "${YELLOW}⚠️  Certificates for $DOMAIN already exist.${NC}"
    read -p "Do you want to renew them? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}✅ Skipping certificate generation${NC}"
        exit 0
    fi
fi

# Start nginx first to handle the challenge
echo -e "${YELLOW}🚀 Starting nginx for certificate challenge...${NC}"
docker-compose up -d nginx

# Wait a moment for nginx to start
sleep 5

# Request certificate
echo -e "${YELLOW}📜 Requesting SSL certificate...${NC}"

if [ $STAGING -eq 1 ]; then
    echo -e "${YELLOW}⚠️  Using Let's Encrypt staging environment (for testing)${NC}"
    docker-compose run --rm certbot certonly \
        --webroot \
        --webroot-path=/var/www/certbot \
        --email $EMAIL \
        --agree-tos \
        --no-eff-email \
        --staging \
        -d $DOMAIN \
        -d www.$DOMAIN
else
    echo -e "${GREEN}🎯 Using Let's Encrypt production environment${NC}"
    docker-compose run --rm certbot certonly \
        --webroot \
        --webroot-path=/var/www/certbot \
        --email $EMAIL \
        --agree-tos \
        --no-eff-email \
        -d $DOMAIN \
        -d www.$DOMAIN
fi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ SSL certificate obtained successfully!${NC}"
    
    # Restart nginx to load the new certificates
    echo -e "${YELLOW}🔄 Restarting nginx with SSL...${NC}"
    docker-compose restart nginx
    
    echo ""
    echo -e "${GREEN}🎉 SSL setup completed successfully!${NC}"
    echo "=================================================="
    echo -e "${GREEN}✅ Your website is now accessible via HTTPS${NC}"
    echo -e "${GREEN}✅ HTTP requests will automatically redirect to HTTPS${NC}"
    echo -e "${GREEN}✅ SSL certificates will auto-renew every 12 hours${NC}"
    echo ""
    echo -e "${YELLOW}📝 Next steps:${NC}"
    echo "1. Update your DNS records to point to this server"
    echo "2. Test your website: https://$DOMAIN"
    echo "3. Check SSL rating: https://www.ssllabs.com/ssltest/"
    echo ""
    echo -e "${YELLOW}🔧 To manage certificates:${NC}"
    echo "- View certificates: docker-compose exec certbot certbot certificates"
    echo "- Renew manually: docker-compose exec certbot certbot renew"
    echo "- Check renewal: docker-compose logs certbot"
    
else
    echo -e "${RED}❌ Failed to obtain SSL certificate${NC}"
    echo ""
    echo -e "${YELLOW}🔍 Common issues:${NC}"
    echo "1. Domain not pointing to this server"
    echo "2. Port 80 not accessible from internet"
    echo "3. Firewall blocking access"
    echo ""
    echo -e "${YELLOW}💡 For testing, you can use staging mode:${NC}"
    echo "Set STAGING=1 in this script and try again"
    exit 1
fi
