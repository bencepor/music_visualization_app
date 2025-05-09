# Music Visualization App

An interactive 2D web-based visualization that maps songs according to their acoustic and emotional characteristics, using data accessed through the Spotify API.

## Features

- Visualize songs on a scatter plot with:
  - x-axis: valence (musical positiveness)
  - y-axis: energy
  - color: danceability
  - size: popularity
- Add new songs by pasting Spotify links
- Click on songs to hear audio previews (when available)
- View detailed track information

## Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/music_visualization_app.git
cd music_visualization_app
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up Spotify API credentials**

Create a Spotify Developer account at [developer.spotify.com](https://developer.spotify.com) and create a new application to get your API credentials.

Copy the `.env.example` file to `.env` and add your Spotify credentials:

```bash
cp .env.example .env
```

Edit the `.env` file and fill in your credentials:

```
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8501
```

4. **Run the application**

```bash
streamlit run app.py
```

The app will be available at [http://localhost:8501](http://localhost:8501).

## Usage

1. **Add songs**: Paste a Spotify track link, URI, or ID in the sidebar and click "Add Song"
2. **Explore the visualization**: Hover over data points to see song details
3. **Listen to previews**: Scroll down to the songs list to play audio previews

## How It Works

The app uses the Spotify API to retrieve audio features for tracks. These features are calculated by Spotify and include:

- **Valence**: Musical positiveness (0.0 to 1.0)
- **Energy**: Intensity and activity (0.0 to 1.0)
- **Danceability**: How suitable a track is for dancing (0.0 to 1.0)
- **Popularity**: The song's popularity on Spotify (0 to 100)

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
