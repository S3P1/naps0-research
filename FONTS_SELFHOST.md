# Fuentes autoalojadas — naps0.com

La landing usa fuentes **autoalojadas** (`@font-face` → `./fonts/*.woff2`), **sin Google Fonts CDN**.
Motivo: privacidad — al no cargar desde `fonts.gstatic.com`, el navegador del visitante no
filtra su IP/peticion a Google. Coherente con el discurso "sin rastreo".

Si algun `.woff2` faltara, el texto degrada al stack de sistema (sigue siendo privacy-clean):
- Inter → `ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif`
- DM Mono → `ui-monospace, 'SFMono-Regular', Menlo, Consolas, monospace`

## Ficheros en `./fonts/` (4)

| Fichero | Fuente | Licencia | Origen |
|---|---|---|---|
| `inter-var.woff2` | Inter (variable 100–900) | OFL 1.1 | Convertido del TTF del propio repo de la app (`app/assets/fonts/Inter-VariableFont_opsz,wght.ttf`) con `fontTools` (`flavor='woff2'`). |
| `dm-mono-300.woff2` | DM Mono Light (300) | OFL 1.1 | Google Fonts, subset `latin`, woff2 (descarga unica para autoalojar). |
| `dm-mono-400.woff2` | DM Mono Regular (400) | OFL 1.1 | idem. |
| `dm-mono-300-italic.woff2` | DM Mono Light Italic (300) | OFL 1.1 | idem. |

El subset `latin` (U+0000–00FF) cubre EN + ES (acentos, ñ, ¿¡). No se incluye `latin-ext` (no necesario).

## Como regenerar

Inter (desde el TTF del repo de la app):
```python
from fontTools.ttLib import TTFont
f = TTFont("app/assets/fonts/Inter-VariableFont_opsz,wght.ttf")
f.flavor = "woff2"; f.save("fonts/inter-var.woff2")
```

DM Mono (subset latin woff2 de Google Fonts, OFL — descarga unica, NO es CDN en runtime):
```
# URL CSS (con User-Agent de navegador) -> extraer los src woff2 del bloque /* latin */:
https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;1,300&display=swap
# descargar cada woff2 latin -> dm-mono-300.woff2 / dm-mono-400.woff2 / dm-mono-300-italic.woff2
```

Generado el 23/06/2026 al desplegar la landing v2 (canon de color `#BA4A00`).
