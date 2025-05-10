import streamlit as st
import pandas as pd
import plotly.express as px
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import re

# Set page config
st.set_page_config(
    page_title="Music Visualization App",
    page_icon="🎵",
    layout="wide",
)
# Load environment variables
if "SPOTIPY_CLIENT_ID" in st.secrets:
    client_id = st.secrets["SPOTIPY_CLIENT_ID"]
    client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
    redirect_uri = st.secrets["REDIRECT_URI"]
else:
    load_dotenv()
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")


# Initialize Spotify client
sp = None
if client_id and client_secret:
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Initialize session state
if 'songs_data' not in st.session_state:
    st.session_state.songs_data = pd.DataFrame(columns=['id', 'name', 'artist', 'valence', 'energy', 'danceability', 'popularity', 'preview_url', 'album_img'])

def extract_track_id(spotify_url):
    """Extract the track ID from a Spotify URL or URI."""
    patterns = [
        r'spotify:track:([a-zA-Z0-9]+)',         # Spotify URI
        r'open.spotify.com/track/([a-zA-Z0-9]+)', # Spotify URL
        r'^([a-zA-Z0-9]+)$'                       # Track ID directly
    ]
    
    for pattern in patterns:
        match = re.search(pattern, spotify_url)
        if match:
            return match.group(1)
    
    return None

def get_track_features(track_id):
    """Get track features from Spotify API."""
    if not sp:
        st.error("Spotify API credentials not set. Please add them to your .env file.")
        return None
    
    try:
        # Get track info
        track_info = sp.track(track_id)
        
        # Get audio features
        audio_features = sp.audio_features([track_id])[0]
        
        # Combine the data
        track_data = {
            'id': track_id,
            'name': track_info['name'],
            'artist': track_info['artists'][0]['name'],
            'valence': audio_features['valence'],
            'energy': audio_features['energy'],
            'danceability': audio_features['danceability'],
            'popularity': track_info['popularity'],
            'preview_url': track_info['preview_url'],
            'album_img': track_info['album']['images'][1]['url'] if track_info['album']['images'] else None
        }
        
        return track_data
    
    except Exception as e:
        st.error(f"Error retrieving track data: {e}")
        return None

def add_song(spotify_link):
    """Add a song to the visualization."""
    track_id = extract_track_id(spotify_link)
    
    if not track_id:
        st.error("Invalid Spotify link. Please provide a valid Spotify track URL or URI.")
        return
    
    # Check if song already exists
    if track_id in st.session_state.songs_data['id'].values:
        st.warning(f"This song is already in your visualization.")
        return
    
    # Get track features
    track_data = get_track_features(track_id)
    
    if track_data:
        # Add to session state dataframe
        st.session_state.songs_data = pd.concat([
            st.session_state.songs_data,
            pd.DataFrame([track_data])
        ], ignore_index=True)
        
        st.success(f"Added: {track_data['name']} by {track_data['artist']}")

