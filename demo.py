"""
Demo Spotify Recommendation Engine - Works without Premium!

This version uses sample data to demonstrate the recommendation algorithm
without requiring Spotify API access or Premium subscription.
"""

from recommendation_engine import SpotifyRecommendationEngine
import pandas as pd
from typing import List, Dict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler


def create_demo_data():
    """Create sample track data for demonstration."""
    # Sample tracks with audio features (based on real Spotify data)
    demo_tracks = [
        {
            'id': 'demo_001',
            'name': 'Blinding Lights',
            'artists': ['The Weeknd'],
            'album': 'After Hours',
            'popularity': 95,
            'acousticness': 0.00146,
            'danceability': 0.514,
            'energy': 0.730,
            'instrumentalness': 0.00146,
            'key': 1,
            'liveness': 0.0897,
            'loudness': -5.934,
            'mode': 1,
            'speechiness': 0.0598,
            'tempo': 171.005,
            'valence': 0.334
        },
        {
            'id': 'demo_002',
            'name': 'Watermelon Sugar',
            'artists': ['Harry Styles'],
            'album': 'Fine Line',
            'popularity': 88,
            'acousticness': 0.122,
            'danceability': 0.548,
            'energy': 0.816,
            'instrumentalness': 0.000001,
            'key': 0,
            'liveness': 0.335,
            'loudness': -4.209,
            'mode': 1,
            'speechiness': 0.0465,
            'tempo': 95.390,
            'valence': 0.557
        },
        {
            'id': 'demo_003',
            'name': 'Levitating',
            'artists': ['Dua Lipa'],
            'album': 'Future Nostalgia',
            'popularity': 89,
            'acousticness': 0.0561,
            'danceability': 0.695,
            'energy': 0.884,
            'instrumentalness': 0.000001,
            'key': 6,
            'liveness': 0.213,
            'loudness': -2.278,
            'mode': 0,
            'speechiness': 0.0753,
            'tempo': 103.014,
            'valence': 0.914
        },
        {
            'id': 'demo_004',
            'name': 'Good 4 U',
            'artists': ['Olivia Rodrigo'],
            'album': 'SOUR',
            'popularity': 87,
            'acousticness': 0.335,
            'danceability': 0.563,
            'energy': 0.664,
            'instrumentalness': 0.000001,
            'key': 9,
            'liveness': 0.0849,
            'loudness': -5.044,
            'mode': 1,
            'speechiness': 0.154,
            'tempo': 166.928,
            'valence': 0.688
        },
        {
            'id': 'demo_005',
            'name': 'Stay',
            'artists': ['The Kid Laroi', 'Justin Bieber'],
            'album': 'F*CK LOVE 3: OVER YOU',
            'popularity': 92,
            'acousticness': 0.0383,
            'danceability': 0.591,
            'energy': 0.764,
            'instrumentalness': 0.000001,
            'key': 1,
            'liveness': 0.103,
            'loudness': -5.484,
            'mode': 1,
            'speechiness': 0.0483,
            'tempo': 169.928,
            'valence': 0.478
        },
        {
            'id': 'demo_006',
            'name': 'Peaches',
            'artists': ['Justin Bieber', 'Daniel Caesar', 'Giveon'],
            'album': 'Justice',
            'popularity': 85,
            'acousticness': 0.321,
            'danceability': 0.677,
            'energy': 0.696,
            'instrumentalness': 0.000001,
            'key': 0,
            'liveness': 0.420,
            'loudness': -6.181,
            'mode': 1,
            'speechiness': 0.119,
            'tempo': 90.030,
            'valence': 0.464
        },
        {
            'id': 'demo_007',
            'name': 'Drivers License',
            'artists': ['Olivia Rodrigo'],
            'album': 'SOUR',
            'popularity': 86,
            'acousticness': 0.721,
            'danceability': 0.561,
            'energy': 0.431,
            'instrumentalness': 0.000001,
            'key': 10,
            'liveness': 0.106,
            'loudness': -8.810,
            'mode': 1,
            'speechiness': 0.0578,
            'tempo': 143.875,
            'valence': 0.137
        },
        {
            'id': 'demo_008',
            'name': 'As It Was',
            'artists': ['Harry Styles'],
            'album': "Harry's House",
            'popularity': 91,
            'acousticness': 0.342,
            'danceability': 0.520,
            'energy': 0.731,
            'instrumentalness': 0.00101,
            'key': 6,
            'liveness': 0.311,
            'loudness': -5.338,
            'mode': 0,
            'speechiness': 0.0557,
            'tempo': 173.930,
            'valence': 0.662
        }
    ]

    return demo_tracks


