#!/bin/bash

echo "🔧 Fixing SSL issues for mobile devices"
echo "======================================"

# Force HTTPS for all resources
echo "🔒 Forcing HTTPS for all resources..."

# Add meta tag to force HTTPS
find . -name "*.html" -type f -exec grep -L "Content-Security-Policy" {} \; | while read file; do
    echo "Adding CSP header to $file"
    sed -i '/<head>/a\    <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">' "$file"
done

# Update nginx config for mobile SSL
echo "📱 Updating nginx config for mobile SSL..."
cat > nginx-mobile-ssl.conf << 'EOF'
# Additional mobile SSL configuration
# Add this to your existing nginx.conf

# Force HTTPS and fix mobile SSL issues
add_header Content-Security-Policy "upgrade-insecure-requests" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

# Fix for mobile browsers
location / {
    # Ensure all redirects use HTTPS
    proxy_redirect http:// https://;
    
    # Set proper headers for mobile
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_set_header X-Forwarded-Ssl on;
    
    # Mobile specific headers
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Server $host;
    
    proxy_pass http://flask_app;
}
EOF

echo "✅ Mobile SSL fixes applied!"
echo ""
echo "📋 Next steps:"
echo "1. Restart nginx: docker-compose restart nginx"
echo "2. Clear mobile browser cache"
echo "3. Test on mobile: https://yourdomain.com"
echo ""
echo "🔍 To diagnose SSL issues:"
echo "- Check: https://www.ssllabs.com/ssltest/"
echo "- Mobile test: https://www.giftofspeed.com/ssl-checker/"
