import yt_dlp
from ytmusicapi import YTMusic

# Function to get video IDs from the artist's profile URL
def get_artist_video_ids(profile_url):
    # Initialize yt-dlp options
    ydl_opts = {
        'quiet': True,  # Suppress output to make it less noisy
        'extract_flat': True,  # Extract only the video URLs, not the full details
        'noplaylist': True,  # Don't fetch playlists
        'max_downloads': 1000  # Limit to 1000 results (or change as needed)
    }

    # Use yt-dlp to extract all videos from the artist's channel or profile
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(profile_url, download=False)

    if 'entries' not in result or not result['entries']:
        print(f"No videos found for profile URL: {profile_url}")
        return []

    # Extract video IDs (URLs) from the results
    video_ids = [entry['id'] for entry in result['entries']]
    return video_ids

# Function to create the playlist from the extracted video IDs
def create_playlist_from_profile(profile_url, playlist_name):
    # Get video IDs from the artist's profile URL
    song_ids = get_artist_video_ids(profile_url)

    if not song_ids:
        print(f"No songs found for the profile URL: {profile_url}")
        return

    # Print out the song URLs (for debugging)
    print(f"Found {len(song_ids)} songs. Creating playlist...")

    # Initialize YTMusic with authentication
    ytmusic = YTMusic('headers_auth.json')

    # Create a new playlist
    playlist_id = ytmusic.create_playlist(
        title=playlist_name,
        description=f"Playlist of all songs by the artist from {profile_url}",
        privacy_status="PRIVATE"  # Options: PRIVATE, PUBLIC, UNLISTED
    )

    # Add songs to the playlist
    ytmusic.add_playlist_items(playlist_id, song_ids)

    print(f"Playlist '{playlist_name}' created successfully with {len(song_ids)} songs!")

# Get the artist profile URL from user input
profile_url = input("Enter the YouTube profile URL of the artist: ")
playlist_name = f"All Songs from {profile_url.split('/')[-1]}"

# Create the playlist
create_playlist_from_profile(profile_url, playlist_name)
