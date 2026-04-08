"""
Spotify Song Recommendation Engine using Collaborative Filtering
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Tuple
import warnings

warnings.filterwarnings('ignore')


class SpotifyRecommendationEngine:
    """
    A collaborative filtering-based recommendation engine for Spotify songs.
    Uses user listening history and track audio features to recommend similar songs.
    """
    
    def __init__(self, client_id: str = None, client_secret: str = None, sp_client=None, demo_mode: bool = False):
        """
        Initialize the recommendation engine with Spotify API credentials or an existing Spotify client.
        
        Args:
            client_id: Spotify API client ID
            client_secret: Spotify API client secret
            sp_client: Existing Spotipy client instance (e.g. SpotifyOAuth)
            demo_mode: If True, allows initialization without Spotify credentials for demo purposes
        """
        try:
            if demo_mode:
                self.sp = None  # No Spotify client in demo mode
            elif sp_client is not None:
                self.sp = sp_client
            elif client_id and client_secret:
                auth_manager = SpotifyClientCredentials(
                    client_id=client_id,
                    client_secret=client_secret
                )
                self.sp = spotipy.Spotify(auth_manager=auth_manager)
            else:
                raise ValueError("Either sp_client, client_id/client_secret, or demo_mode=True must be provided.")
            self.user_tracks = []
            self.track_features = pd.DataFrame()
            self.scaler = StandardScaler()
        except Exception as e:
            raise Exception(f"Failed to initialize Spotify API: {str(e)}")
    
    def get_user_top_tracks(self, limit: int = 50, 
                           time_range: str = "medium_term") -> List[Dict]:
        """
        Fetch the current user's top played tracks from Spotify.
        
        Args:
            limit: Number of top tracks to fetch (max 50)
            time_range: 'long_term', 'medium_term', or 'short_term'
            
        Returns:
            List of track dictionaries
        """
        try:
            if hasattr(self.sp, 'current_user_top_tracks'):
                results = self.sp.current_user_top_tracks(limit=limit, time_range=time_range)
            elif hasattr(self.sp, 'user_top_tracks'):
                results = self.sp.user_top_tracks(limit=limit, time_range=time_range)
            else:
                raise AttributeError('Spotify client does not support user top tracks.')
            
            tracks = results.get('items', [])
            self.user_tracks = [
                {
                    'id': track['id'],
                    'name': track['name'],
                    'artists': [artist['name'] for artist in track['artists']],
                    'popularity': track['popularity'],
                    'uri': track['uri']
                }
                for track in tracks
            ]
            
            print(f"✓ Fetched {len(self.user_tracks)} top tracks")
            return self.user_tracks
            
        except Exception as e:
            print(f"Error fetching user top tracks: {str(e)}")
            return []
    
    def get_track_features(self, track_ids: List[str]) -> pd.DataFrame:
        """
        Fetch audio features for given track IDs.
        
        Args:
            track_ids: List of Spotify track IDs
            
        Returns:
            DataFrame with audio features for each track
        """
        features_list = []
        
        # Fetch features in batches (API limit: 100 tracks per request)
        for i in range(0, len(track_ids), 100):
            batch = track_ids[i:i+100]
            try:
                features = self.sp.audio_features(batch)
                if features:
                    features_list.extend(features)
                else:
                    print(f"Warning: No features returned for batch {i//100 + 1}")
            except Exception as e:
                error_msg = str(e)
                if 'Premium' in error_msg or 'Active premium subscription required' in error_msg:
                    print("❌ Audio features require a Spotify Premium account or app approval.")
                    print("This is a limitation of the current Spotify app configuration.")
                else:
                    print(f"Error fetching features for batch {i//100 + 1}: {error_msg}")
        
        # Create DataFrame with relevant audio features
        features_data = []
        for feature in features_list:
            if feature:
                features_data.append({
                    'id': feature['id'],
                    'acousticness': feature['acousticness'],
                    'danceability': feature['danceability'],
                    'energy': feature['energy'],
                    'instrumentalness': feature['instrumentalness'],
                    'key': feature['key'],
                    'liveness': feature['liveness'],
                    'loudness': feature['loudness'],
                    'mode': feature['mode'],
                    'speechiness': feature['speechiness'],
                    'tempo': feature['tempo'],
                    'valence': feature['valence']
                })
        
        self.track_features = pd.DataFrame(features_data)
        if not features_data:
            print("❌ No audio features could be fetched. This may be due to API restrictions.")
        else:
            print(f"✓ Fetched audio features for {len(features_data)} tracks")
        return self.track_features
    
    def find_similar_tracks(self, track_id: str, limit: int = 10) -> List[Dict]:
        """
        Find similar tracks using collaborative filtering based on audio features.
        
        Args:
            track_id: Spotify track ID to find similar tracks for
            limit: Number of recommendations to return
            
        Returns:
            List of similar track recommendations
        """
        if self.track_features.empty:
            raise ValueError("No track features available. Call get_track_features() first.")
        
        if track_id not in self.track_features['id'].values:
            raise ValueError(f"Track ID {track_id} not found in feature data.")
        
        # Get features for the target track
        target_track = self.track_features[self.track_features['id'] == track_id].iloc[0]
        target_features = target_track.drop('id').values.reshape(1, -1)
        
        # Normalize all features
        feature_columns = self.track_features.columns.drop('id')
        normalized_features = self.scaler.fit_transform(
            self.track_features[feature_columns]
        )
        normalized_target = self.scaler.transform(target_features)
        
        # Calculate cosine similarity
        similarities = cosine_similarity(normalized_target, normalized_features)[0]
        
        # Get top similar tracks (excluding the query track itself)
        similar_indices = np.argsort(similarities)[::-1][1:limit+1]
        similar_track_ids = self.track_features.iloc[similar_indices]['id'].tolist()
        
        # Fetch track info for recommendations
        recommendations = []
        try:
            tracks_info = self.sp.tracks(similar_track_ids)
            for track in tracks_info['tracks']:
                recommendations.append({
                    'id': track['id'],
                    'name': track['name'],
                    'artists': [artist['name'] for artist in track['artists']],
                    'album': track['album']['name'],
                    'popularity': track['popularity'],
                    'similarity_score': similarities[
                        np.where(self.track_features['id'] == track['id'])[0][0]
                    ]
                })
        except Exception as e:
            print(f"Error fetching track info: {str(e)}")
        
        return recommendations
    
    def recommend_from_seed_track(self, track_id: str, limit: int = 10, country: str = 'US') -> List[Dict]:
        """
        Generate recommendations based on a seed track using Spotify's recommendations endpoint.
        
        Args:
            track_id: Spotify track ID to use as the recommendation seed
            limit: Number of recommended tracks to return
            country: Country code for recommendations
            
        Returns:
            List of recommended tracks
        """
        try:
            results = self.sp.recommendations(seed_tracks=[track_id], limit=limit, country=country)
            recommendations = []
            for track in results.get('tracks', []):
                recommendations.append({
                    'id': track['id'],
                    'name': track['name'],
                    'artists': [artist['name'] for artist in track['artists']],
                    'album': track['album']['name'],
                    'popularity': track.get('popularity', 0),
                    'similarity_score': None
                })
            return recommendations
        except Exception as e:
            error_message = str(e)
            if 'Active premium subscription required' in error_message:
                print("Error: Spotify API access is blocked by your developer account settings.")
                print("This usually means the owner account needs an active Premium subscription or app approval.")
                print("Try creating the Spotify app under a different account or enable Premium on the current account.")
            elif 'http status: 404' in error_message:
                print("Error: Spotify recommendations endpoint returned 404.")
                print("This often means the current Spotify app is not authorized to use this endpoint.")
                print("Check your Spotify Developer Dashboard, app settings, and account status.")
            else:
                print(f"Error generating recommendations from seed track: {error_message}")
            return []
    
    def recommend_based_on_user(self, num_recommendations: int = 10) -> List[Dict]:
        """
        Generate recommendations based on the current authenticated user's top tracks.

        Requires SpotifyOAuth authorization with the user-top-read scope.
        """
        user_tracks = self.get_user_top_tracks(limit=min(50, num_recommendations * 3))
        if not user_tracks:
            print("❌ Could not fetch user top tracks. Check your Spotify account and permissions.")
            return []
        
        track_ids = [track['id'] for track in user_tracks]
        
        # Try to get track features
        self.get_track_features(track_ids)
        
        # Check if we successfully got track features
        if self.track_features.empty:
            print("❌ Could not fetch audio features for tracks.")
            print("This might be due to API restrictions or rate limiting.")
            print("Falling back to basic recommendations...")
            
            # Fallback: Return some of the user's top tracks as "recommendations"
            fallback_recommendations = []
            for track in user_tracks[:num_recommendations]:
                fallback_recommendations.append({
                    'id': track['id'],
                    'name': track['name'],
                    'artists': track['artists'],
                    'album': track['album'],
                    'popularity': track['popularity'],
                    'similarity_score': None
                })
            return fallback_recommendations
        
        recommendations = []
        seen_ids = set(track_ids)
        
        for track_id in track_ids[:5]:
            try:
                similar = self.find_similar_tracks(track_id, limit=num_recommendations)
                for track in similar:
                    if track['id'] not in seen_ids:
                        recommendations.append(track)
                        seen_ids.add(track['id'])
            except Exception as e:
                print(f"Warning: Could not find similar tracks for {track_id}: {str(e)}")
                continue
        
        recommendations.sort(key=lambda x: x.get('similarity_score', 0), reverse=True)
        return recommendations[:num_recommendations]
    
    def print_recommendations(self, recommendations: List[Dict]) -> None:
        """Pretty print recommendations."""
        if not recommendations:
            print("No recommendations found.")
            return
        
        print("\n" + "="*80)
        print("🎵 SPOTIFY SONG RECOMMENDATIONS")
        print("="*80)
        
        for i, track in enumerate(recommendations, 1):
            artists = ", ".join(track.get('artists', ['Unknown']))
            album = track.get('album', 'Unknown Album')
            popularity = track.get('popularity', 0)
            similarity = track.get('similarity_score', 0)
            
            print(f"\n{i}. {track['name']}")
            print(f"   Artists: {artists}")
            print(f"   Album: {album}")
            print(f"   Popularity: {popularity}/100")
            if similarity:
                print(f"   Similarity Score: {similarity:.2%}")
        
        print("\n" + "="*80 + "\n")
