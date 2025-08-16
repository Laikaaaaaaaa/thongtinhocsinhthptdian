@echo off
echo 🔒 SSL Setup Script for THPT Di An Management System
echo ===================================================

REM Kiểm tra Docker
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Docker không được cài đặt hoặc không có trong PATH
    echo 📋 Vui lòng cài đặt Docker Desktop: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Kiểm tra Docker Compose
where docker-compose >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Docker Compose không được cài đặt
    echo 📋 Vui lòng cài đặt Docker Compose
    pause
    exit /b 1
)

echo ✅ Docker và Docker Compose đã sẵn sàng
echo.

echo 📋 Thiết lập SSL/HTTPS cho THPT Dĩ An:
echo.
echo 🔧 Bước 1: Cấu hình domain
echo    - Sửa file .env.production với domain thực của bạn
echo    - Đảm bảo DNS records point về server này
echo.
echo 🔧 Bước 2: Khởi động services
echo    - Tạo containers và network
echo    - Start nginx, web app, redis, postgres
echo.
echo 🔒 Bước 3: Cấp SSL certificate từ Let's Encrypt
echo    - Tự động request và setup SSL certificates
echo    - Configure auto-renewal
echo.

set /p proceed="Bạn có muốn tiếp tục? (y/n): "
if /i not "%proceed%"=="y" (
    echo ❌ Hủy bỏ thiết lập
    pause
    exit /b 0
)

echo.
echo 🚀 Đang khởi động Docker services...

REM Copy environment file
if not exist .env (
    copy .env.production .env
    echo ✅ Đã copy .env.production thành .env
)

REM Tạo directories cần thiết
mkdir certbot\conf 2>nul
mkdir certbot\www 2>nul
echo ✅ Đã tạo directories cho SSL certificates

REM Build và start services
docker-compose up -d --build

if %errorlevel% neq 0 (
    echo ❌ Lỗi khi khởi động Docker services
    pause
    exit /b 1
)

echo ✅ Docker services đã khởi động thành công!
echo.

echo 🔒 Bây giờ bạn cần chạy lệnh để lấy SSL certificate:
echo.
echo    docker-compose exec nginx /bin/sh
echo    # Sau đó trong container nginx, chạy:
echo    # certbot certonly --webroot --webroot-path=/var/www/certbot ^
echo    #   --email admin@yourdomain.com --agree-tos --no-eff-email ^
echo    #   -d yourdomain.com -d www.yourdomain.com
echo.
echo 🌐 Kiểm tra services:
echo    - Web app: http://localhost:5000
echo    - Admin: http://localhost:5000/admin
echo    - Nginx: http://localhost:80
echo.
echo 📋 Logs:
echo    docker-compose logs -f web
echo    docker-compose logs -f nginx
echo.

pause
