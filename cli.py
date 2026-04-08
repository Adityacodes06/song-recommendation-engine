"""
CLI Interface for Spotify Recommendation Engine
"""

import os
from dotenv import load_dotenv
import argparse
from recommendation_engine import SpotifyRecommendationEngine


def main():
    """Main CLI entry point."""
    
    load_dotenv()
    
    parser = argparse.ArgumentParser(
        description='Spotify Song Recommendation Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Recommend songs based on user's listening history
  python cli.py --user-id spotify_user_id --output recommendations.txt
  
  # Find similar songs to a specific track
  python cli.py --track-id spotify_track_id --similar --limit 20
        """
    )
    
    parser.add_argument(
        '--user-id',
        type=str,
        help='Spotify user ID to generate recommendations for'
    )
    parser.add_argument(
        '--track-id',
        type=str,
        help='Spotify track ID to find similar songs for'
    )
    parser.add_argument(
        '--similar',
        action='store_true',
        help='Find similar tracks instead of user recommendations'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Number of recommendations to generate (default: 10)'
    )
    parser.add_argument(
        '--time-range',
        choices=['short_term', 'medium_term', 'long_term'],
        default='medium_term',
        help='Time range for user top tracks'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Save recommendations to a file'
    )
    
    args = parser.parse_args()
    
    # Get API credentials from environment
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ Error: Missing Spotify API credentials")
        print("\nPlease set the following environment variables:")
        print("  - SPOTIFY_CLIENT_ID")
        print("  - SPOTIFY_CLIENT_SECRET")
        print("\nYou can create a .env file in the current directory:")
        print("""
  SPOTIFY_CLIENT_ID=your_client_id
  SPOTIFY_CLIENT_SECRET=your_client_secret
        """)
        return
    
    try:
        # Initialize recommendation engine
        print("🎵 Initializing Spotify Recommendation Engine...")
        engine = SpotifyRecommendationEngine(client_id, client_secret)
        
        recommendations = []
        
        if args.similar and args.track_id:
            # Find similar tracks
            print(f"\n🔍 Finding {args.limit} songs similar to track ID: {args.track_id}")
            
            # First, fetch the track features
            engine.get_track_features([args.track_id])
            
            # Then find similar tracks for other songs (we need to fetch more data)
            all_tracks = engine.sp.search(q='track', type='track', limit=50)['tracks']['items']
            all_track_ids = [t['id'] for t in all_tracks]
            engine.get_track_features(all_track_ids)
            
            recommendations = engine.find_similar_tracks(args.track_id, limit=args.limit)
        
        elif args.user_id:
            # Generate recommendations based on user
            print(f"\n👤 Generating recommendations for user: {args.user_id}")
            print(f"   Using {args.time_range} listening history...")
            
            recommendations = engine.recommend_based_on_user(
                args.user_id,
                num_recommendations=args.limit
            )
        
        else:
            print("❌ Error: Please provide either --user-id or --track-id with --similar")
            parser.print_help()
            return
        
        # Display recommendations
        engine.print_recommendations(recommendations)
        
        # Save to file if requested
        if args.output and recommendations:
            try:
                with open(args.output, 'w') as f:
                    f.write("SPOTIFY SONG RECOMMENDATIONS\n")
                    f.write("="*80 + "\n\n")
                    
                    for i, track in enumerate(recommendations, 1):
                        artists = ", ".join(track.get('artists', ['Unknown']))
                        album = track.get('album', 'Unknown Album')
                        popularity = track.get('popularity', 0)
                        similarity = track.get('similarity_score', 0)
                        
                        f.write(f"{i}. {track['name']}\n")
                        f.write(f"   Artists: {artists}\n")
                        f.write(f"   Album: {album}\n")
                        f.write(f"   Popularity: {popularity}/100\n")
                        if similarity:
                            f.write(f"   Similarity Score: {similarity:.2%}\n")
                        f.write("\n")
                
                print(f"✓ Recommendations saved to {args.output}")
            except Exception as e:
                print(f"❌ Error saving to file: {str(e)}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return


if __name__ == '__main__':
    main()
