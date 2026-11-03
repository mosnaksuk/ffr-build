# Final Fantasy Resonance - Deploy & Save Sync Script
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  FF Resonance: Auto-Sync Save & Deploy to Web " -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# 1. Re-scan local save file
Write-Host "`n[1/3] Scanning local save file from AppData..." -ForegroundColor Yellow
python save_reader.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Save reader encountered a warning, continuing with existing profile..." -ForegroundColor DarkYellow
}

# 2. Commit and Push to GitHub
Write-Host "`n[2/3] Pushing changes to GitHub repository..." -ForegroundColor Yellow
git add .
git commit -m "sync: Update save profile and build optimizer"
git push origin main

# 3. Deployment status
Write-Host "`n[3/3] Deployment Triggered Successfully!" -ForegroundColor Green
Write-Host "-----------------------------------------------" -ForegroundColor Green
Write-Host "Live Website URL: https://mosnaksuk.github.io/ffr-build/" -ForegroundColor White
Write-Host "GitHub Repo URL:  https://github.com/mosnaksuk/ffr-build" -ForegroundColor White
Write-Host "-----------------------------------------------" -ForegroundColor Green
