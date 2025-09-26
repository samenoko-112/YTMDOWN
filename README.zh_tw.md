# YTMDOWN
語言: [日本語](README.ja_jp.md) | [English (US)](README.md) | [简体中文](README.zh_cn.md) | [繁體中文](README.zh_tw.md) | [한국어](README.ko_kr.md) | [Français](README.fr_fr.md) | [Deutsch](README.de_de.md) | [Español](README.es_es.md) | [Português (Brasil)](README.pt_br.md) | [Русский](README.ru_ru.md)
用於從 YouTube Music 優雅地下載專輯的軟體。

## 關於本軟體
本應用從 [samenoko-112/yt-dlpGUI](https://github.com/samenoko-112/yt-dlpGUI) 精簡而來，
專注於 YouTube Music 的下載。

> [!NOTE]
> 若需要下載一般影片，建議使用 samenoko-112/NeCd。

## 特色
### 簡單設定
只需 URL、儲存位置、Cookie（可選）與格式！
僅有一個額外選項。

### 儲存設定
會將你的儲存路徑、Cookie、格式選擇儲存到檔案，並於下次啟動時讀取，
免去每次重新設定的麻煩。

### 中繼資料
設定不會自動嵌入的曲目編號與專輯藝人。
若啟用「設定專輯藝人」，會將第一首曲目的藝人設為專輯藝人。

### 專輯封面
將專輯封面裁切為 1:1 並嵌入。
部分檔案類型的嵌入需要 mutagen。

## 截圖
![](img/2025-05-05-23-52-10.png)

![通知](img/2025-05-05-23-52-38.png)

## 系統需求
| OS | Version | .py | Binary |
| -- | --- | - | - |
| Windows10 Pro | 19045.5737 | OK | OK |
| Ubuntu 24.04 | LTS | OK | OK |
| macOS | 15 | OK | OK |

註：目前僅發佈 Windows 可執行檔。

## 必要元件
- Python 3.10+
- yt-dlp
    ```shell
    pip install yt-dlp
    ```
- ffmpeg
- mutagen（部分檔案的中繼資料嵌入需要）
    ```shell
    pip install mutagen
    ```

## 疑難排解
### 被判定為病毒
雖然在建置時會重新建置 bootloader，但部分軟體仍可能誤判。
請將執行檔加入允許清單，或自行 clone 專案並建置。

### 出現錯誤
請先嘗試更新 yt-dlp。本工具未內建 yt-dlp。
```shell
pip install -U yt-dlp
```
若能解決那就最好。下載日誌保存在 logs 資料夾，.txt 格式，可用記事本開啟。
也可以嘗試搜尋錯誤日誌或詢問 AI 協助。


