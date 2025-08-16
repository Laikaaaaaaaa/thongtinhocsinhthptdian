# Hướng dẫn Deploy lên Heroku với Custom Domain

## Bước 1: Cài đặt Heroku CLI

### Tải và cài đặt Heroku CLI:
- Truy cập: https://devcenter.heroku.com/articles/heroku-cli
- Tải về và cài đặt cho Windows

### Hoặc sử dụng PowerShell (với Chocolatey):
```powershell
# Cài đặt Chocolatey nếu chưa có
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Cài đặt Heroku CLI
choco install heroku-cli
```

## Bước 2: Đăng nhập và tạo ứng dụng Heroku

```powershell
# Đăng nhập vào Heroku
heroku login

# Tạo ứng dụng mới (thay ten-app-cua-ban bằng tên bạn muốn)
heroku create thongtinhocsinh-app

# Hoặc tạo với region Singapore (gần Việt Nam hơn)
heroku create thongtinhocsinh-app --region ap
```

## Bước 3: Cấu hình môi trường

```powershell
# Set biến môi trường cho production
heroku config:set SECRET_KEY="thpt-di-an-secret-production-key-2025"
heroku config:set FLASK_ENV="production"

# Cấu hình email (thay thông tin thật)
heroku config:set SMTP_SERVER="smtp.gmail.com"
heroku config:set SMTP_PORT="587"
heroku config:set SMTP_EMAIL="your-email@gmail.com"
heroku config:set SMTP_PASSWORD="your-app-password"

# Thêm database PostgreSQL
heroku addons:create heroku-postgresql:mini
```

## Bước 4: Deploy code

```powershell
# Khởi tạo git repository (nếu chưa có)
git init

# Thêm tất cả files
git add .

# Commit code
git commit -m "Initial deployment to Heroku"

# Thêm Heroku remote
heroku git:remote -a thongtinhocsinh-app

# Push code lên Heroku
git push heroku main
```

## Bước 5: Cấu hình Custom Domain (thongtinhocsinh.site)

### 5.1. Thêm domain vào Heroku
```powershell
# Thêm domain
heroku domains:add thongtinhocsinh.site
heroku domains:add www.thongtinhocsinh.site

# Xem thông tin DNS cần cấu hình
heroku domains
```

### 5.2. Cấu hình DNS tại nhà cung cấp domain

Sau khi chạy `heroku domains`, bạn sẽ nhận được DNS target. Cấu hình tại nhà cung cấp domain:

**A Records:**
- `@` (root domain) → IP của Heroku hoặc dùng CNAME flattening
- `www` → CNAME target từ Heroku

**CNAME Records:**
- `www.thongtinhocsinh.site` → `your-app-name.herokuapp.com`

### 5.3. Bật SSL (bắt buộc cho custom domain)
```powershell
# Bật Automated Certificate Management (ACM)
heroku certs:auto:enable

# Kiểm tra trạng thái SSL
heroku certs:auto
```

## Bước 6: Kiểm tra và monitoring

```powershell
# Xem logs
heroku logs --tail

# Restart app nếu cần
heroku restart

# Mở app
heroku open

# Kiểm tra status
heroku ps
```

## Bước 7: Cập nhật sau này

```powershell
# Khi có thay đổi code
git add .
git commit -m "Update description"
git push heroku main

# Heroku sẽ tự động deploy lại
```

## Troubleshooting

### Lỗi thường gặp:

1. **Database connection error:**
   ```powershell
   heroku config:get DATABASE_URL
   # Kiểm tra xem có PostgreSQL addon chưa
   heroku addons
   ```

2. **SSL certificate chưa ready:**
   - Đợi 10-30 phút sau khi cấu hình DNS
   - Kiểm tra: `heroku certs:auto`

3. **App crash:**
   ```powershell
   heroku logs --tail
   # Xem chi tiết lỗi
   ```

4. **Port binding error:**
   - Đảm bảo app.py sử dụng: `port = int(os.environ.get('PORT', 5000))`

## Lưu ý quan trọng:

1. **Backup database định kỳ:**
   ```powershell
   heroku pg:backups:capture
   heroku pg:backups:download
   ```

2. **Monitor usage:**
   - Free tier Heroku có giới hạn 550 giờ/tháng
   - App sẽ sleep sau 30 phút không hoạt động

3. **Custom domain cần plan trả phí:**
   - Upgrade lên Hobby plan ($7/tháng) để sử dụng custom domain
   ```powershell
   heroku ps:scale web=1:hobby
   ```

## Kết quả cuối cùng:
- App sẽ chạy tại: `https://thongtinhocsinh.site`
- Admin panel: `https://thongtinhocsinh.site/admin`
- SSL được bật tự động
- Database PostgreSQL trên cloud
