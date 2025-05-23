import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page config
st.set_page_config(
    page_title="Music Visualization App",
    page_icon="🎵",
    layout="wide",
)

# Song data
SONGS_DATA = {
    "bad_guy": {
        "name": "Bad Guy",
        "artist": "Billie Eilish",
        "valence": 0.56,
        "energy": 0.43,
        "danceability": 0.70,
        "popularity": 95,
        "audio_file": "audio/bad_guy.mp3"
    },
    "happier": {
        "name": "Happier",
        "artist": "Marshmello & Bastille",
        "valence": 0.67,
        "energy": 0.79,
        "danceability": 0.69,
        "popularity": 88,
        "audio_file": "audio/happier.mp3"
    },
    "higher_love": {
        "name": "Higher Love",
        "artist": "Kygo & Whitney Houston",
        "valence": 0.40,
        "energy": 0.68,
        "danceability": 0.69,
        "popularity": 88,
        "audio_file": "audio/higher_love.mp3"
    },
    "panini": {
        "name": "Panini",
        "artist": "Lil Nas X",
        "valence": 0.48,
        "energy": 0.59,
        "danceability": 0.70,
        "popularity": 91,
        "audio_file": "audio/panini.mp3"
    },
    "shallow": {
        "name": "Shallow",
        "artist": "Lady Gaga & Bradley Cooper",
        "valence": 0.32,
        "energy": 0.39,
        "danceability": 0.57,
        "popularity": 87,
        "audio_file": "audio/shallow.mp3"
    }
}

def main():
    st.title("🎵 Music Visualization App")
    
    # Convert songs data to DataFrame
    songs_df = pd.DataFrame.from_dict(SONGS_DATA, orient='index')
    
    # Main visualization
    st.header("Song Visualization")
    st.write("**x-axis**: valence (musical positiveness), **y-axis**: energy, **color**: danceability, **size**: popularity")
    
    # Create the scatter plot with Plotly
    fig = px.scatter(
        songs_df,
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
    
    # Display songs with audio players
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
    
    for song_id, song in SONGS_DATA.items():
        st.markdown(f"**{song['name']}**")
        st.markdown(f"by {song['artist']}")
        
        features_text = (
            f"Valence: {song['valence']:.2f} | "
            f"Energy: {song['energy']:.2f} | "
            f"Danceability: {song['danceability']:.2f} | "
            f"Popularity: {song['popularity']}/100"
        )
        st.markdown(f"<span style='color: #888; font-size: 0.9em;'>{features_text}</span>", unsafe_allow_html=True)
        
        # Audio player
        st.audio(song['audio_file'])
        
        st.markdown("---")
    
    # Data source information
    st.markdown("---")
    st.markdown("### Data Source")
    st.markdown("The song data is from the Kaggle dataset: [Top 50 Spotify Songs - 2019](https://www.kaggle.com/datasets/leonardopena/top50spotify2019)")

if __name__ == "__main__":
    main() 