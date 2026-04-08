"""
Example usage of Spotify Recommendation Engine

This script demonstrates how to use the recommendation engine
to get song recommendations based on user listening history.
"""

from recommendation_engine import SpotifyRecommendationEngine
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def example_user_recommendations():
    """
    Example: Get recommendations based on the authenticated user's top tracks.
    """
    
    # Load environment variables from .env file
    load_dotenv()
    
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')
    scope = os.getenv('SPOTIFY_SCOPE', 'user-top-read')
    
    if not client_id or not client_secret:
        print("❌ Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env file")
        return
    
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    engine = SpotifyRecommendationEngine(sp_client=sp)
    
    # Fetch recommendations for the authenticated Spotify user
    recommendations = engine.recommend_based_on_user(num_recommendations=10)
    
    engine.print_recommendations(recommendations)
    
    return recommendations


def example_track_recommendations():
    """
    Example: Find similar tracks to a given song
    """
    
    load_dotenv()
    
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env file")
        return
    
    # Initialize the engine
    engine = SpotifyRecommendationEngine(client_id, client_secret)
    
    # Example track ID (Blinding Lights - The Weeknd)
    track_id = "0VjIjW4GlUZAMYd2vXMwbY"
    
    # Search and fetch features
    print("Fetching audio features for similar track analysis...")
    search_results = engine.sp.search(q='song', type='track', limit=100)
    track_ids = [t['id'] for t in search_results['tracks']['items']]
    
    # Add the target track
    track_ids.insert(0, track_id)
    engine.get_track_features(track_ids)
    
    # Find similar tracks
    recommendations = engine.find_similar_tracks(track_id, limit=10)
    
    print(f"\n🎵 Songs similar to: Blinding Lights")
    engine.print_recommendations(recommendations)
    
    return recommendations


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "seed":
        print("Running seed-track recommendations example...")
        print("\n📝 Note: You can change the track_id inside example.py to a song you like.\n")
        example_track_recommendations()
    elif len(sys.argv) > 1 and sys.argv[1] == "similar":
        print("Running similar tracks example...")
        example_similar_tracks()
    else:
        print("Running user-based recommendations example...")
        print("\n📝 Note: This will open a browser so you can sign in with your Spotify account.\n")
        example_user_recommendations()
