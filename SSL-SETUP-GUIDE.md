# Hướng dẫn triển khai HTTPS/SSL với Let's Encrypt cho THPT Dĩ An

## 🔒 Tổng quan
Hệ thống đã được cấu hình để hỗ trợ HTTPS/SSL tự động với Let's Encrypt, bao gồm:
- Nginx reverse proxy với SSL termination
- Tự động redirect HTTP → HTTPS
- Security headers tăng cường
- Rate limiting cho các endpoint quan trọng
- Auto-renewal SSL certificates

## 📋 Chuẩn bị

### 1. Domain và DNS
```bash
# Đảm bảo domain của bạn point về server
# Ví dụ:
# thptdian.edu.vn     A    YOUR_SERVER_IP
# www.thptdian.edu.vn A    YOUR_SERVER_IP
```

### 2. Firewall
```bash
# Mở ports cần thiết
ufw allow 80    # HTTP (cho Let's Encrypt challenge)
ufw allow 443   # HTTPS
ufw allow 22    # SSH (nếu cần)
```

## 🚀 Triển khai

### Bước 1: Cấu hình Environment
```bash
# 1. Sửa file .env.production với thông tin thực:
DOMAIN=yourdomain.com
SSL_EMAIL=admin@yourdomain.com
SECRET_KEY=your-super-secret-key-here

# 2. Copy sang .env để sử dụng:
cp .env.production .env
```

### Bước 2: Khởi động Services (Linux/Mac)
```bash
# Chạy script tự động:
chmod +x setup-ssl.sh
./setup-ssl.sh

# Hoặc thủ công:
mkdir -p ./certbot/conf ./certbot/www
docker-compose up -d --build
```

### Bước 3: Khởi động Services (Windows)
```cmd
# Chạy file bat:
setup-ssl.bat

# Hoặc thủ công:
mkdir certbot\conf certbot\www
docker-compose up -d --build
```

### Bước 4: Lấy SSL Certificate
```bash
# Option A: Tự động (Linux/Mac)
./setup-ssl.sh

# Option B: Thủ công
docker-compose run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email admin@yourdomain.com \
  --agree-tos \
  --no-eff-email \
  -d yourdomain.com \
  -d www.yourdomain.com
```

### Bước 5: Restart với SSL
```bash
# Restart nginx để load certificates
docker-compose restart nginx

# Kiểm tra logs
docker-compose logs nginx
```

## 🔧 Cấu hình đã bao gồm

### Security Headers
- `Strict-Transport-Security`: HSTS protection
- `X-Frame-Options`: Clickjacking protection
- `X-Content-Type-Options`: MIME sniffing protection
- `X-XSS-Protection`: XSS protection
- `Referrer-Policy`: Referrer information control

### Rate Limiting
- Login endpoints: 5 requests/minute
- API endpoints: 30 requests/minute
- Static files: Unlimited với caching

### SSL Configuration
- TLS 1.2 và 1.3 only
- Modern cipher suites
- OCSP stapling
- Perfect Forward Secrecy

## 📊 Kiểm tra và Monitoring

### Kiểm tra SSL
```bash
# SSL Labs test:
# https://www.ssllabs.com/ssltest/analyze.html?d=yourdomain.com

# Local test:
curl -I https://yourdomain.com
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
```

### Logs
```bash
# Web application logs
docker-compose logs -f web

# Nginx logs
docker-compose logs -f nginx

# SSL renewal logs
docker-compose logs certbot
```

### Health Check
```bash
# Application health
curl https://yourdomain.com/health

# SSL expiry check
curl https://yourdomain.com -v 2>&1 | grep "expire"
```

## 🔄 Maintenance

### Auto-renewal
SSL certificates sẽ tự động renew mỗi 12 giờ thông qua certbot container.

### Manual renewal
```bash
# Force renewal test
docker-compose exec certbot certbot renew --dry-run

# Force renewal
docker-compose exec certbot certbot renew --force-renewal
docker-compose restart nginx
```

### Backup certificates
```bash
# Backup SSL certificates
tar -czf ssl-backup-$(date +%Y%m%d).tar.gz ./certbot/conf/
```

## 🚨 Troubleshooting

### Common Issues

1. **Domain không accessible**
   ```bash
   # Kiểm tra DNS
   nslookup yourdomain.com
   
   # Kiểm tra firewall
   ufw status
   ```

2. **Let's Encrypt rate limit**
   ```bash
   # Sử dụng staging environment để test
   # Thêm flag --staging vào lệnh certbot
   ```

3. **Permission errors**
   ```bash
   # Fix permissions
   sudo chown -R $USER:$USER ./certbot/
   ```

### Debug Commands
```bash
# Container status
docker-compose ps

# Network connectivity
docker-compose exec nginx ping web
docker-compose exec web ping google.com

# SSL certificate info
docker-compose exec certbot certbot certificates
```

## 📈 Performance Tips

1. **Enable HTTP/2**: Đã được enable trong nginx config
2. **Gzip compression**: Đã được cấu hình cho static files
3. **Browser caching**: Static files cache 1 year
4. **Connection keep-alive**: Được tối ưu trong nginx

## 🔐 Security Best Practices

1. **Regular updates**:
   ```bash
   docker-compose pull
   docker-compose up -d --build
   ```

2. **Monitor logs**:
   ```bash
   # Setup log rotation
   docker-compose logs --tail=100 nginx | grep "error\|403\|404\|500"
   ```

3. **Backup regularly**:
   ```bash
   # Database backup
   docker-compose exec web python -c "import sqlite3; conn=sqlite3.connect('students.db'); conn.backup(sqlite3.connect('backup.db'))"
   ```

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra logs: `docker-compose logs`
2. Kiểm tra DNS và firewall
3. Test SSL với staging environment trước
4. Đảm bảo ports 80/443 available

Hệ thống đã sẵn sàng cho production với security và performance tối ưu! 🚀
