# YTMDOWN
Languages: [日本語](README.ja_jp.md) | [English (US)](README.md) | [简体中文](README.zh_cn.md) | [繁體中文](README.zh_tw.md) | [한국어](README.ko_kr.md) | [Français](README.fr_fr.md) | [Deutsch](README.de_de.md) | [Español](README.es_es.md) | [Português (Brasil)](README.pt_br.md) | [Русский](README.ru_ru.md)
Software to neatly download albums from YouTube Music.

## About this Software
This app is a trimmed-down version of [samenoko-112/yt-dlpGUI](https://github.com/samenoko-112/yt-dlpGUI),
specialized for downloading from YouTube Music.

> [!NOTE]
> If you want to download regular videos, please use samenoko-112/NeCd.

## Features
### Simple settings
Only URL, output directory, Cookies (optional), and format!
There is just one extra option.

### Save settings
Your output path, cookies, and format selections are saved to a file and loaded at next startup,
so you don't have to set them again.

### Metadata
Sets track numbers and album artist that are not automatically embedded.
If you enable the "Set album artist" option, the artist of the first track will be set as the album artist.

### Album art
Album art is cropped to 1:1 and embedded.
For embedding into some file types, mutagen is required.

## Screenshots
![](img/2025-05-05-23-52-10.png)

![Notification](img/2025-05-05-23-52-38.png)

## Environments
| OS | Version | .py | Binary |
| -- | --- | - | - |
| Windows10 Pro | 19045.5737 | OK | OK |
| Ubuntu 24.04 | LTS | OK | OK |
| macOS | 15 | OK | OK |

Note: Prebuilt executables are distributed for Windows only.

## Requirements
- Python 3.10+
- yt-dlp
    ```shell
    pip install yt-dlp
    ```
- ffmpeg
- mutagen (required for embedding metadata into some files)
    ```shell
    pip install mutagen
    ```

## Troubleshooting
### Flagged as a virus
Although we rebuild the bootloader during build, some software may still falsely detect it.
Please add the executable to the allowlist or clone this repository and build it yourself.

### Errors occur
First, try updating yt-dlp. This tool does not bundle yt-dlp.
```shell
pip install -U yt-dlp
```
If that solves it, great. Download logs are stored in the logs folder in .txt format,
so you can open them in Notepad. Try searching the error log or ask AI for help.

