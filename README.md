---
runme:
  id: 01HH3G2Y7584J8HBRJVFM1DJEP
  version: v2.0
---

## Spotify Playlist and Album Downloader - Python Script

## Description

This Python script enables users to download playlists or albums from Spotify as MP3 files. The tool is designed for personal use to allow Spotify users to save their favorite music offline. It is essential to note that the use of this script should comply with Spotify's terms of service and copyright laws.

## Features

- **Download Playlists**: Download any playlist from your Spotify account.
- **Download Albums**: Download entire albums based on Spotify's album ID.
- **High-Quality MP3**: Downloads are saved as high-quality MP3 files.
- **ID3 Tags**: Automatically adds ID3 tags (title, artist, album) to the MP3 files.

## Prerequisites

- Python 3.6 or higher.
- Spotify account and API credentials.

## Installation

1. Clone the repository:

```
https://github.com/nathanfeitoza/spotify-playlist-album-download
```

2. Install the required packages:

```
pip install -r requirements.txt
```

## Usage
Obtain the playlist or album id, this is information is in url of shared resource.
Eg: 

```
https://open.spotify.com/playlist/37i9dQZF1DXbITWG1ZJKYt 

ID is: `37i9dQZF1DXbITWG1ZJKYt`
```

So, run

```
python download.py --playlistid=<playlist_id>
```

Or, if is album

```
python download.py --playlistid=<album_id> --album=true
```

## Disclaimer

This tool is for educational purposes only. The user is responsible for adhering to Spotify's terms of service and respecting copyright laws. This script should not be used for commercial purposes or to distribute copyrighted content.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Spotify API
- Spotifydown API
- Python community for various helpful libraries

---

**Note**: This script is a proof of concept and is not affiliated with, sponsored by, or endorsed by Spotify. Usage of this script may be against Spotify's terms of service. The developer is not responsible for any misuse of this tool.