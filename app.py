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
        "valence": 56,
        "energy": 43,
        "danceability": 70,
        "popularity": 95,
        "audio_file": "audio/bad_guy.mp3"
    },
    "happier": {
        "name": "Happier",
        "artist": "Marshmello & Bastille",
        "valence": 67,
        "energy": 79,
        "danceability": 69,
        "popularity": 88,
        "audio_file": "audio/happier.mp3"
    },
    "higher_love": {
        "name": "Higher Love",
        "artist": "Kygo & Whitney Houston",
        "valence": 40,
        "energy": 68,
        "danceability": 69,
        "popularity": 88,
        "audio_file": "audio/higher_love.mp3"
    },
    "panini": {
        "name": "Panini",
        "artist": "Lil Nas X",
        "valence": 48,
        "energy": 59,
        "danceability": 70,
        "popularity": 91,
        "audio_file": "audio/panini.mp3"
    },
    "shallow": {
        "name": "Shallow",
        "artist": "Lady Gaga & Bradley Cooper",
        "valence": 32,
        "energy": 39,
        "danceability": 57,
        "popularity": 87,
        "audio_file": "audio/shallow.mp3"
    }
}

# Initialize session state
if 'selected_songs' not in st.session_state:
    st.session_state.selected_songs = set()
if 'playing_song' not in st.session_state:
    st.session_state.playing_song = None

def toggle_song(song_id):
    """Toggle song selection in the visualization."""
    if song_id in st.session_state.selected_songs:
        st.session_state.selected_songs.remove(song_id)
        if st.session_state.playing_song == song_id:
            st.session_state.playing_song = None
    else:
        st.session_state.selected_songs.add(song_id)

def toggle_play(song_id):
    """Toggle play/pause for a song."""
    if st.session_state.playing_song == song_id:
        st.session_state.playing_song = None
    else:
        st.session_state.playing_song = song_id

def main():
    st.title("🎵 Music Visualization App")
    
    # Create two columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("Available Songs")
        
        # Custom CSS for the song list
        st.markdown("""
        <style>
        .song-item {
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .song-item:hover {
            background-color: #f0f2f6;
        }
        .song-item.selected {
            background-color: #e6f3ff;
            border-left: 3px solid #1f77b4;
        }
        .stButton button {
            width: 100%;
            text-align: left;
            background: none;
            border: none;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #f0f2f6;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display song list
        for song_id, song in SONGS_DATA.items():
            is_selected = song_id in st.session_state.selected_songs
            if st.button(
                f"**{song['name']}**\n{song['artist']}",
                key=f"toggle_{song_id}",
                help=f"Click to {'remove' if is_selected else 'add'} this song to the visualization"
            ):
                toggle_song(song_id)
                st.rerun()
    
    with col2:
        st.header("Song Visualization")
        st.write("**x-axis**: valence (musical positiveness), **y-axis**: energy, **color**: danceability, **size**: popularity")
        
        # Filter songs based on selection
        selected_songs_data = {k: v for k, v in SONGS_DATA.items() if k in st.session_state.selected_songs}
        
        # Create an empty DataFrame with the same structure when no songs are selected
        if not selected_songs_data:
            songs_df = pd.DataFrame({
                'valence': [50],  # Add a dummy point in the middle
                'energy': [50],
                'danceability': [65],  # Middle of our color range
                'popularity': [0],  # Make it invisible
                'name': [''],
                'artist': ['']
            })
        else:
            songs_df = pd.DataFrame.from_dict(selected_songs_data, orient='index')
        
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
            range_x=[0, 100],
            range_y=[0, 100],
            range_color=[50, 80],
            title="Song Audio Features Visualization"
        )
        
        # Update layout for a cleaner look
        fig.update_layout(
            height=600,
            xaxis_title="Valence (Musical Positiveness)",
            yaxis_title="Energy",
            coloraxis_colorbar_title="Danceability",
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                linewidth=1,
                linecolor='black',
                range=[0, 100]
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                linewidth=1,
                linecolor='black',
                range=[0, 100]
            ),
            coloraxis=dict(
                colorbar=dict(
                    title="Danceability",
                    thickness=20,
                    len=0.8,
                    y=0.5,
                    yanchor="middle",
                    tickmode='array',
                    tickvals=[50, 60, 70, 80],
                    ticktext=['50', '60', '70', '80'],
                    ticks="outside"
                )
            )
        )
        
        # Add play/pause button annotations only if there are selected songs
        if selected_songs_data:
            for i, (song_id, song) in enumerate(selected_songs_data.items()):
                is_playing = st.session_state.playing_song == song_id
                icon = "⏸️" if is_playing else "▶️"
                fig.add_annotation(
                    x=song['valence'],
                    y=song['energy'],
                    text=icon,
                    showarrow=False,
                    font=dict(size=20),
                    clicktoshow="onoff",
                    hovertext=f"{'Pause' if is_playing else 'Play'} {song['name']}",
                    xref="x",
                    yref="y"
                )
        else:
            # Add a message in the center of the plot when no songs are selected
            fig.add_annotation(
                x=50,
                y=50,
                text="Select songs from the list to visualize them here!",
                showarrow=False,
                font=dict(size=16, color="gray"),
                xref="x",
                yref="y"
            )
            # Make the dummy point invisible
            fig.update_traces(
                marker=dict(
                    size=0,
                    opacity=0
                ),
                selector=dict(name='')
            )
        
        # Display the plot
        st.plotly_chart(fig, use_container_width=True)
    
    # Always show all songs at the bottom
    st.markdown("---")
    st.header("Song Controls")
    st.write("Click the buttons below to play/pause songs:")
    
    # Create a grid of buttons for all songs
    num_cols = 3  # Number of columns in the grid
    cols = st.columns(num_cols)
    
    for i, (song_id, song) in enumerate(SONGS_DATA.items()):
        with cols[i % num_cols]:
            is_playing = st.session_state.playing_song == song_id
            if st.button(
                f"{'⏸️ Pause' if is_playing else '▶️ Play'} {song['name']}",
                key=f"play_{song_id}"
            ):
                toggle_play(song_id)
                st.rerun()
    
    # Handle song playback
    if st.session_state.playing_song:
        song = SONGS_DATA[st.session_state.playing_song]
        st.audio(song['audio_file'])
    
    # Data source information
    st.markdown("---")
    st.markdown("### Data Source")
    st.markdown("The song data is from the Kaggle dataset: [Top 50 Spotify Songs - 2019](https://www.kaggle.com/datasets/leonardopena/top50spotify2019)")

if __name__ == "__main__":
    main() 