def demo_recommendations():
    """Demonstrate the recommendation engine with sample data."""
    print("🎵 DEMO: Spotify Song Recommendation Engine")
    print("=" * 60)
    print("This demo works without Spotify Premium or API access!")
    print("Using sample data to show the recommendation algorithm.\n")

    # Create demo data
    demo_tracks = create_demo_data()

    # Initialize engine with mock data
    engine = SpotifyRecommendationEngine(demo_mode=True)

    # Manually set track features for demo
    features_data = []
    for track in demo_tracks:
        features_data.append({
            'id': track['id'],
            'acousticness': track['acousticness'],
            'danceability': track['danceability'],
            'energy': track['energy'],
            'instrumentalness': track['instrumentalness'],
            'key': track['key'],
            'liveness': track['liveness'],
            'loudness': track['loudness'],
            'mode': track['mode'],
            'speechiness': track['speechiness'],
            'tempo': track['tempo'],
            'valence': track['valence']
        })

    engine.track_features = pd.DataFrame(features_data)

    print("✓ Loaded demo track database with 8 popular songs")
    print("✓ Initialized recommendation algorithm\n")

    # Demonstrate recommendations for different tracks
    demo_seeds = [
        ('demo_001', 'Blinding Lights - The Weeknd'),
        ('demo_002', 'Watermelon Sugar - Harry Styles'),
        ('demo_004', 'Good 4 U - Olivia Rodrigo')
    ]

    for track_id, track_name in demo_seeds:
        print(f"🎯 Finding songs similar to: {track_name}")
        try:
            # Use demo-specific similarity calculation
            recommendations = demo_find_similar_tracks(engine, track_id, demo_tracks, limit=3)
            engine.print_recommendations(recommendations)

        except Exception as e:
            print(f"❌ Error generating recommendations: {str(e)}\n")

    print("🎉 Demo completed successfully!")
    print("\n💡 To use with real Spotify data:")
    print("   1. Get Spotify Premium on the app owner account")
    print("   2. Or create the app under a Premium account")
    print("   3. Run: python3 example.py")


def demo_find_similar_tracks(engine, track_id: str, demo_tracks: List[Dict], limit: int = 10) -> List[Dict]:
    """
    Demo version of find_similar_tracks that works without Spotify API.
    """
    if engine.track_features.empty:
        raise ValueError("No track features available. Call get_track_features() first.")

    if track_id not in engine.track_features['id'].values:
        raise ValueError(f"Track ID {track_id} not found in feature data.")

    # Get features for the target track
    target_track = engine.track_features[engine.track_features['id'] == track_id].iloc[0]
    target_features = target_track.drop('id').values.reshape(1, -1)

    # Normalize all features using a local scaler
    scaler = StandardScaler()
    feature_columns = engine.track_features.columns.drop('id')
    normalized_features = scaler.fit_transform(
        engine.track_features[feature_columns]
    )
    normalized_target = scaler.transform(target_features)

    # Calculate cosine similarity
    similarities = cosine_similarity(normalized_target, normalized_features)[0]

    # Get top similar tracks (excluding the query track itself)
    similar_indices = np.argsort(similarities)[::-1][1:limit+1]
    similar_track_ids = engine.track_features.iloc[similar_indices]['id'].tolist()

    # Create recommendations using demo track data
    recommendations = []
    for i, track_id in enumerate(similar_track_ids):
        track_info = next((t for t in demo_tracks if t['id'] == track_id), None)
        if track_info:
            recommendations.append({
                'id': track_id,
                'name': track_info['name'],
                'artists': track_info['artists'],
                'album': track_info['album'],
                'popularity': track_info['popularity'],
                'similarity_score': similarities[similar_indices[i]]
            })

    return recommendations


if __name__ == "__main__":
    demo_recommendations()