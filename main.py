from tinytag import TinyTag as tg
import os
import pathlib

def get_files(folder):
	FILE_EXTENSIONS = ['.mp3', '.m4a', '.flac', '.wav', '.ogg', '.opus']
	files = {}
	for file in folder.iterdir():
		if file.is_file() and file.suffix in FILE_EXTENSIONS:
			files[file.name] = file
			print(f"Added file: {file.name}")
	return files

def get_metadata(file):
	tag = tg.get(file)
	metadata = {
		"title": tag.title,
		"artist": tag.artist if tag.album else "Unknown Artist",
		"album": tag.album if tag.album else "Unknown Album", 
		"track": tag.track,
		"duration": tag.duration,
		"genre": tag.genre,
		"path": file,
	}
	print(f"Added metadata for: {metadata['title']}")
	return metadata

def generate_directory_structure(chosen_folder, structure_dict):
	for artist, albums in structure_dict.items():
		artist_folder = chosen_folder / pathlib.Path(artist)
		if artist_folder.exists():
			print(f"Artist folder already exists. Skipping: {artist_folder}")
		else:
			artist_folder.mkdir(parents=True, exist_ok=True)
			print(f"Created artist folder: {artist_folder}")
		for album, songs in albums.items():
			album_folder = pathlib.Path(artist_folder, album)
			if album_folder.exists():
				print(f"Album folder already exists. Skipping: {album_folder}")
			else:
				album_folder = chosen_folder / album_folder
				album_folder.mkdir(parents=True, exist_ok=True)
				print(f"Created album folder: {album_folder}")
			for song, metadata in songs.items():
				song_path = pathlib.Path(album_folder, song)
				if song_path.exists():
					print(f"Song already exists. Skipping: {song_path}")
				else:
					print(f"Moved song: {metadata['title']} to {song_path}")
				os.rename(metadata["path"], song_path)
	print("\nFinished!\n")
	
def preprocess(folder):
	files = get_files(folder)
	for title, path in files.items():
		files[title] = get_metadata(path)
	return files

def process(files):
	artists = {}
	albums = {}
	for title, metadata in files.items():
		artist = metadata["artist"]
		album = metadata["album"]
		if artist not in artists:
			artists[artist] = {}
			print(f"Added artist: {artist}")
		if album not in artists[artist]:
			artists[artist][album] = {}
			print(f"Added album: {album} for artist: {artist}")
		artists[artist][album][title] = metadata
		print(f"Added song: {title} to album: {album} by artist: {artist}")
	return artists

def main():
	music_folder = pathlib.Path(input("Please enter the absolute path to the folder containing your music: "))
	ignore_subfolders = input("Do you want the program to affect files already in subfolders? (y/n): ")
	while True:
		if not music_folder.exists():
			music_folder = pathlib.Path(input("Not a valid folder, please input again! "))
		else:
			break
	while True:
		if ignore_subfolders.lower() in ["y", "yes"]:
			ignore_subfolders = True
			break
		elif ignore_subfolders.lower() in ["n", "no"]:
			ignore_subfolders = False
			break
		else:
			ignore_subfolders = input("Not a valid input, please try again (y/n): ")
	files = preprocess(music_folder)
	artists = process(files)
	generate_directory_structure(music_folder, artists)
if __name__ == "__main__":
	main()