def main():
    st.title("🎵 Music Visualization App")
    
    # Display API status
    if sp:
        st.sidebar.success("✅ Connected to Spotify API")
    else:
        st.sidebar.error("❌ Spotify API not connected. Check your .env file.")
        st.sidebar.info("To use this app, you need to create a Spotify Developer account and get API credentials. Add them to a .env file in the project directory.")
        st.sidebar.code("SPOTIPY_CLIENT_ID=your_client_id\nSPOTIFY_CLIENT_SECRET=your_client_secret")
    
    # Add new songs
    st.sidebar.header("Add New Songs")
    spotify_link = st.sidebar.text_input("Paste Spotify link/URI or track ID:")
    if st.sidebar.button("Add Song") and spotify_link:
        add_song(spotify_link)
    
    # Sample tracks to get started
    st.sidebar.header("Sample Tracks")
    if st.sidebar.button("Add Sample Tracks"):
        sample_tracks = [
            "spotify:track:4cOdK2wGLETKBW3PvgPWqT",  # Rick Astley - Never Gonna Give You Up
            "spotify:track:4PTG3Z6ehGkBFwjybzWkR8",  # Harry Styles - As It Was
            "spotify:track:7qiZfU4dY1lWllzX7mPBI3",  # Ed Sheeran - Shape of You
            "spotify:track:4MKzCHlZvkwJOQRNkdLbGz",  # Adele - Hello
            "spotify:track:3w3y8KPTfNeOKPiqUTakBh",  # Metallica - Nothing Else Matters
        ]
        for track in sample_tracks:
            add_song(track)
    
    # Main visualization
    if not st.session_state.songs_data.empty:
        st.header("Song Visualization")
        st.write("**x-axis**: valence (musical positiveness), **y-axis**: energy, **color**: danceability, **size**: popularity")
        
        # Create the scatter plot with Plotly
        fig = px.scatter(
            st.session_state.songs_data,
            x="valence",
            y="energy",
            color="danceability",
            size="popularity",
            hover_name="name",
            hover_data=["artist", "danceability", "popularity"],
            color_continuous_scale=px.colors.sequential.Viridis,
            size_max=30,
            range_x=[0, 1],
            range_y=[0, 1],
            title="Song Audio Features Visualization"
        )
        
        fig.update_layout(
            height=600,
            xaxis_title="Valence (Musical Positiveness)",
            yaxis_title="Energy",
            coloraxis_colorbar_title="Danceability"
        )
        
        # Display the plot
        chart = st.plotly_chart(fig, use_container_width=True)
        
        # Display songs table with preview functionality
        st.header("Songs")
        
        # Custom CSS for the song cards
        st.markdown("""
        <style>
        .song-card {
            display: flex;
            align-items: center;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            background-color: #f0f2f6;
        }
        .song-img {
            width: 60px;
            height: 60px;
            margin-right: 15px;
        }
        .song-info {
            flex-grow: 1;
        }
        .song-title {
            font-weight: bold;
            margin-bottom: 5px;
        }
        .song-artist {
            color: #666;
            font-size: 0.9em;
        }
        .song-features {
            color: #888;
            font-size: 0.8em;
            margin-top: 5px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        for _, song in st.session_state.songs_data.iterrows():
            col1, col2 = st.columns([1, 4])
            
            with col1:
                if song['album_img']:
                    st.image(song['album_img'], width=80)
                else:
                    st.markdown("🎵")
            
            with col2:
                st.markdown(f"**{song['name']}**")
                st.markdown(f"by {song['artist']}")
                
                features_text = (
                    f"Valence: {song['valence']:.2f} | "
                    f"Energy: {song['energy']:.2f} | "
                    f"Danceability: {song['danceability']:.2f} | "
                    f"Popularity: {song['popularity']}/100"
                )
                st.markdown(f"<span style='color: #888; font-size: 0.9em;'>{features_text}</span>", unsafe_allow_html=True)
                
                if song['preview_url']:
                    st.audio(song['preview_url'])
                else:
                    st.markdown("*No audio preview available*")
            
            st.markdown("---")
    else:
        st.info("Add songs using the sidebar to visualize them here!")
        
        # Show information about the app
        st.markdown("""
        ## How to use this app
        
        1. **Add Spotify API credentials** - Create a .env file with your Spotify Developer credentials
        2. **Add songs** - Paste Spotify song links or use the sample tracks button
        3. **Explore the visualization** - See how songs compare based on their audio features
        4. **Listen to previews** - Click on a song to hear a preview (if available)
        
        ### Understanding the visualization
        
        - **Valence** (x-axis): Musical positiveness conveyed by a track (0.0 to 1.0)
        - **Energy** (y-axis): Intensity and activity measure (0.0 to 1.0)
        - **Danceability** (color): How suitable a track is for dancing (0.0 to 1.0)
        - **Popularity** (size): The song's popularity on Spotify (0 to 100)
        """)

if __name__ == "__main__":
    main() 