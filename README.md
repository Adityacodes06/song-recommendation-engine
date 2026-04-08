# 🎵 Spotify Song Recommendation Engine

A collaborative filtering-based recommendation engine that suggests songs based on Spotify user listening history and audio features.

## Features

✨ **Collaborative Filtering**: Uses audio features and user listening patterns to find similar songs
🎼 **Audio Feature Analysis**: Analyzes 12 audio metrics (energy, danceability, valence, etc.)
👤 **User-Based Recommendations**: Generate personalized recommendations from user's top tracks
🔍 **Track Similarity**: Find songs similar to any Spotify track
📊 **Popularity Scoring**: Combines similarity scores with track popularity metrics
🖥️ **CLI Interface**: Easy command-line interface for quick recommendations

## Installation

### Prerequisites
- Python 3.8+
- Spotify Developer Account (free)

### Setup Steps

1. **Clone/Download the repository**
   ```bash
   cd "Square one"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get Spotify API credentials**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Log in or create a free account
   - Create a new app
   - Copy your **Client ID** and **Client Secret**

4. **Configure environment**
   ```bash
   # Copy the template
   cp .env.template .env
   
   # Edit .env and add your credentials
   # SPOTIFY_CLIENT_ID=your_id_here
   # SPOTIFY_CLIENT_SECRET=your_secret_here
   ```

## Usage

### Option 1: Using Python Script

```python
from recommendation_engine import SpotifyRecommendationEngine
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize engine
engine = SpotifyRecommendationEngine(
    os.getenv('SPOTIFY_CLIENT_ID'),
    os.getenv('SPOTIFY_CLIENT_SECRET')
)

# Get user recommendations
recommendations = engine.recommend_based_on_user(
    user_id="your_spotify_username",
    num_recommendations=10
)

# Display results
engine.print_recommendations(recommendations)
```

### Option 2: Using CLI

```bash
# Get recommendations for a user
python cli.py --user-id your_spotify_username --limit 10

# Find similar songs to a track
python cli.py --track-id 0VjIjW4GlUZAMYd2vXMwbY --similar --limit 15

# Save recommendations to file
python cli.py --user-id your_spotify_username --output recommendations.txt

# Use different time range
python cli.py --user-id your_spotify_username --time-range long_term
```

### Option 3: Running Examples

```bash
# User recommendations example
python dsjnd.py

# Similar tracks example
python dsjnd.py similar
```

## API Reference

### SpotifyRecommendationEngine Class

#### `__init__(client_id, client_secret)`
Initialize the engine with Spotify API credentials.

#### `get_user_top_tracks(user_id, limit=50, time_range="medium_term")`
Fetch a user's top played tracks.
- `time_range`: 'short_term' (4 weeks), 'medium_term' (6 months), 'long_term' (all time)

#### `get_track_features(track_ids)`
Fetch audio features for given track IDs.

#### `find_similar_tracks(track_id, limit=10)`
Find similar tracks using cosine similarity on audio features.

#### `recommend_based_on_user(user_id, num_recommendations=10)`
Generate personalized recommendations for a user.

#### `print_recommendations(recommendations)`
Pretty print recommendations to console.

## Audio Features Used

The recommendation engine analyzes these audio characteristics:

| Feature | Range | Description |
|---------|-------|-------------|
| Acousticness | 0-1 | Acoustic sound probability |
| Danceability | 0-1 | How suitable for dancing (beat stability, tempo) |
| Energy | 0-1 | Intensity and activity level |
| Instrumentalness | 0-1 | Predicted lack of vocals |
| Key | 0-11 | Musical key |
| Liveness | 0-1 | Presence of audience |
| Loudness | dB | Overall loudness |
| Mode | 0-1 | Major (1) or Minor (0) |
| Speechiness | 0-1 | Presence of spoken words |
| Tempo | BPM | Beats per minute |
| Valence | 0-1 | Musical positiveness (happy/sad) |

## How It Works

1. **Data Collection**
   - Fetches user's top tracks from Spotify API
   - Extracts audio features for each track

2. **Feature Normalization**
   - Standardizes all features to mean=0, std=1
   - Ensures equal weight across different scales

3. **Similarity Calculation**
   - Uses cosine similarity to compare audio feature vectors
   - Finds most similar tracks to user's preferences

4. **Ranking**
   - Ranks recommendations by similarity score
   - Factors in track popularity

## Example Output

```
================================================================================
🎵 SPOTIFY SONG RECOMMENDATIONS
================================================================================

1. Blinding Lights
   Artists: The Weeknd
   Album: After Hours
   Popularity: 95/100
   Similarity Score: 87.32%

2. Levitating
   Artists: Dua Lipa, DaBaby
   Album: Future Nostalgia (The Moonlight Edition)
   Popularity: 92/100
   Similarity Score: 84.67%

...
================================================================================
```

## Troubleshooting

### "Invalid credentials"
- Verify your Client ID and Secret are correct
- Check .env file formatting

### "User not found"
- Use your Spotify username (not display name)
- Ensure your profile is public

### "Track ID not found"
- Verify the track ID is valid
- Use Spotify search to find track IDs

### Rate Limiting
- Spotify API has rate limits
- Add delays between bulk requests if needed

## Project Structure

```
Square one/
├── dsjnd.py                      # Main example usage
├── recommendation_engine.py      # Core recommendation engine
├── cli.py                        # Command-line interface
├── requirements.txt              # Python dependencies
├── .env.template                 # Environment variables template
├── .env                          # Your credentials (create from template)
└── README.md                     # This file
```

## Algorithm Details

### Collaborative Filtering Approach
The engine uses **item-based collaborative filtering** with audio features:

1. **Feature Vector Creation**: Each track is represented as a 12-dimensional vector of audio features
2. **Normalization**: Features are standardized to prevent scale bias
3. **Similarity Metric**: Cosine similarity measures angle between feature vectors
4. **Ranking**: Similar songs are ranked by their similarity score

### Why Cosine Similarity?
- Robust to feature scaling differences
- Effective for high-dimensional audio data
- Fast computation for real-time recommendations
- Proven in music recommendation systems

## Performance Considerations

- Initial track feature fetch: ~1-2 seconds per 100 tracks
- Similarity calculation: O(n) where n = number of reference tracks
- Recommendation generation: Usually < 5 seconds for 50 tracks

## Future Enhancements

🚀 Potential improvements:
- User-user collaborative filtering
- Hybrid recommendation models
- Caching for frequently accessed data
- Web API with FastAPI
- Playlist generation
- Genre-specific recommendations
- Real-time Spotify integration

## License

MIT License - Feel free to use and modify

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Improve documentation
- Optimize algorithms

## Support

For issues or questions:
1. Check troubleshooting section
2. Review Spotify API documentation
3. Check feature examples in dsjnd.py

---

**Happy Recommending! 🎵**
