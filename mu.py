import subprocess
from flet import *
import os
import threading
import pyperclip
import logging
import datetime
import json

os.makedirs("./logs",exist_ok=True)
CONFIG_FILE = "./config.json"

def main(page:Page):
    page.title = "ytm_download"
    page.window.center()

    download_process = None

    def load_config():
        """設定ファイルを読み込んで UI に適用"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    output_path.value = config.get("OUTPUT", "")
                    cookie_from.value = config.get("COOKIE_FROM", "")
                    cookie_file.value = config.get("COOKIE_FILE", "")
            except json.JSONDecodeError:
                print("設定ファイルが壊れています。")
        else:
            save_config()

    def save_config():
        """現在の UI の状態を設定ファイルに保存"""
        config = {
            "OUTPUT": output_path.value,
            "COOKIE_FROM": cookie_from.value,
            "COOKIE_FILE": cookie_file.value,
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

    def on_window_close(e):
        save_config()
        nonlocal download_process
        if download_process and download_process.poll() is None:  # プロセスが実行中の場合
            print("プロセスを終了します...")
            download_process.terminate()  # プロセスを終了
            download_process.wait()  # プロセスの終了を待つ
        page.window_destroy()  # ウィンドウを閉じる

    page.on_close = on_window_close

    def cookie(e):
        if cookie_from.value == "firefox":
            cookie_file.visible = False
            cookie_select.visible = False
            page.update()
        elif cookie_from.value == "file":
            cookie_file.visible = True
            cookie_select.visible = True
            page.update()
        save_config()

    def sel_path(e: FilePickerResultEvent):
        before = output_path.value
        output_path.value = e.path if e.path else before
        output_path.update()
        save_config()

    def sel_cookie(e: FilePickerResultEvent):
        if e.files:
            cookie_file.value = e.files[0].path
            cookie_file.update()
        else:
            cookie_file.value = ""
            cookie_file.update()
        save_config()
    
    def paste_url(e):
        url_input.value = pyperclip.paste()
        url_input.update()

    sel_path_dialog = FilePicker(on_result=sel_path)
    sel_cookie_dialog = FilePicker(on_result=sel_cookie)
    page.overlay.append(sel_path_dialog)
    page.overlay.append(sel_cookie_dialog)

    def download(e):
        progress_bar.value = None
        log.value = "開始しています..."
        dl_btn.disabled = True
        page.update()
        progress_template = "Downloading: %(progress._percent_str)s | Speed: %(progress._speed_str)s | ETA: %(progress._eta_str)s | Title: %(info.title)s"
        command = [
            "yt-dlp",
            url_input.value,
            "--newline",  # 進捗情報を1行ずつ出力
            "--progress-template", progress_template,
            "--default-search", "ytsearch",
            "--add-metadata",
            "-f", "bestaudio[acodec^=opus]/best",
            "-x", "--audio-format", "mp3", "--audio-quality", "0",
            "--embed-thumbnail",
            "--ppa", "EmbedThumbnail+ffmpeg_o:-c:v mjpeg -vf crop=\"'if(gt(ih,iw),iw,ih)':'if(gt(iw,ih),ih,iw)'\"",
            "-o", output_path.value+"/%(album)s/%(playlist_index)s - %(title)s.%(ext)s",
            "--parse-metadata", "playlist_index:%(track_number)s",
            "--parse-metadata", "release_year:%(date)s"
        ]
        if cookie_from.value == "firefox":
            command.extend(["--cookies-from-browser", "firefox"])
        elif cookie_from.value == "file":
            command.extend(["--cookies",cookie_file.value])

        def run_download():
            nonlocal download_process
            timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            log_filename = os.path.join("./logs",f"download_{timestamp}.log")
            logging.basicConfig(
                filename=log_filename,
                level=logging.INFO,
                format="%(asctime)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            # サブプロセスを実行
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
            )
            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    log_entry = f"{output.strip()}"
                    logging.info(log_entry)
                    log.value = output
                    log.update()
                    if "Downloading:" in output:
                        progress = progress = output.split("Downloading: ")[1].split(" | ")[0].strip()
                        title = output.split("Title: ")[1].split(" | ")[0].strip()
                        progress_bar.value = float(progress.strip("%")) / 100
                        progress_bar.update()
                        title_text.value = title
                        title_text.update()


            for line in process.stderr:
                error_message = line.strip()
                print(error_message)
                logging.error(f"[ERROR] {error_message}")

            process.wait()

            if process.returncode != 0:
                log.value = "エラーログ :"+log_filename
                progress_bar.value = 0
            else:
                log.value = "正常にダウンロード出来ました。"
                progress_bar.value = 1

            title_text.value = ""
            dl_btn.disabled = False
            page.update()

        threading.Thread(target=run_download, daemon=True).start()


    url_input = TextField(label="URL", expand=True, on_submit=download)
    paste_btn = IconButton(icon=Icons.PASTE, on_click=paste_url)
    cookie_from = Dropdown(options=[dropdown.Option(key="firefox",text="Firefox"),dropdown.Option(key="file",text="cookies.txt")],label="Cookie From",on_change=cookie)
    cookie_file = TextField(label="Cookie File Path",expand=True,visible=False)
    cookie_select = TextButton(text="Select",visible=False,on_click=lambda _:sel_cookie_dialog.pick_files(allow_multiple=False,allowed_extensions=["txt"]))
    output_path = TextField(label="Output Path", value=os.path.normcase(os.path.expanduser("~")), expand=True)
    output_select = TextButton(text="Select", on_click=lambda e: sel_path_dialog.get_directory_path(dialog_title="保存先を選択"))
    progress_bar = ProgressBar(value=0)
    title_text = TextField(read_only=True, label="Title")
    log = Text(max_lines=1,value="ログが表示されます")
    dl_btn = FloatingActionButton(icon=Icons.DOWNLOAD, on_click=download)

    page.add(
        Row([url_input, paste_btn]),
        Row([output_path, output_select]),
        cookie_from,
        Row([cookie_file, cookie_select]),
        title_text,
        progress_bar,
        log,
        dl_btn
    )

    load_config()

if __name__ == "__main__":
    app(target=main)