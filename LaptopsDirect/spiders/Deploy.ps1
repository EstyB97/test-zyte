Clear-Host

Write-Host Deploy Spiders Script 0.1

Start-Sleep -Seconds 3

Write-Host Change to Local Directory

Set-Location C:\Users\BrandonEsteves\Documents\GitHub\test-zyte

Write-Host Activate Anaconda Environment

conda activate shub

Write-Host Zyte Deploy Using shub Package Version: | shub version

Write-Host Deploying Latest Files to Zyte...

shub deploy 354427

Write-Host ...

Start-Sleep -Seconds 2

Write-Host Deployment Script Complete

conda deactivate

exit