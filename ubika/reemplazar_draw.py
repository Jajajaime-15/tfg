from PIL import Image
from pathlib import Path

ICONO = Path("src/assets/android/res/icono_ubika.png")
BASE  = Path("build/flutter/android/app/src/main/res")

CARPETAS = {
    "mipmap-mdpi":    48,
    "mipmap-hdpi":    72,
    "mipmap-xhdpi":   96,
    "mipmap-xxhdpi":  144,
    "mipmap-xxxhdpi": 192,
    "drawable-mdpi":    48,
    "drawable-hdpi":    72,
    "drawable-xhdpi":   96,
    "drawable-xxhdpi":  144,
    "drawable-xxxhdpi": 192,
}

if not ICONO.exists():
    print(f"No se encontro el icono en: {ICONO}")
    exit(1)

img = Image.open(ICONO).convert("RGBA")
print(f"Icono cargado: {img.size}")

for carpeta, tam in CARPETAS.items():
    d = BASE / carpeta
    d.mkdir(parents=True, exist_ok=True)
    r = img.resize((tam, tam), Image.LANCZOS)
    r.save(d / "ic_launcher.png")
    r.save(d / "ic_launcher_foreground.png")
    print(f"  {carpeta} -> {tam}x{tam} OK")

print("Listo! Ahora ejecuta: flet build apk")