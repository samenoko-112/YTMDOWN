import subprocess
from flet import *
import os
import threading
import pyperclip
import logging
import datetime
import json
import platform
import requests
from PIL import Image, UnidentifiedImageError
import io
import tempfile

# プラットフォームに応じた通知システムのインポート
if platform.system() == "Windows":
    try:
        from win11toast import toast
        has_windows_toast = True
    except ImportError:
        has_windows_toast = False
else:
    has_windows_toast = False

os.makedirs("./logs",exist_ok=True)
CONFIG_FILE = "./config.json"
VERSION = "1.21"

def show_notification(title, message, image=None):
    """プラットフォームに応じた通知を表示"""
    if platform.system() == "Windows" and has_windows_toast:
        toast(title, message, image=image)
    elif platform.system() == "Darwin":  # macOS
        os.system(f"""
            osascript -e 'display notification "{message}" with title "{title}"'
        """)
    elif platform.system() == "Linux":
        os.system(f'notify-send "{title}" "{message}"')

def main(page:Page):
    page.title = f"YTMDOWN - version{VERSION}"
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
                    format_dropdown.value = config.get("FORMAT","mp3")
                    page.update()
                    #print("読み込んだよ")
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
            "FORMAT": format_dropdown.value
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        #print("保存したよ")

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
        else:
            cookie_file.visible = False
            cookie_select.visible = False
            page.update()
        save_config()

    def change(e):
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

    def change_high_quality(e):
        if set_high_quality.value == True:
            if cookie_from.value == "none":
                set_high_quality.value = False
                set_high_quality.update()
            else:
                set_high_quality.value = True
                set_high_quality.update()
        else:
            set_high_quality.value = False
            set_high_quality.update()
    
    sel_path_dialog = FilePicker(on_result=sel_path)
    sel_cookie_dialog = FilePicker(on_result=sel_cookie)
    page.overlay.append(sel_path_dialog)
    page.overlay.append(sel_cookie_dialog)

    def download(e):
        progress_bar.value = None
        log.controls.append(Text("ダウンロードを開始します...", color=Colors.BLUE))
        dl_btn.disabled = True
        page.update()
        
        # まず最初のエントリのメタデータだけを取得
        metadata_command = [
            "yt-dlp",
            url_input.value,
            "--dump-json",
            "--playlist-items", "1",
            "--no-warnings",
            "--add-header", "Accept-Language:ja-JP"
        ]
        
        if cookie_from.value == "firefox":
            metadata_command.extend(["--cookies-from-browser", "firefox"])
        elif cookie_from.value == "file":
            metadata_command.extend(["--cookies", cookie_file.value])
        
        # メタデータ取得プロセスを実行
        try:
            metadata_process = subprocess.run(
                metadata_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            
            # JSONとしてパース
            import json
            metadata = json.loads(metadata_process.stdout)
            # 諸々の情報をおいておく
            thumbnail_image = None
            tmp_path = None
            album_name = None
            if 'thumbnail' in metadata:
                thumbnail_url = metadata['thumbnail']
                try:
                    response = requests.get(thumbnail_url, timeout=10)
                    response.raise_for_status()
                    image_bytes = response.content
                    image_stream = io.BytesIO(image_bytes)
                    with Image.open(image_stream) as img:
                        png_stream = io.BytesIO()
                        img.save(png_stream, format="PNG")
                        png_bytes = png_stream.getvalue()
                    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                        temp_file.write(png_bytes)
                        tmp_path = temp_file.name
                        print(f"{tmp_path}")
                except requests.exceptions.RequestException as e:
                    pass
                except UnidentifiedImageError:
                    pass
                except Exception as e:
                    pass

                if tmp_path:
                    thumbnail_image = {
                        'src': tmp_path,
                        'placement': 'hero'
                    }
            if 'album' in metadata:
                album_name = metadata['album']
                
            # artists.0の値を取得（存在する場合）
            album_artist = None
            if 'artist' in metadata:
                album_artist = metadata['artist']
            elif 'artists' in metadata and len(metadata['artists']) > 0:
                album_artist = metadata['artists'][0]
            elif 'uploader' in metadata:
                uploader = metadata['uploader']
                if uploader.endswith(" - Topic"):
                    album_artist = uploader.removesuffix(" - Topic")
                else:
                    album_artist = uploader
            
            elif 'channel' in metadata:
                album_artist = metadata['channel']
                
            log.controls.append(Text(f"アルバムアーティスト: {album_artist}", color=Colors.GREEN))
            page.update()
                
        except Exception as ex:
                log.controls.append(Text(f"メタデータ取得エラー: {str(ex)}", color=Colors.RED))
                page.update()
                album_artist = None
        
        # 通常のダウンロードコマンド
        progress_template = "Downloading: %(progress._percent_str)s | Speed: %(progress._speed_str)s | ETA: %(progress._eta_str)s | Title: %(info.title)s"
        command = [
            "yt-dlp",
            url_input.value,
            "--newline",  # 進捗情報を1行ずつ出力
            "--progress-template", progress_template,
            "--default-search", "ytsearch",
            "--add-header", "Accept-Language:ja-JP",
            "--add-metadata", "--embed-metadata",
            "-x", "--audio-format", format_dropdown.value, "--audio-quality", "0",
            "--embed-thumbnail", "--convert-thumbnails", "jpg",
            "--ppa", "ThumbnailsConvertor:-qmin 1 -q:v 1 -vf crop=\"'if(gt(ih,iw),iw,ih)':'if(gt(iw,ih),ih,iw)'\"",
            "-o", output_path.value+"/%(album)s/%(playlist_index)s - %(title)s.%(ext)s",
            "--parse-metadata", "%(playlist_index)s/%(n_entries)s:%(track_number)s",
            "--parse-metadata", "%(upload_date).4s:%(meta_date)s",
            "--no-warnings",
        ]
        
        if set_high_quality.value == True:
            command.extend(["-S","abr","-f","bestaudio[acodec=opus]","--extractor-args","youtube:formats=missing_pot"])
        else:
            command.extend(["-f","bestaudio/best"])

        # album_artistが取得できた場合は固定値として設定
        # アルバムアーティストが取得できた場合は固定値として設定
        if set_album.value == True:
            if album_artist:
                escaped_artist = album_artist.replace("'", "'\\''")
                command.extend([
                    "--ppa", f"Metadata:-metadata album_artist='{escaped_artist}'"
                ])
            else:
                command.extend(["--parse-metadata", "%(artists.0)s:%(meta_album_artist)s"])
        else:
            # 取得できなかった場合は元のコマンドに戻す
            command.extend(["--parse-metadata", "%(artists.0)s:%(meta_album_artist)s"])
        
        if cookie_from.value == "firefox":
            command.extend(["--cookies-from-browser", "firefox"])
        elif cookie_from.value == "file":
            command.extend(["--cookies", cookie_file.value])

        def run_download():
            nonlocal download_process
            timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            log_filename = os.path.normpath(os.path.join("./logs",f"download_{timestamp}.log"))
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
                    if "Downloading:" in output:
                        progress = progress = output.split("Downloading: ")[1].split(" | ")[0].strip()
                        title = output.split("Title: ")[1].split(" | ")[0].strip()
                        progress_bar.value = float(progress.strip("%")) / 100
                        progress_bar.update()
                        title_text.value = title
                        title_text.update()
                    else:
                        log.controls.append(Text(value=output.strip()))
                        log.scroll_to(offset=-1)
                        log.update()


            for line in process.stderr:
                error_message = line.strip()
                print(error_message)
                logging.error(f"[ERROR] {error_message}")
                log.controls.append(Text(value=f"エラー: {error_message}",color=Colors.RED,weight=FontWeight.BOLD))

            process.wait()

            if process.returncode != 0:
                log.controls.append(Text(value=f"エラーが発生しました:{log_filename}",color=Colors.RED))
                log.scroll_to(offset=-1)
                progress_bar.value = 0
                show_notification("エラーが発生しました", "ダウンロード中にエラーが発生しました")
            else:
                log.controls.append(Text(value="正常にダウンロードできました",color=Colors.GREEN))
                log.scroll_to(offset=-1)
                progress_bar.value = 1
                show_notification("ダウンロード完了", f"{album_artist} - {album_name}をダウンロードしました", image=thumbnail_image)

            title_text.value = ""
            dl_btn.disabled = False
            page.update()
            os.remove(tmp_path)

        threading.Thread(target=run_download, daemon=True).start()

    app_title = Row([
        Text("YTMDOWN",color=Colors.BLACK,size=24,weight=FontWeight.BOLD),
        Text(f"v{VERSION}",color=Colors.BLACK54)
    ])
    url_input = TextField(label="URL", expand=True, on_submit=download)
    paste_btn = IconButton(icon=Icons.PASTE, on_click=paste_url)
    cookie_from = Dropdown(
        options=[
            dropdown.Option(key="none", text="None"),
            dropdown.Option(key="firefox", text="Firefox"),
            dropdown.Option(key="file", text="cookies.txt")
        ],
        label="Cookie From",
        on_change=cookie,
        value="none"
    )
    cookie_file = TextField(label="Cookie File Path", expand=True, visible=False)
    cookie_select = TextButton(
        text="Select", 
        visible=False,
        on_click=lambda _: sel_cookie_dialog.pick_files(allow_multiple=False, allowed_extensions=["txt"])
    )
    format_dropdown = Dropdown(
        options=[
            dropdown.Option(key="mp3", text="mp3"),
            dropdown.Option(key="opus", text="opus"),
            dropdown.Option(key="m4a", text="m4a"),
            dropdown.Option(key="flac", text="flac"),
            dropdown.Option(key="alac", text="alac")
        ],
        label="Format",
        value="mp3",
        on_change=change
    )
    output_path = TextField(label="Output Path", value=os.path.normcase(os.path.expanduser("~")), expand=True)
    output_select = TextButton(text="Select", on_click=lambda e: sel_path_dialog.get_directory_path(dialog_title="保存先を選択"))
    set_album = Checkbox(label="アルバムアーティストを設定")
    set_high_quality = Checkbox(label="最高音質でダウンロードする(要Premium/Cookie)",tooltip="最高音質でダウンロードします。\nPremiumアカウントでログインしているCookieが必要です。\nPremiumアカウントでない場合エラーが発生します。",on_change=change_high_quality)
    progress_bar = ProgressBar(value=0)
    title_text = TextField(read_only=True, label="Title")
    log = Column(
        controls=[],
        scroll=ScrollMode.AUTO,
        on_scroll_interval=0,
        height=400,  # ログ表示部分の高さを増やしました
        width=float("inf"),   # 幅を設定
        spacing=2,
        expand=True
    )
    dl_btn = ElevatedButton(text="ダウンロード", icon=Icons.DOWNLOAD, on_click=download, width=200)  # ボタンサイズ調整

    # 左パネル: 操作コントロール
    left_panel = Container(
        content=Column(
            controls=[
                app_title,
                Row([url_input, paste_btn], alignment=MainAxisAlignment.SPACE_BETWEEN),
                Row([output_path, output_select], alignment=MainAxisAlignment.SPACE_BETWEEN),
                Row([cookie_from,format_dropdown]),
                Row([cookie_file, cookie_select], alignment=MainAxisAlignment.SPACE_BETWEEN),
                set_album,
                set_high_quality,
                title_text,
                progress_bar,
                Row([dl_btn], alignment=MainAxisAlignment.CENTER)  # ダウンロードボタンを中央に配置
            ],
            spacing=15,  # コントロール間の間隔を広げました
            horizontal_alignment=CrossAxisAlignment.START
        ),
        width=500,
        padding=15,
        margin=margin.only(right=10)
    )

    # 右パネル: ログ表示エリア
    right_panel = Container(
        content=Column(
            controls=[
                Text("ログ", size=16, weight=FontWeight.BOLD),  # タイトル追加
                log
            ]
        ),
        expand=True,
        border=border.all(1, "#DDDDDD"),
        border_radius=border_radius.all(10),
        padding=15
    )

    # メインレイアウト
    page.add(
        Row(
            [left_panel, right_panel],
            spacing=10,
            expand=True,
            alignment=MainAxisAlignment.START
        )
    )

    load_config()

if __name__ == "__main__":
    app(target=main)