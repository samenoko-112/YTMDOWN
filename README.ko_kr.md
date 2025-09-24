# YTMDOWN
언어: [日本語](README.md) | [English (US)](README.en_us.md) | [简体中文](README.zh_cn.md) | [繁體中文](README.zh_tw.md) | [한국어](README.ko_kr.md) | [Français](README.fr_fr.md) | [Deutsch](README.de_de.md) | [Español](README.es_es.md) | [Português (Brasil)](README.pt_br.md) | [Русский](README.ru_ru.md)
YouTube Music에서 앨범을 깔끔하게 다운로드하는 소프트웨어입니다.

## 소프트웨어 소개
[samenoko-112/yt-dlpGUI](https://github.com/samenoko-112/yt-dlpGUI)의 기능을 축소하여,
YouTube Music 다운로드에 특화했습니다.

> [!NOTE]
> 일반 동영상을 다운로드하려면 samenoko-112/NeCd 사용을 권장합니다.

## 특징
### 간단한 설정
URL, 저장 경로, 쿠키(선택), 포맷만 설정하면 됩니다!
추가 옵션은 하나뿐입니다.

### 설정 저장
저장 경로, 쿠키, 포맷 선택을 파일에 저장하고 다음 실행 시 불러옵니다.
매번 다시 설정할 필요가 없습니다.

### 메타데이터
자동으로 삽입되지 않는 트랙 번호와 앨범 아티스트를 설정합니다.
"앨범 아티스트 설정" 옵션을 활성화하면 첫 번째 트랙의 아티스트를 앨범 아티스트로 설정합니다.

### 앨범 아트
앨범 아트를 1:1로 크롭하여 임베드합니다.
일부 파일 형식에 임베드하려면 mutagen이 필요합니다.

## 스크린샷
![](img/2025-05-05-23-52-10.png)

![알림](img/2025-05-05-23-52-38.png)

## 동작 환경
| OS | Version | .py | Binary |
| -- | --- | - | - |
| Windows10 Pro | 19045.5737 | OK | OK |
| Ubuntu 24.04 | LTS | OK | OK |
| macOS | 15 | OK | OK |

※ 실행 파일 배포는 Windows 전용입니다.

## 필수
- Python 3.10+
- yt-dlp
    ```shell
    pip install yt-dlp
    ```
- ffmpeg
- mutagen (일부 파일 메타데이터 임베드 시 필요)
    ```shell
    pip install mutagen
    ```

## 트러블슈팅
### 바이러스 판정됨
빌드 시 부트로더를 재빌드하는 등 대책을 적용하지만 일부 소프트웨어에서는 오탐지될 수 있습니다.
실행 파일을 허용 목록에 추가하거나, 이 저장소를 클론하여 직접 빌드하세요.

### 오류 발생
우선 yt-dlp를 업데이트해 보세요. 이 도구는 yt-dlp를 내장하지 않습니다.
```shell
pip install -U yt-dlp
```
이것으로 해결되면 가장 간단합니다. 다운로드 로그는 logs 폴더에 저장되며 .txt 형식이므로 메모장으로 열 수 있습니다.
오류 로그를 검색하거나 AI에 질문해 보세요.


