#!/bin/bash
# Force SSL reload and mobile compatibility fix

echo "Forcing SSL reload for mobile compatibility..."

# Stop containers
docker-compose down

# Clear SSL cache and reload certificates
docker run --rm -v letsencrypt_certs:/etc/letsencrypt \
    -v letsencrypt_www:/var/www/certbot \
    certbot/certbot renew --force-renewal

# Rebuild nginx with new config
docker-compose build nginx

# Start with fresh SSL
docker-compose up -d

echo "Waiting for services to start..."
sleep 10

# Test SSL
echo "Testing SSL after reload..."
curl -I https://thptdian.edu.vn/ 2>/dev/null | head -5

echo "SSL reload complete! Test on mobile device now."
