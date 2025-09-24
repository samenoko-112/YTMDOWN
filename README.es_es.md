# YTMDOWN
Idiomas: [日本語](README.md) | [English (US)](README.en_us.md) | [简体中文](README.zh_cn.md) | [繁體中文](README.zh_tw.md) | [한국어](README.ko_kr.md) | [Français](README.fr_fr.md) | [Deutsch](README.de_de.md) | [Español](README.es_es.md) | [Português (Brasil)](README.pt_br.md) | [Русский](README.ru_ru.md)
Software para descargar álbumes de YouTube Music de forma ordenada.

## Acerca del software
Esta aplicación es una versión simplificada de [samenoko-112/yt-dlpGUI](https://github.com/samenoko-112/yt-dlpGUI),
especializada en descargas de YouTube Music.

> [!NOTE]
> Si desea descargar videos normales, use samenoko-112/NeCd.

## Características
### Configuración sencilla
Solo URL, carpeta de salida, cookies (opcional) y formato.
Hay solo una opción adicional.

### Guardar configuración
La carpeta de salida, las cookies y el formato se guardan y se cargan al iniciar,
para no tener que configurarlo cada vez.

### Metadatos
Establece el número de pista y el artista del álbum cuando no se integran automáticamente.
Si activa "Establecer artista del álbum", el artista de la primera pista se usará como artista del álbum.

### Carátula del álbum
La carátula se recorta a 1:1 y se integra.
Para algunos formatos, se requiere mutagen.

## Capturas
![](img/2025-05-05-23-52-10.png)

![Notificación](img/2025-05-05-23-52-38.png)

## Entornos
| OS | Versión | .py | Binario |
| -- | --- | - | - |
| Windows10 Pro | 19045.5737 | OK | OK |
| Ubuntu 24.04 | LTS | OK | OK |
| macOS | 15 | OK | OK |

Nota: Los ejecutables precompilados solo se distribuyen para Windows.

## Requisitos
- Python 3.10+
- yt-dlp
    ```shell
    pip install yt-dlp
    ```
- ffmpeg
- mutagen (necesario para integrar metadatos en algunos archivos)
    ```shell
    pip install mutagen
    ```

## Solución de problemas
### Marcado como virus
A pesar de reconstruir el cargador de arranque durante la compilación, algunos programas pueden detectarlo por error.
Agregue el ejecutable a la lista de permitidos o clone este repositorio y compílelo usted mismo.

### Aparecen errores
Primero, actualice yt-dlp. Esta herramienta no incluye yt-dlp.
```shell
pip install -U yt-dlp
```
Si eso lo soluciona, perfecto. Los registros de descarga se guardan en la carpeta logs en formato .txt,
puede abrirlos con el Bloc de notas. Busque el mensaje de error o pregunte a una IA.


