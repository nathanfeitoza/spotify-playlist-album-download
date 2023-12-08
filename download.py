import requests
import asyncio
import time
import os
import argparse

base_url = 'https://api.spotifydown.com/'
headers = {
    'origin': 'https://spotifydown.com',
    'referer': 'https://spotifydown.com/'
}

def sanitize_filename(filename):
    filename = filename.replace('\\', '').replace('/', '-').replace('?', '')
    return filename

async def download_mp3(url, playlist_info, filename):
    folder = f"files/{sanitize_filename(playlist_info)}"

    if not os.path.exists(folder):
      os.makedirs(folder)

    filename = sanitize_filename(filename)
    file_path = folder + "/" + filename

    if os.path.exists(file_path):
      print(f"File {file_path} was downloaded!!!")
      return

    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded and saved as {file_path}")
    else:
        print("Failed to download the file")

def get_music_download_link(track_id):
    response = requests.get(base_url + 'download/' + track_id, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get download link")

def get_playlist_tracks(playlist_id, is_album=None, offset=None, tracks=[]):
    use_offset = f'?offset={offset}' if offset is not None else ''
    endpoint = 'album' if is_album else 'playlist'
    response = requests.get(f"{base_url}trackList/{endpoint}/{playlist_id}{use_offset}", headers=headers)

    if response.status_code == 200:
        
        playlist_data = response.json()

        if playlist_data["nextOffset"] is not None:
            return get_playlist_tracks(playlist_id=playlist_id, offset=playlist_data["nextOffset"], tracks=tracks + playlist_data["trackList"])
        else:
            return tracks + playlist_data["trackList"]
    else:
        print("Failed to get playlist tracks")

def get_playlist_metadata(playlist_id, is_album=None):
    endpoint = 'album' if is_album else 'playlist'
    response = requests.get(f"{base_url}metadata/{endpoint}/{playlist_id}", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get playlist metadata")

async def download_all_musics_from_playlist(playlist_id, is_album=None):
    start_time = time.perf_counter()
    print('Search playlist tracks...')
    playlist_metadata = get_playlist_metadata(playlist_id, is_album)

    if playlist_metadata is None:
        print("Failed to get playlist metadata")
        return

    tracks = get_playlist_tracks(playlist_id, is_album)

    print(f'Found {len(tracks)} tracks')
    print("--------------------------------------------------\n")

    tracks_downloaded = 0
    
    for track in tracks:
        print(f'Search music id: {track["id"]}, name: {track["title"]}, artist: {track["artists"]}')
        track_info = get_music_download_link(track["id"])

        if track_info is None:
            continue

        track_info_sucess = track_info["success"]
        
        if track_info_sucess is False:
            print("Failed to get download link")
            continue

        track_metada = track_info["metadata"]
        music_name = track_metada["title"] + " - " + track_metada["artists"]

        if 'link' not in track_info:
            print("Music withou download link")
            continue
        
        await download_mp3(url=track_info["link"], playlist_info=f'{playlist_metadata["title"]} - {playlist_id}', filename=music_name + ".mp3")
        tracks_downloaded += 1
        print(f"Downloaded {tracks_downloaded} of {len(tracks)}\n ")
        print(f"{tracks_downloaded / len(tracks) * 100:.2f}%")
        print("--------------------------------------------------\n")
    
    end_time = time.perf_counter()
    duration = end_time - start_time

    print("Start Time:", start_time)
    print("End Time:", end_time)
    print("Duration:", duration, "seconds")

def main():
  parser = argparse.ArgumentParser(description="Script to donwload spotify playlist tracks.")

  parser.add_argument('--playlistid', type=str, help='Spotify Playlist ID')
  parser.add_argument('--album', type=bool, help='Set the playlist is album')

  args = parser.parse_args()

  if args.playlistid:
      asyncio.run(download_all_musics_from_playlist(args.playlistid, args.album))
  else:
      print("--playlistid is required")

if __name__ == "__main__":
    main()