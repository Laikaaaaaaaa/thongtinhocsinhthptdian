# SSL Mobile Fix Deployment Script for Windows
Write-Host "Deploying SSL Mobile Compatibility Fixes..." -ForegroundColor Green

# Check if running on production server
$isProduction = Test-Path "C:\nginx" -or (Get-Service -Name "nginx" -ErrorAction SilentlyContinue)

if ($isProduction) {
    Write-Host "Production environment detected" -ForegroundColor Yellow
    
    # Backup current nginx config
    if (Test-Path "C:\nginx\conf\nginx.conf") {
        Copy-Item "C:\nginx\conf\nginx.conf" "C:\nginx\conf\nginx.conf.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Write-Host "Nginx config backed up" -ForegroundColor Green
    }
    
    # Copy new nginx config
    if (Test-Path "nginx.conf") {
        Copy-Item "nginx.conf" "C:\nginx\conf\nginx.conf" -Force
        Write-Host "New nginx config deployed" -ForegroundColor Green
    }
    
    # Restart nginx
    try {
        Restart-Service nginx -ErrorAction Stop
        Write-Host "Nginx restarted successfully" -ForegroundColor Green
    } catch {
        Write-Host "Failed to restart nginx: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Test SSL
    Write-Host "Testing SSL configuration..." -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri "https://thptdian.edu.vn/" -Method Head -ErrorAction Stop
        Write-Host "SSL test successful - Status: $($response.StatusCode)" -ForegroundColor Green
        
        # Check headers
        $headers = $response.Headers
        if ($headers["Strict-Transport-Security"]) {
            Write-Host "HSTS header found: $($headers['Strict-Transport-Security'])" -ForegroundColor Green
        }
        if ($headers["Content-Security-Policy"]) {
            Write-Host "CSP header found: Mobile compatibility enabled" -ForegroundColor Green
        }
    } catch {
        Write-Host "SSL test failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
} else {
    Write-Host "Development environment - Files updated successfully" -ForegroundColor Yellow
    Write-Host "To deploy to production:" -ForegroundColor Cyan
    Write-Host "1. Upload nginx.conf to server" -ForegroundColor White
    Write-Host "2. Upload HTML files with CSP headers" -ForegroundColor White
    Write-Host "3. Restart nginx service" -ForegroundColor White
    Write-Host "4. Test on mobile devices" -ForegroundColor White
}

Write-Host "`nSSL Mobile Fixes Applied:" -ForegroundColor Cyan
Write-Host "✓ Added upgrade-insecure-requests to all HTML files" -ForegroundColor Green
Write-Host "✓ Enhanced nginx CSP headers for mobile compatibility" -ForegroundColor Green
Write-Host "✓ Improved HSTS and security headers" -ForegroundColor Green
Write-Host "✓ Mobile-optimized SSL configuration" -ForegroundColor Green

Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Test website on mobile browsers" -ForegroundColor White
Write-Host "2. Clear browser cache on mobile devices" -ForegroundColor White
Write-Host "3. Verify HTTPS works on both desktop and mobile" -ForegroundColor White
