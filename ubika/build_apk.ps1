# ============================================================
# Script para generar APK de Flet desde proyecto con ruta problematica
# Uso: ejecutar desde la carpeta del proyecto con PowerShell
# ============================================================

$SOURCE = Get-Location
$DEST = "C:\proyectos\tfg_apk"
$FLET = "C:\Python\Python312\Scripts\flet.exe"
$APK_ORIGIN = "$DEST\build\apk"
$APK_DEST = "$SOURCE\build\apk"

Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "   BUILD APK - Flet Geolocator Map" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# 1. Copiar fuentes al directorio limpio
Write-Host "[1/4] Copiando proyecto a ruta sin caracteres especiales..." -ForegroundColor Yellow

if (Test-Path $DEST) {
    Remove-Item -Recurse -Force $DEST
}

Copy-Item -Path $SOURCE -Destination $DEST -Recurse
Write-Host "      OK -> $DEST" -ForegroundColor Green

# 2. Entrar al directorio limpio
Set-Location $DEST

# 3. Buildear
Write-Host ""
Write-Host "[2/4] Ejecutando build APK (puede tardar 5-15 min)..." -ForegroundColor Yellow
Write-Host ""

& $FLET build apk --module-name src/main.py --permissions location

# 4. Comprobar si se generó el APK
if (Test-Path "$APK_ORIGIN\app-release.apk") {
    Write-Host ""
    Write-Host "[3/4] Copiando APK al proyecto original..." -ForegroundColor Yellow

    if (-not (Test-Path $APK_DEST)) {
        New-Item -ItemType Directory -Path $APK_DEST | Out-Null
    }

    Copy-Item -Path "$APK_ORIGIN\*" -Destination $APK_DEST -Recurse -Force
    Write-Host "      OK -> $APK_DEST" -ForegroundColor Green

    Write-Host ""
    Write-Host "[4/4] Volviendo al directorio original..." -ForegroundColor Yellow
    Set-Location $SOURCE

    Write-Host ""
    Write-Host "=======================================" -ForegroundColor Green
    Write-Host "   APK generado correctamente!" -ForegroundColor Green
    Write-Host "   Ubicacion: $APK_DEST" -ForegroundColor Green
    Write-Host "=======================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "ERROR: No se encontro el APK. Revisa los errores de arriba." -ForegroundColor Red
    Set-Location $SOURCE
}
