# ============================================================
# Script para depurar app Flet en Android desde proyecto con ruta problematica
# Uso: ejecutar desde la carpeta del proyecto con PowerShell
# ============================================================

$SOURCE = Get-Location
$DEST = "C:\proyectos\prueba"
$FLET = "C:\Python\Python312\Scripts\flet.exe"

Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "   DEBUG ANDROID - Flet Geolocator Map" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# 1. Listar dispositivos disponibles
Write-Host "[1/3] Buscando dispositivos Android..." -ForegroundColor Yellow
& $FLET devices
Write-Host ""

# 2. Pedir device ID
$DEVICE_ID = Read-Host "Introduce el device ID (o pulsa Enter para usar el primero disponible)"

# 3. Copiar proyecto a ruta limpia
Write-Host ""
Write-Host "[2/3] Copiando proyecto a ruta sin caracteres especiales..." -ForegroundColor Yellow

if (Test-Path $DEST) {
    Remove-Item -Recurse -Force $DEST
}

Copy-Item -Path $SOURCE -Destination $DEST -Recurse
Write-Host "      OK -> $DEST" -ForegroundColor Green

# 4. Entrar al directorio limpio y lanzar debug
Set-Location $DEST

$env:PUB_CACHE = "C:\DartCache"
$env:ANDROID_HOME = "C:\Android\Sdk"
$env:ANDROID_SDK_ROOT = "C:\Android\Sdk"

Write-Host ""
Write-Host "[3/3] Lanzando debug en Android..." -ForegroundColor Yellow
Write-Host "      Pulsa 'r' en cualquier momento para hot reload" -ForegroundColor Gray
Write-Host "      Pulsa 'q' para salir" -ForegroundColor Gray
Write-Host ""

if ($DEVICE_ID -eq "") {
    & $FLET debug android 
} else {
    & $FLET debug android --device-id $DEVICE_ID 
}

# Volver al directorio original al salir
Set-Location $SOURCE
Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "   Debug finalizado" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
