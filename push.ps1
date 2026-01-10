# 1. Ask you what you did today
$commitMessage = Read-Host -Prompt "What did you study/change in this session?"

# If you just hit Enter without typing, it will use a default message
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Study Session: " + (Get-Date -Format "yyyy-MM-dd HH:mm")
}

# 2. Stage all changes
git add .

# 3. Commit with your custom message
git commit -m "$commitMessage"

# 4. Push to GitHub
write-host "Pushing to GitHub..." -ForegroundColor Cyan
git push origin main

# 5. Success Check
if ($?) {
    write-host "Successfully pushed! Streak updated." -ForegroundColor Green
} else {
    write-host "Push failed. Check the error above." -ForegroundColor Red
}