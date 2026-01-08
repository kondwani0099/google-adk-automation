# multi_agent/researcher.py
import os
import requests
from typing import Dict, List, Any
from google.adk.agents import Agent
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GoogleSearchService:
    """Google Custom Search API service."""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_CSE_API_KEY')
        self.cse_id = os.getenv('GOOGLE_CSE_ID')
        
        if not self.api_key or not self.cse_id:
            print("Warning: Google Custom Search API credentials not found in environment variables.")
            print("Please set GOOGLE_CSE_API_KEY and GOOGLE_CSE_ID in your .env file.")
            self.service = None
        else:
            try:
                self.service = build("customsearch", "v1", developerKey=self.api_key)
            except Exception as e:
                print(f"Error initializing Google Custom Search service: {e}")
                self.service = None
    
    def search(self, query: str, num_results: int = 10) -> Dict[str, Any]:
        """
        Perform Google Custom Search.
        
        Args:
            query: Search query
            num_results: Number of results to return (max 10 per request)
            
        Returns:
            Dictionary with search results
        """
        if not self.service:
            return {
                "status": "error",
                "error": "Google Custom Search service not initialized. Please check your API credentials.",
                "results": []
            }
        
        try:
            # Perform the search
            result = self.service.cse().list(
                q=query,
                cx=self.cse_id,
                num=min(num_results, 10)  # API limit is 10 per request
            ).execute()
            
            # Extract relevant information
            items = result.get('items', [])
            search_results = []
            
            for item in items:
                search_results.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'displayLink': item.get('displayLink', '')
                })
            
            return {
                "status": "success",
                "query": query,
                "total_results": result.get('searchInformation', {}).get('totalResults', '0'),
                "search_time": result.get('searchInformation', {}).get('searchTime', '0'),
                "results": search_results
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Search failed: {str(e)}",
                "results": []
            }

# Initialize the search service
search_service = GoogleSearchService()

def google_search(query: str, num_results: int = 5) -> dict:
    """
    Google search tool function for the agent.
    
    Args:
        query: The search query
        num_results: Number of results to return (default: 5, max: 10)
        
    Returns:
        Dictionary with search results
    """
    try:
        result = search_service.search(query, num_results)
        
        if result["status"] == "success":
            # Format results for the agent
            formatted_results = []
            for item in result["results"]:
                formatted_results.append(
                    f"Title: {item['title']}\n"
                    f"URL: {item['link']}\n"
                    f"Snippet: {item['snippet']}\n"
                    f"Source: {item['displayLink']}\n"
                )
            
            return {
                "status": "success",
                "query": query,
                "total_results": result["total_results"],
                "search_time": result["search_time"],
                "formatted_results": "\n---\n".join(formatted_results),
                "raw_results": result["results"]
            }
        else:
            return {
                "status": "error",
                "query": query,
                "error": result.get("error", "Unknown error occurred"),
                "formatted_results": f"Search failed for query '{query}': {result.get('error', 'Unknown error')}"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "query": query,
            "error": str(e),
            "formatted_results": f"Error performing search for '{query}': {str(e)}"
        }

def web_scrape(url: str) -> dict:
    """
    Simple web scraping tool to get content from a URL.
    
    Args:
        url: The URL to scrape
        
    Returns:
        Dictionary with the scraped content
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Simple text extraction (you might want to use BeautifulSoup for better parsing)
        content = response.text
        
        # Basic cleanup - extract text between body tags if present
        if '<body' in content.lower() and '</body>' in content.lower():
            start = content.lower().find('<body')
            start = content.find('>', start) + 1
            end = content.lower().rfind('</body>')
            content = content[start:end]
        
        # Remove HTML tags (basic approach)
        import re
        clean_content = re.sub(r'<[^>]+>', ' ', content)
        clean_content = re.sub(r'\s+', ' ', clean_content).strip()
        
        # Limit content length
        max_length = 2000
        if len(clean_content) > max_length:
            clean_content = clean_content[:max_length] + "..."
        
        return {
            "status": "success",
            "url": url,
            "content": clean_content,
            "length": len(clean_content)
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "url": url,
            "error": f"Failed to fetch URL: {str(e)}",
            "content": ""
        }
    except Exception as e:
        return {
            "status": "error",
            "url": url,
            "error": f"Error processing URL: {str(e)}",
            "content": ""
        }

root_agent = Agent(
    name="researcher",
    model="gemini-3.0-flash",
    description="Fetches information using Google Custom Search API and web scraping tools.",
    instruction="""You are a research agent that can search the web for information and scrape web pages. 

    Use the google_search tool to find relevant information on the web. The tool returns formatted search results with titles, URLs, and snippets.
    
    Use the web_scrape tool to get detailed content from specific URLs when you need more information than what's available in the search snippets.
    
    When responding:
    1. Perform searches using relevant keywords
    2. Analyze the search results and identify the most relevant sources
    3. If needed, scrape specific URLs for more detailed information
    4. Provide comprehensive answers based on the collected information
    5. Always cite your sources with URLs when possible
    6. If search fails or returns no results, acknowledge this clearly
    
    Be thorough in your research and provide accurate, up-to-date information.""",
    tools=[google_search, web_scrape],
)

# Example usage and testing
if __name__ == "__main__":
    # Test the Google search functionality
    test_query = "latest AI developments 2024"
    result = google_search(test_query, num_results=3)
    
    print("=== Google Search Test ===")
    print(f"Query: {test_query}")
    print(f"Status: {result['status']}")
    
    if result['status'] == 'success':
        print(f"Total results: {result['total_results']}")
        print(f"Search time: {result['search_time']} seconds")
        print("\n=== Search Results ===")
        print(result['formatted_results'])
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
        print(result['formatted_results'])