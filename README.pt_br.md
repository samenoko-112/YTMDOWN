# YTMDOWN
Idiomas: [日本語](README.ja_jp.md) | [English (US)](README.md) | [简体中文](README.zh_cn.md) | [繁體中文](README.zh_tw.md) | [한국어](README.ko_kr.md) | [Français](README.fr_fr.md) | [Deutsch](README.de_de.md) | [Español](README.es_es.md) | [Português (Brasil)](README.pt_br.md) | [Русский](README.ru_ru.md)
Software para baixar álbuns do YouTube Music de forma prática.

## Sobre o software
Este app é uma versão enxuta de [samenoko-112/yt-dlpGUI](https://github.com/samenoko-112/yt-dlpGUI),
especializado em downloads do YouTube Music.

> [!NOTE]
> Para baixar vídeos comuns, use o samenoko-112/NeCd.

## Recursos
### Configuração simples
Apenas URL, pasta de saída, cookies (opcional) e formato!
Há apenas uma opção extra.

### Salvar configurações
O caminho de saída, os cookies e o formato são salvos e carregados na próxima inicialização,
evitando redefinições a cada vez.

### Metadados
Define o número da faixa e o artista do álbum quando não são inseridos automaticamente.
Se você ativar "Definir artista do álbum", o artista da primeira faixa será usado como artista do álbum.

### Capa do álbum
A capa é recortada em 1:1 e incorporada.
Para alguns formatos, é necessário o mutagen.

## Capturas de tela
![](img/2025-05-05-23-52-10.png)

![Notificação](img/2025-05-05-23-52-38.png)

## Ambientes
| OS | Versão | .py | Binário |
| -- | --- | - | - |
| Windows10 Pro | 19045.5737 | OK | OK |
| Ubuntu 24.04 | LTS | OK | OK |
| macOS | 15 | OK | OK |

Observação: os executáveis pré-compilados são distribuídos apenas para Windows.

## Requisitos
- Python 3.10+
- yt-dlp
    ```shell
    pip install yt-dlp
    ```
- ffmpeg
- mutagen (necessário para incorporar metadados em alguns arquivos)
    ```shell
    pip install mutagen
    ```

## Solução de problemas
### Marcado como vírus
Embora reconstruamos o bootloader durante o build, alguns softwares podem sinalizá-lo por engano.
Adicione o executável à lista de permissões ou clone este repositório e faça o build você mesmo.

### Ocorreram erros
Primeiro, atualize o yt-dlp. Esta ferramenta não inclui o yt-dlp.
```shell
pip install -U yt-dlp
```
Se isso resolver, ótimo. Os logs de download ficam na pasta logs em formato .txt,
podem ser abertos no Bloco de Notas. Procure a mensagem de erro ou pergunte a uma IA.


