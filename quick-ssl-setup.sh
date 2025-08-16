#!/bin/bash

# Quick SSL Setup Script
# Chạy sau khi đã có domain và DNS setup

set -e

echo "🔒 Quick SSL Setup for THPT Dĩ An"
echo "=================================="

# Prompt for domain
read -p "Nhập domain của bạn (ví dụ: thptdian.edu.vn): " DOMAIN
read -p "Nhập email admin (ví dụ: admin@thptdian.edu.vn): " EMAIL

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    echo "❌ Domain và email không được để trống"
    exit 1
fi

echo "📋 Configuration:"
echo "Domain: $DOMAIN"
echo "Email: $EMAIL"
echo ""

# Update nginx config with actual domain
sed -i "s/thptdian.edu.vn/$DOMAIN/g" nginx.conf
sed -i "s/www.thptdian.edu.vn/www.$DOMAIN/g" nginx.conf

# Update environment file
sed -i "s/DOMAIN=thptdian.edu.vn/DOMAIN=$DOMAIN/g" .env.production
sed -i "s/SSL_EMAIL=admin@thptdian.edu.vn/SSL_EMAIL=$EMAIL/g" .env.production

# Copy to .env if not exists
if [ ! -f .env ]; then
    cp .env.production .env
    echo "✅ Created .env from .env.production"
fi

# Create directories
mkdir -p ./certbot/conf ./certbot/www

echo "🚀 Starting services..."
docker-compose up -d --build

echo "🔒 Requesting SSL certificate..."
sleep 10  # Wait for services to start

docker-compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN \
    -d www.$DOMAIN

if [ $? -eq 0 ]; then
    echo "✅ SSL certificate obtained successfully!"
    echo "🔄 Restarting nginx..."
    docker-compose restart nginx
    
    echo ""
    echo "🎉 Setup completed successfully!"
    echo "=================================="
    echo "✅ Your website is now accessible via HTTPS"
    echo "🌐 URL: https://$DOMAIN"
    echo "👨‍💼 Admin: https://$DOMAIN/admin"
    echo "🔒 SSL Grade: Check at https://www.ssllabs.com/ssltest/"
    echo ""
    echo "📊 Monitor services:"
    echo "docker-compose logs -f"
    echo "docker-compose ps"
else
    echo "❌ SSL certificate request failed"
    echo "Please check domain DNS and try again"
    exit 1
fi
