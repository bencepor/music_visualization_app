import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page config
st.set_page_config(
    page_title="Music Visualization App",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add custom CSS for creative design
st.markdown("""
<style>
/* ==================== */
/* Global Styles      */
/* ==================== */

/* Import modern fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap');

/* Modern color scheme (CSS Variables) */
:root {
    --primary-color: #7C3AED;  /* Vibrant purple */
    --secondary-color: #4F46E5; /* Indigo */
    --accent-color: #EC4899;   /* Pink */
    --text-color: #1F2937;    
    --background-color: #F9FAFB;
    --card-background: #FFFFFF;
    --hover-color: #F3F4F6;
    --selected-color: #EDE9FE;
    --gradient-start: #7C3AED;
    --gradient-end: #4F46E5;
}

/* Base font application */
* {
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
}

/* Basic body padding/margin */
body {
    margin: 0;
    padding: 0;
    background-color: var(--background-color);
    font-family: 'Inter', sans-serif;
}

/* General heading styles */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif;
    color: var(--text-color);
}

/* Specific H2 override for general style */
h2 {
    font-weight: 500;
}

/* Subtitle styling - more specific to override h2 */
.center-container h2.subtitle {
    font-size: 1.8rem;
    font-weight: 500;
    color: var(--text-color);
    font-family: "Space Grotesk", sans-serif;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.4;
    text-align: center;
    width: 100%;
}

/* Info text styling */
.info-text {
    color: #6B7280;
    font-size: 0.9rem;
    font-style: italic;
    font-family: 'Inter', sans-serif;
}

/* Focus styles for accessibility */
button:focus, a:focus {
    outline: 2px solid var(--primary-color);
    outline-offset: 2px;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--background-color);
}

::-webkit-scrollbar-thumb {
    background: var(--primary-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--secondary-color);
}

/* ==================== */
/* Header Styles      */
/* ==================== */

/* Main title styling with gradient and underline */
h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 3.5rem;
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-transform: uppercase;
    letter-spacing: -0.02em;
    position: relative;
    display: inline-block;
    padding: 0;
}

/* Underline for the main title */
h1::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    height: 4px;
    background: linear-gradient(90deg, transparent, var(--gradient-start), var(--gradient-end), transparent);
    border-radius: 2px;
}

/* Long horizontal divider line */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--primary-color), transparent);
}

/* ======================== */
/* Section Header Styles  */
/* ======================== */

/* Base section header styling */
.section-header {
    border-bottom: none;
    position: relative;
    display: inline-block;
}

/* Underline for section headers */
.section-header::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: var(--primary-color);
    border-radius: 1px;
}

/* Custom header styling */
.custom-header {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 500;
    color: var(--text-color);
    font-size: 2rem;
    margin: 2rem 0 1.5rem 0;
    width: 100%;
    position: relative;
}

.custom-header::after {
    content: '';
    position: absolute;
    bottom: -0.1rem;
    left: 0;
    width: 100%;
    height: 2px;
    background: var(--primary-color);
    border-radius: 1px;
}

/* ==================== */
/* Card & Button Styles */
/* ==================== */

/* Styling for buttons that look like cards */
.stButton button {
    width: 100%;
    text-align: left;
    background: var(--card-background);
    border: 1px solid #E5E7EB;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 12px;
    cursor: pointer;
    color: var(--text-color);
    font-size: 1rem;
    line-height: 1.5;
    transition: all 0.3s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.stButton button:hover {
    background-color: var(--hover-color);
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* Song item styling */
.song-item {
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    background: var(--card-background);
    border: 1px solid #E5E7EB;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.song-item:hover {
    background-color: var(--hover-color);
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* Styling for selected song item */
.song-item.selected {
    background-color: var(--selected-color);
    border-left: 4px solid var(--primary-color);
}

/* Play/Pause button styling */
.play-button {
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.play-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* ==================== */
/* Layout Styles      */
/* ==================== */

/* Center container */
.center-container {
    text-align: center;
}

/* Footer styling */
.footer {
    text-align: center;
    margin-top: 3rem;
    padding: 2rem;
    background: var(--card-background);
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.footer h3 {
    color: var(--primary-color);
    margin-bottom: 1rem;
}

.footer a {
    color: var(--primary-color);
    text-decoration: none;
}

/* Now playing container */
.now-playing {
    background: var(--card-background);
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.now-playing p {
    margin: 0;
}

/* ==================== */
/* Utility Classes    */
/* ==================== */

/* Class to remove default h2 border */
.no-underline h2 {
    border-bottom: none !important;
}

/* Note: .full-width-underline and .player-divider classes from previous iterations are kept but could be refactored/removed if not used. .custom-header also exists. Review usage in Python code. */

</style>
""", unsafe_allow_html=True)

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
    # Creative header with gradient
    st.markdown("""
    <div class="center-container">
        <h1>Music Explorer</h1>
        <h2 class="subtitle">Discover the emotional landscape of your favorite songs</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<hr>""", unsafe_allow_html=True)

    # Create two columns with custom styling
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <h2 class='section-header'>Your Playlist</h2>
        """, unsafe_allow_html=True)
        
        # Display song list with custom styling
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
        st.markdown("""
        <h2 class='section-header'>Emotional Map</h2>
        <p class='info-text'>Explore how your songs relate to each other in terms of energy, mood, and danceability</p>
        """, unsafe_allow_html=True)
        
        # Filter songs based on selection
        selected_songs_data = {k: v for k, v in SONGS_DATA.items() if k in st.session_state.selected_songs}
        
        # Create an empty DataFrame with the same structure when no songs are selected
        if not selected_songs_data:
            songs_df = pd.DataFrame({
                'valence': [50],
                'energy': [50],
                'danceability': [65],
                'popularity': [0],
                'name': [''],
                'artist': ['']
            })
        else:
            songs_df = pd.DataFrame.from_dict(selected_songs_data, orient='index')
        
        # Create the scatter plot with Plotly using creative styling
        fig = px.scatter(
            songs_df,
            x="valence",
            y="energy",
            color="danceability",
            size="popularity",
            hover_name="name",
            hover_data=["artist", "danceability", "popularity"],
            color_continuous_scale=px.colors.sequential.Viridis,
            size_max=40,
            range_x=[0, 100],
            range_y=[0, 100],
            range_color=[50, 80],
            title=""
        )
        
        # Update layout for creative design
        fig.update_layout(
            height=600,
            xaxis_title="Valence (Musical Positiveness)",
            yaxis_title="Energy",
            coloraxis_colorbar_title="Danceability",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(
                family="Inter, sans-serif",
                size=14,
                color="#1F2937"
            ),
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                linewidth=1,
                linecolor='#1F2937',
                range=[0, 100],
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                linewidth=1,
                linecolor='#1F2937',
                range=[0, 100],
                tickfont=dict(size=12)
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
                    ticks="outside",
                    tickfont=dict(size=12)
                )
            )
        )
        
        # Update marker size range to focus on the narrow popularity range (87-95)
        fig.update_traces(
            marker=dict(
                sizemode='area',
                sizeref=2.*max(songs_df['popularity'])/(40.**2),
                sizemin=15
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
            # Add a creative message in the center of the plot
            fig.add_annotation(
                x=50,
                y=50,
                text="Select songs to start your musical journey!",
                showarrow=False,
                font=dict(size=16, color="#4B5563"),
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
        
    # Player controls with creative styling
    st.markdown("""
    <h2 class="custom-header">Player Controls</h2>
    """, unsafe_allow_html=True)
    st.markdown("""<p class='info-text'>Take control of your musical experience</p>""", unsafe_allow_html=True)
    
    # Create a grid of buttons for all songs
    num_cols = 3
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
    
    # Handle song playback with custom styling
    if st.session_state.playing_song:
        song = SONGS_DATA[st.session_state.playing_song]
        st.markdown("""
        <div class="now-playing">
            <p><strong>Now Playing:</strong> {}</p>
        </div>
        """.format(song['name']), unsafe_allow_html=True)
        st.audio(song['audio_file'])
    
    # Footer with creative styling
    st.markdown("""
    <div class="footer">
        <h3>About the Data</h3>
        <p class='info-text'>Song data sourced from the <a href='https://www.kaggle.com/datasets/leonardopena/top50spotify2019'>Top 50 Spotify Songs - 2019</a> dataset</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 