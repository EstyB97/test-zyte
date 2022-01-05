Write-Host Scraping Development Environment Installer v0.1
Start-Sleep -Seconds 1
Write-Host Installing - Press Y to prompts blindly please...

Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy RemoteSigned -Force

$dlpath = (New-Object -ComObject Shell.Application).NameSpace('shell:Downloads').Self.Path
$outpath = Join-Path -Path $dlpath -ChildPath "\anaconda.exe"
Invoke-WebRequest -Uri https://repo.anaconda.com/archive/Anaconda2-5.3.1-Windows-x86_64.exe -OutFile "$outpath"

cd $dlpath

start /wait "" anaconda.exe /InstallationType=JustMe /RegisterPython=0 /S /D=%UserProfile%\Anaconda2
msiexec.exe /package PowerShell-7.1.5-win-x64.msi /quiet ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1 ENABLE_PSREMOTING=1 REGISTER_MANIFEST=1

conda update -n base -c defaults conda

conda create --name Scrapy python=2.7

conda create --name shub python=3

conda activate Scrapy

conda install -c conda-forge scrapy

conda deactivate

conda activate shub

pip install shub

conda deactivate

conda init powershell

Start-Sleep -Seconds 20

conda -v

Install-Module posh-git -Scope CurrentUser -Force

python -m pip install --upgrade pip