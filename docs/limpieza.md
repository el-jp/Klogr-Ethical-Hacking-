# Limpieza del laboratorio

## Windows (PowerShell como administrador)

```powershell
taskkill /F /IM MetasploitFramework-latest.exe 2>$null
taskkill /F /IM msfconsole.exe 2>$null
taskkill /F /IM victim.exe 2>$null

schtasks /delete /tn WindowsUpdateCheck /f

Remove-Item "$env:APPDATA\msfconsole.exe" -ErrorAction SilentlyContinue
Remove-Item "$env:APPDATA\SystemUpdate.exe" -ErrorAction SilentlyContinue
Remove-Item "$env:APPDATA\Material_Semana10_Metasploit.exe" -ErrorAction SilentlyContinue

Remove-Item "$env:TEMP\dat.txt" -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\dat.txt.old" -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\payload_err.txt" -ErrorAction SilentlyContinue

Get-ChildItem "$env:TEMP" -Directory -Filter "_MEI*" | ForEach-Object {
    Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
}

reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v SystemUpdate /f 2>$null
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v MaterialSemana10 /f 2>$null
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v WindowsUpdateCheck /f 2>$null

Remove-MpPreference -ExclusionPath "$env:APPDATA" -ErrorAction SilentlyContinue
Remove-MpPreference -ExclusionPath "$env:TEMP" -ErrorAction SilentlyContinue
Remove-MpPreference -ExclusionProcess "msfconsole.exe" -ErrorAction SilentlyContinue

Remove-Item "$env:USERPROFILE\Desktop\victim.exe" -ErrorAction SilentlyContinue
Remove-Item "$env:USERPROFILE\Desktop\victim.spec" -ErrorAction SilentlyContinue
Remove-Item "$env:USERPROFILE\Desktop\build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:USERPROFILE\Desktop\dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:USERPROFILE\Desktop\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
