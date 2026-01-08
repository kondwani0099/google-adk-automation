# Google Custom Search API Setup Instructions

## Overview
The researcher agent has been updated to use the actual Google Custom Search API instead of mock data. To use this functionality, you need to set up Google Custom Search Engine and get the required credentials.

## Step 1: Create a Google Custom Search Engine

1. Go to [Google Custom Search Engine](https://cse.google.com/cse/)
2. Click "Add" to create a new search engine
3. In the "Sites to search" field, enter `*` to search the entire web
4. Give your search engine a name (e.g., "Research Agent Search")
5. Click "Create"
6. After creation, click on "Control Panel" for your search engine
7. In the "Setup" tab, note down your **Search engine ID** (this is your CSE_ID)
8. In the "Setup" tab, turn ON "Search the entire web" option
9. You can also customize other settings as needed

## Step 2: Get Google API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the "Custom Search API":
   - Go to "APIs & Services" > "Library"
   - Search for "Custom Search API"
   - Click on it and press "Enable"
4. Create credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the generated API key
   - (Optional) Restrict the API key to only the Custom Search API for security

## Step 3: Update Environment Variables

Update your `.env` file with the credentials:

```env
# Replace 'your-custom-search-engine-id' with your actual CSE ID from Step 1
GOOGLE_CSE_ID="your-custom-search-engine-id"

# Replace with your API key from Step 2 (or use the existing GOOGLE_API_KEY if it has Custom Search API enabled)
GOOGLE_CSE_API_KEY="your-google-api-key"
```

## Step 4: Test the Setup

Run the researcher agent test:

```python
from multi_agent.researcher import google_search

# Test search
result = google_search("Python programming tutorial", num_results=3)
print(result)
```

## Features Available

### 1. Google Search Tool
- **Function**: `google_search(query: str, num_results: int = 5)`
- **Purpose**: Search the web using Google Custom Search API
- **Returns**: Formatted search results with titles, URLs, and snippets

### 2. Web Scraping Tool
- **Function**: `web_scrape(url: str)`
- **Purpose**: Extract content from specific web pages
- **Returns**: Cleaned text content from the webpage

## Usage Examples

### Basic Search
```python
result = google_search("artificial intelligence trends 2024")
```

### Search with Specific Number of Results
```python
result = google_search("machine learning algorithms", num_results=10)
```

### Scrape a Specific URL
```python
content = web_scrape("https://example.com/article")
```

## API Limits and Pricing

- **Free Tier**: 100 search queries per day
- **Paid Tier**: $5 per 1000 queries (after free tier)
- **Rate Limits**: 10 queries per second
- **Results per Query**: Maximum 10 results per API call

## Troubleshooting

### Common Issues:

1. **"Google Custom Search service not initialized"**
   - Check that `GOOGLE_CSE_ID` and `GOOGLE_CSE_API_KEY` are set in `.env`
   - Verify the API key has Custom Search API enabled

2. **"Search failed: API key not valid"**
   - Verify your API key is correct
   - Check that the Custom Search API is enabled for your project
   - Ensure API key restrictions (if any) allow Custom Search API

3. **"Search failed: Invalid CSE ID"**
   - Double-check your Custom Search Engine ID
   - Ensure the search engine is set to search the entire web

4. **"Daily quota exceeded"**
   - You've hit the daily limit of 100 free searches
   - Consider upgrading to paid tier or wait until next day

## Security Notes

- Never commit API keys to version control
- Use environment variables for all sensitive credentials
- Consider restricting API keys to specific APIs and IP ranges in production
- Monitor your API usage to avoid unexpected charges

## Next Steps

After setting up the credentials:
1. Test the search functionality
2. Integrate with your multi-agent system
3. Consider adding more specialized search tools (image search, news search, etc.)
4. Implement caching to reduce API calls for repeated queries