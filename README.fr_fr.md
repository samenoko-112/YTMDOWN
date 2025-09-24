# YTMDOWN
Logiciel pour télécharger proprement des albums depuis YouTube Music.

## À propos
Cette application est une version allégée de [samenoko-112/yt-dlpGUI](https://github.com/samenoko-112/yt-dlpGUI),
spécialisée pour YouTube Music.

> [!NOTE]
> Pour télécharger des vidéos classiques, utilisez plutôt samenoko-112/NeCd.

## Fonctionnalités
### Paramétrage simple
URL, dossier de sortie, cookies (optionnel) et format uniquement !
Une seule option supplémentaire.

### Sauvegarde des paramètres
Le dossier de sortie, les cookies et le format sont enregistrés et rechargés au prochain démarrage,
pour éviter de tout reconfigurer.

### Métadonnées
Définit les numéros de piste et l’artiste de l’album lorsqu’ils ne sont pas intégrés automatiquement.
Avec l’option « Définir l’artiste de l’album », l’artiste de la première piste est utilisé.

### Pochette d’album
La pochette est recadrée en 1:1 et intégrée.
Pour certains formats, mutagen est requis.

## Captures d’écran
![](img/2025-05-05-23-52-10.png)

![Notification](img/2025-05-05-23-52-38.png)

## Environnements
| OS | Version | .py | Binaire |
| -- | --- | - | - |
| Windows10 Pro | 19045.5737 | OK | OK |
| Ubuntu 24.04 | LTS | OK | OK |
| macOS | 15 | OK | OK |

Note : Des exécutables précompilés sont fournis uniquement pour Windows.

## Prérequis
- Python 3.10+
- yt-dlp
    ```shell
    pip install yt-dlp
    ```
- ffmpeg
- mutagen (nécessaire pour intégrer les métadonnées dans certains fichiers)
    ```shell
    pip install mutagen
    ```

## Dépannage
### Détecté comme virus
Bien que le bootloader soit reconstruit lors du build, certains antivirus peuvent encore le signaler par erreur.
Ajoutez l’exécutable à la liste d’autorisation ou clonez ce dépôt et construisez-le vous‑même.

### Des erreurs se produisent
Commencez par mettre à jour yt-dlp. Cet outil n’embarque pas yt-dlp.
```shell
pip install -U yt-dlp
```
Si cela règle le problème, parfait. Les journaux de téléchargement sont dans le dossier logs au format .txt,
vous pouvez les ouvrir avec le Bloc‑notes. Cherchez le message d’erreur ou demandez à une IA.


