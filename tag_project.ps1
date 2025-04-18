# Prompt for tag name and message
$tagName = Read-Host "Enter tag name (e.g. before-chapter-16-enhancement)"
$tagMessage = Read-Host "Enter tag message (e.g. Tag before starting enhancement)"

Write-Host ""
Write-Host "📝 Creating Git tag: $tagName" -ForegroundColor Cyan

# Add all changes and make a commit
git add .

try {
    git commit -m "Checkpoint before tag $tagName" | Out-Null
} catch {
    Write-Host "⚠️ No changes to commit (or commit failed)" -ForegroundColor Yellow
}

# Create annotated tag
git tag -a $tagName -m "$tagMessage"
git push origin $tagName

Write-Host ""
Write-Host "✅ Git tag '$tagName' created and pushed." -ForegroundColor Green
