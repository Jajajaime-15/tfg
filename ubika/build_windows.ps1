# ============================================================
# Script para generar build Windows de Flet desde proyecto con ruta problematica
# Uso: ejecutar desde la carpeta del proyecto con PowerShell
# ============================================================

$SOURCE = Get-Location
$DEST = "C:\proyectos\tfg_windows"
$FLET = "C:\Python\Python312\Scripts\flet.exe"
$BUILD_ORIGIN = "$DEST\build\windows\x64\runner\Release"
$BUILD_DEST = "$SOURCE\build\windows"

Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "   BUILD WINDOWS - Flet Ubika" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# 1. Copiar fuentes al directorio limpio
Write-Host "[1/4] Copiando proyecto a ruta sin caracteres especiales..." -ForegroundColor Yellow

if (Test-Path $DEST) {
    Remove-Item -Recurse -Force $DEST
}

Copy-Item -Path $SOURCE -Destination $DEST -Recurse
Write-Host "      OK -> $DEST" -ForegroundColor Green

# resolver la ruta real del proyecto copiado
$BUILD_DIR = $DEST
if (Test-Path "$DEST\ubika") {
    $BUILD_DIR = "$DEST\ubika"
}

# 2. Buildear lanzando flet en un proceso hijo con WorkingDirectory limpio
# Set-Location no garantiza que el proceso hijo herede el cwd correcto en Windows
# Start-Process con -WorkingDirectory si lo garantiza
Write-Host ""
Write-Host "[2/4] Ejecutando build Windows (puede tardar 5-15 min)..." -ForegroundColor Yellow
Write-Host ""

$argumentos = "build windows --module-name src/main.py"
$proceso = Start-Process -FilePath $FLET `
    -ArgumentList $argumentos `
    -WorkingDirectory $BUILD_DIR `
    -NoNewWindow `
    -Wait `
    -PassThru

if ($proceso.ExitCode -ne 0) {
    Write-Host ""
    Write-Host "ERROR: El build fallo con codigo $($proceso.ExitCode). Revisa los errores de arriba." -ForegroundColor Red
    exit 1
}

# 3. Comprobar si se genero el ejecutable
$exe = Get-ChildItem -Path $BUILD_ORIGIN -Filter "*.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if ($exe) {
    Write-Host ""
    Write-Host "[3/4] Copiando build al proyecto original..." -ForegroundColor Yellow

    if (-not (Test-Path $BUILD_DEST)) {
        New-Item -ItemType Directory -Path $BUILD_DEST | Out-Null
    }

    Copy-Item -Path "$BUILD_ORIGIN\*" -Destination $BUILD_DEST -Recurse -Force
    Write-Host "      OK -> $BUILD_DEST" -ForegroundColor Green

    Write-Host ""
    Write-Host "[4/4] Volviendo al directorio original..." -ForegroundColor Yellow
    Set-Location $SOURCE

    Write-Host ""
    Write-Host "=======================================" -ForegroundColor Green
    Write-Host "   Build Windows generado correctamente!" -ForegroundColor Green
    Write-Host "   Ubicacion: $BUILD_DEST" -ForegroundColor Green
    Write-Host "=======================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "ERROR: No se encontro el ejecutable. Revisa los errores de arriba." -ForegroundColor Red
    Set-Location $SOURCE
}
