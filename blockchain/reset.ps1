Get-ChildItem -Directory -Filter "data/besu*" | ForEach-Object {
    Write-Host "Processing $($_.FullName)"
    Set-Location $_.FullName

    # Delete all files except 'key'
    Get-ChildItem -File | Where-Object { $_.Name -ne "key" } | Remove-Item -Force

    # Delete all subdirectories
    Get-ChildItem -Directory | Remove-Item -Recurse -Force

    Set-Location ..
}
Write-Host "Done!"
Pause
