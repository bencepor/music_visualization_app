# Music Visualization App

An interactive 2D web-based visualization that maps songs according to their acoustic and emotional characteristics, using local audio files and pre-defined song data.

## Features

- Visualize songs on a scatter plot with:
  - x-axis: valence (musical positiveness)
  - y-axis: energy
  - color: danceability
  - size: popularity
- Play audio files directly in the browser
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

3. **Run the application**

```bash
streamlit run app.py
```

The app will be available at [http://localhost:8501](http://localhost:8501).

## Usage

1. **Explore the visualization**: Hover over data points to see song details
2. **Listen to songs**: Scroll down to the songs list to play audio files

## How It Works

The app uses pre-defined song data from the Kaggle dataset "Top 50 Spotify Songs - 2019" and local audio files. The visualization shows:

- **Valence**: Musical positiveness (0.0 to 1.0)
- **Energy**: Intensity and activity (0.0 to 1.0)
- **Danceability**: How suitable a track is for dancing (0.0 to 1.0)
- **Popularity**: The song's popularity on Spotify (0 to 100)

## Data Source

The song data is from the Kaggle dataset: [Top 50 Spotify Songs - 2019](https://www.kaggle.com/datasets/leonardopena/top50spotify2019)

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
