#!/bin/bash
# Test SSL mobile compatibility

echo "Testing SSL configuration for mobile compatibility..."

DOMAIN="thptdian.edu.vn"

echo "1. Testing SSL certificate validity..."
openssl s_client -connect $DOMAIN:443 -servername $DOMAIN < /dev/null 2>/dev/null | openssl x509 -noout -dates

echo -e "\n2. Testing SSL Labs API for mobile compatibility..."
curl -s "https://api.ssllabs.com/api/v3/analyze?host=$DOMAIN" | grep -E "(grade|hasWarnings|isExceptional)"

echo -e "\n3. Testing specific mobile user agents..."
# iPhone
echo "iPhone Safari:"
curl -I -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1" https://$DOMAIN/ 2>/dev/null | head -1

# Android Chrome
echo "Android Chrome:"
curl -I -H "User-Agent: Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36" https://$DOMAIN/ 2>/dev/null | head -1

echo -e "\n4. Testing for mixed content..."
curl -s https://$DOMAIN/ | grep -i "http://" && echo "WARNING: Found HTTP links!" || echo "OK: No HTTP links found"

echo -e "\n5. Testing HSTS header..."
curl -I https://$DOMAIN/ 2>/dev/null | grep -i "strict-transport-security"

echo -e "\n6. Testing CSP header..."
curl -I https://$DOMAIN/ 2>/dev/null | grep -i "content-security-policy"

echo -e "\nSSL Mobile Test Complete!"
