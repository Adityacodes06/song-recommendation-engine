"""
Test and validation script for Spotify Recommendation Engine

This script verifies that:
1. All dependencies are installed
2. Spotify API credentials are valid
3. The recommendation engine works correctly
"""

import os
import sys
from dotenv import load_dotenv


def check_dependencies():
    """Check if all required packages are installed."""
    print("📦 Checking dependencies...")
    
    required_packages = {
        'spotipy': 'Spotipy',
        'pandas': 'Pandas',
        'numpy': 'NumPy',
        'sklearn': 'Scikit-learn',
        'dotenv': 'python-dotenv'
    }
    
    missing = []
    for module, name in required_packages.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT INSTALLED")
            missing.append(name)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✓ All dependencies installed!\n")
    return True


def check_credentials():
    """Check if Spotify API credentials are configured."""
    print("🔐 Checking Spotify credentials...")
    
    load_dotenv()
    
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("  ✗ Credentials not found in .env file")
        print("\nSetup instructions:")
        print("1. Copy .env.template to .env")
        print("2. Get credentials from: https://developer.spotify.com/dashboard")
        print("3. Add your Client ID and Secret to .env")
        return False
    
    if client_id == "your_client_id_here":
        print("  ✗ Credentials not configured (still using template values)")
        return False
    
    print("  ✓ Client ID found")
    print("  ✓ Client Secret found")
    print("✓ Credentials configured!\n")
    return True


def test_api_connection():
    """Test connection to Spotify API."""
    print("🌐 Testing Spotify API connection...")
    
    try:
        from recommendation_engine import SpotifyRecommendationEngine
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        engine = SpotifyRecommendationEngine(client_id, client_secret)
        
        # Try a simple search to verify connection
        results = engine.sp.search(q='track', type='track', limit=1)
        
        if results['tracks']['items']:
            print("  ✓ Successfully connected to Spotify API")
            print("✓ API connection working!\n")
            return True
        else:
            print("  ✗ No search results (unexpected)")
            return False
    
    except Exception as e:
        print(f"  ✗ API connection failed: {str(e)}")
        return False


def test_recommendation_generation():
    """Test recommendation generation with sample data."""
    print("🎵 Testing recommendation generation...")
    
    try:
        from recommendation_engine import SpotifyRecommendationEngine
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        engine = SpotifyRecommendationEngine(client_id, client_secret)
        
        # Search for a popular track
        print("  Fetching test track data...")
        results = engine.sp.search(q='Blinding Lights', type='track', limit=10)
        
        track_ids = [t['id'] for t in results['tracks']['items']]
        
        print("  Extracting audio features...")
        engine.get_track_features(track_ids)
        
        if engine.track_features.empty:
            print("  ✗ Failed to extract features")
            return False
        
        print("  Finding similar tracks...")
        similar = engine.find_similar_tracks(track_ids[0], limit=5)
        
        if similar:
            print("  ✓ Successfully generated recommendations")
            print(f"  ✓ Found {len(similar)} similar tracks")
            print("✓ Recommendation generation working!\n")
            
            # Show sample output
            print("Sample recommendations:")
            for i, track in enumerate(similar[:3], 1):
                print(f"  {i}. {track['name']} - {', '.join(track.get('artists', []))}")
            print()
            
            return True
        else:
            print("  ✗ No recommendations generated")
            return False
    
    except Exception as e:
        print(f"  ✗ Recommendation test failed: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("SPOTIFY RECOMMENDATION ENGINE - VALIDATION")
    print("="*60 + "\n")
    
    tests = [
        ("Dependencies", check_dependencies),
        ("Credentials", check_credentials),
        ("API Connection", test_api_connection),
        ("Recommendations", test_recommendation_generation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with error: {str(e)}\n")
            results.append((test_name, False))
    
    # Summary
    print("="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your engine is ready to use.")
        print("\nNext steps:")
        print("1. Update user_id in dsjnd.py with your Spotify username")
        print("2. Run: python dsjnd.py")
        print("3. Or use CLI: python cli.py --user-id your_username")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        sys.exit(1)
    
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
