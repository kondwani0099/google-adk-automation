#!/usr/bin/env python3
"""
Test script for Google Custom Search API functionality.
Run this script to verify your Google Custom Search setup is working correctly.
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_environment_variables():
    """Test if required environment variables are set."""
    print("=== Environment Variables Test ===")
    
    load_dotenv()
    
    cse_id = os.getenv('GOOGLE_CSE_ID')
    api_key = os.getenv('GOOGLE_CSE_API_KEY')
    
    print(f"GOOGLE_CSE_ID: {'✓ Set' if cse_id else '✗ Not set'}")
    print(f"GOOGLE_CSE_API_KEY: {'✓ Set' if api_key else '✗ Not set'}")
    
    if not cse_id or not api_key:
        print("\n❌ Missing required environment variables!")
        print("Please update your .env file with:")
        print("GOOGLE_CSE_ID=\"your-custom-search-engine-id\"")
        print("GOOGLE_CSE_API_KEY=\"your-google-api-key\"")
        print("\nSee GOOGLE_SEARCH_SETUP.md for detailed setup instructions.")
        return False
    
    print("✅ Environment variables are set!")
    return True

def test_google_search():
    """Test the Google Custom Search functionality."""
    print("\n=== Google Search API Test ===")
    
    try:
        from multi_agent.researcher import google_search
        
        # Test with a simple query
        test_query = "Python programming"
        print(f"Testing search for: '{test_query}'")
        
        result = google_search(test_query, num_results=3)
        
        print(f"Status: {result['status']}")
        
        if result['status'] == 'success':
            print(f"✅ Search successful!")
            print(f"Total results: {result.get('total_results', 'N/A')}")
            print(f"Search time: {result.get('search_time', 'N/A')} seconds")
            print(f"Number of results returned: {len(result.get('raw_results', []))}")
            
            # Show first result
            if result.get('raw_results'):
                first_result = result['raw_results'][0]
                print(f"\nFirst result:")
                print(f"  Title: {first_result.get('title', 'N/A')}")
                print(f"  URL: {first_result.get('link', 'N/A')}")
                print(f"  Snippet: {first_result.get('snippet', 'N/A')[:100]}...")
            
            return True
        else:
            print(f"❌ Search failed: {result.get('error', 'Unknown error')}")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_web_scraping():
    """Test the web scraping functionality."""
    print("\n=== Web Scraping Test ===")
    
    try:
        from multi_agent.researcher import web_scrape
        
        # Test with a simple, reliable URL
        test_url = "https://httpbin.org/html"
        print(f"Testing web scraping for: {test_url}")
        
        result = web_scrape(test_url)
        
        print(f"Status: {result['status']}")
        
        if result['status'] == 'success':
            print(f"✅ Web scraping successful!")
            print(f"Content length: {result.get('length', 0)} characters")
            print(f"Sample content: {result.get('content', '')[:200]}...")
            return True
        else:
            print(f"❌ Web scraping failed: {result.get('error', 'Unknown error')}")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Run all tests."""
    print("Google Custom Search API Test Suite")
    print("=" * 40)
    
    # Test environment variables
    if not test_environment_variables():
        return
    
    # Test Google Search
    search_success = test_google_search()
    
    # Test web scraping
    scraping_success = test_web_scraping()
    
    # Summary
    print("\n" + "=" * 40)
    print("Test Summary:")
    print(f"Environment Variables: ✅")
    print(f"Google Search API: {'✅' if search_success else '❌'}")
    print(f"Web Scraping: {'✅' if scraping_success else '❌'}")
    
    if search_success and scraping_success:
        print("\n🎉 All tests passed! Your Google Custom Search setup is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above and:")
        print("1. Verify your API credentials are correct")
        print("2. Ensure the Custom Search API is enabled")
        print("3. Check your internet connection")
        print("4. Review the GOOGLE_SEARCH_SETUP.md file for troubleshooting")

if __name__ == "__main__":
    main()