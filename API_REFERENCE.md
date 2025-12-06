# 📡 API Integration Reference

Complete guide for integrating with marketing platforms.

---

## Overview

| Platform | Difficulty | Setup Time | Real-Time | Documentation |
|----------|-----------|-----------|-----------|-----------------|
| **Facebook/Instagram** | Medium | 30 min | ✓ Yes | Meta Business Suite |
| **Google Analytics** | Medium | 25 min | ✓ Yes | Google Console |
| **Google Ads** | Hard | 45 min | ✓ Yes | Google Ads API |
| **Email (Mailchimp)** | Easy | 15 min | ✓ Yes | Mailchimp API |
| **Stripe** | Easy | 20 min | ✓ Yes | Stripe Dashboard |

---

## 1. Facebook & Instagram Ads

### Difficulty: Medium | Time: 30 min

### Get Access Token

1. Go to [Meta Business Suite](https://business.facebook.com)
2. Click "Settings" → "User & Accounts"
3. Go to "System User" or create new
4. Create app and get access token
5. Token lasts 60 days, then renew

### Code Integration

```python
# In src/data_collector.py

import requests
from datetime import datetime, timedelta

def fetch_facebook_campaigns(self):
    """Fetch Facebook/Instagram campaign data"""
    
    access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
    api_version = 'v18.0'
    
    try:
        # Get all campaigns for account
        response = requests.get(
            f'https://graph.instagram.com/{api_version}/me/campaigns',
            params={
                'access_token': access_token,
                'fields': 'id,name,status,created_time,spend,reach,impressions'
            }
        )
        response.raise_for_status()
        campaigns = response.json()['data']
        
        results = []
        for campaign in campaigns:
            # Get detailed insights
            insights_response = requests.get(
                f'https://graph.instagram.com/{api_version}/{campaign["id"]}/insights',
                params={
                    'access_token': access_token,
                    'metric': 'spend,reach,impressions,inline_link_clicks,actions'
                }
            )
            
            insights = {item['name']: item['values'][0]['value'] 
                       for item in insights_response.json()['data']}
            
            campaign_data = {
                'campaign_name': campaign['name'],
                'channel': 'facebook',
                'platform': 'Instagram Ads',
                'budget': float(insights.get('spend', 0)),
                'spend': float(insights.get('spend', 0)),
                'impressions': int(insights.get('impressions', 0)),
                'clicks': int(insights.get('inline_link_clicks', 0)),
                'conversions': int(insights.get('actions', [{}])[0].get('value', 0)),
                'date': datetime.now().isoformat()
            }
            results.append(campaign_data)
        
        print(f"✓ Fetched {len(results)} Facebook campaigns")
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Facebook API error: {e}")
        return []
```

### Environment Variables
```bash
echo "FACEBOOK_ACCESS_TOKEN=eaab123...your_token_here" >> .env
```

### Permissions Needed
- `ads_read`
- `instagram_basic`
- `instagram_insights`

### API Limits
- Rate limit: 200 requests/10 seconds
- Batch up to 50 campaigns per request
- Data available after 30 minutes

---

## 2. Google Analytics 4

### Difficulty: Medium | Time: 25 min

### Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project
3. Enable Google Analytics API
4. Create Service Account (JSON key)
5. Download credentials JSON
6. Add service account to GA4 property

### Code Integration

```python
# In src/data_collector.py

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, Dimension, Metric, DateRange
)
from google.oauth2 import service_account
import json

def fetch_google_analytics_data(self):
    """Fetch Google Analytics 4 data"""
    
    cred_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json')
    property_id = os.getenv('GOOGLE_GA4_PROPERTY_ID')
    
    try:
        # Initialize client
        credentials = service_account.Credentials.from_service_account_file(cred_file)
        client = BetaAnalyticsDataClient(credentials=credentials)
        
        # Query GA4 data
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
            dimensions=[
                Dimension(name="sessionSource"),
                Dimension(name="sessionMedium"),
                Dimension(name="pageTitle")
            ],
            metrics=[
                Metric(name="sessions"),
                Metric(name="activeUsers"),
                Metric(name="conversions"),
                Metric(name="totalRevenue")
            ]
        )
        
        response = client.run_report(request)
        
        results = []
        for row in response.rows:
            result = {
                'campaign_name': row.dimension_values[0].value,
                'channel': row.dimension_values[1].value,
                'platform': 'Google Analytics',
                'impressions': int(row.metric_values[0].value),
                'clicks': int(row.metric_values[1].value),
                'conversions': int(row.metric_values[2].value),
                'revenue': float(row.metric_values[3].value),
                'date': datetime.now().isoformat()
            }
            results.append(result)
        
        print(f"✓ Fetched {len(results)} GA4 campaigns")
        return results
        
    except Exception as e:
        print(f"✗ Google Analytics error: {e}")
        return []
```

### Installation
```bash
pip install google-analytics-data google-auth google-auth-oauthlib
```

### Environment Variables
```bash
echo "GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json" >> .env
echo "GOOGLE_GA4_PROPERTY_ID=123456789" >> .env
```

### Get Property ID
1. Go to GA4 account
2. Admin → Property settings
3. Copy "Property ID"

---

## 3. Google Ads

### Difficulty: Hard | Time: 45 min

### Setup

1. Go to [Google Ads API](https://developers.google.com/google-ads/api)
2. Create Google Cloud project
3. Enable Google Ads API
4. Get OAuth 2.0 credentials
5. Generate refresh token

### Code Integration

```python
# In src/data_collector.py

from google.ads.googleads.client import GoogleAdsClient

def fetch_google_ads_campaigns(self):
    """Fetch Google Ads campaign data"""
    
    client = GoogleAdsClient.load_from_storage()
    customer_id = os.getenv('GOOGLE_ADS_CUSTOMER_ID')
    
    try:
        ga_service = client.get_service("GoogleAdsService")
        
        query = """
            SELECT
              campaign.id,
              campaign.name,
              campaign.status,
              metrics.impressions,
              metrics.clicks,
              metrics.conversions,
              metrics.cost_micros
            FROM campaign
            WHERE campaign.status = ENABLED
        """
        
        request = client.build_list_request(
            customer_id=customer_id,
            query=query
        )
        
        results = []
        for row in ga_service.search_stream(request):
            campaign = row.campaign
            metrics = row.metrics
            
            campaign_data = {
                'campaign_name': campaign.name,
                'channel': 'google',
                'platform': 'Google Ads',
                'budget': metrics.cost_micros / 1_000_000,
                'spend': metrics.cost_micros / 1_000_000,
                'impressions': metrics.impressions,
                'clicks': metrics.clicks,
                'conversions': metrics.conversions,
                'date': datetime.now().isoformat()
            }
            results.append(campaign_data)
        
        print(f"✓ Fetched {len(results)} Google Ads campaigns")
        return results
        
    except Exception as e:
        print(f"✗ Google Ads error: {e}")
        return []
```

### Installation
```bash
pip install google-ads
```

### Setup google_ads.yaml
```yaml
development:
  client_id: YOUR_CLIENT_ID
  client_secret: YOUR_CLIENT_SECRET
  refresh_token: YOUR_REFRESH_TOKEN
  use_proto_plus: true

production:
  client_id: ${GOOGLE_ADS_CLIENT_ID}
  client_secret: ${GOOGLE_ADS_CLIENT_SECRET}
  refresh_token: ${GOOGLE_ADS_REFRESH_TOKEN}
  use_proto_plus: true
```

---

## 4. Mailchimp Email Campaigns

### Difficulty: Easy | Time: 15 min

### Get API Key

1. Go to [Mailchimp Account](https://mailchimp.com/account/)
2. Settings → API keys
3. Create new API key
4. Copy key (format: `xxxxxxxxxxxxx-us1`)

### Code Integration

```python
# In src/data_collector.py

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

def fetch_mailchimp_campaigns(self):
    """Fetch Mailchimp email campaign data"""
    
    api_key = os.getenv('MAILCHIMP_API_KEY')
    
    try:
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": api_key,
            "region": api_key.split('-')[1]  # Extract region from key
        })
        
        campaigns_response = client.campaigns.list(get_all=True)
        
        results = []
        for campaign in campaigns_response['campaigns']:
            campaign_data = {
                'campaign_name': campaign['settings']['title'],
                'channel': 'email',
                'platform': 'Mailchimp',
                'budget': 0,  # Mailchimp doesn't use budget
                'spend': 0,
                'impressions': campaign['emails_sent'],
                'clicks': campaign['report_summary']['click_rate'],
                'conversions': campaign['report_summary'].get('opens', 0),
                'revenue': 0,
                'date': datetime.now().isoformat()
            }
            results.append(campaign_data)
        
        print(f"✓ Fetched {len(results)} Mailchimp campaigns")
        return results
        
    except ApiClientError as e:
        print(f"✗ Mailchimp error: {e}")
        return []
```

### Installation
```bash
pip install mailchimp-marketing
```

### Environment Variables
```bash
echo "MAILCHIMP_API_KEY=xxxxxxxxxxxxx-us1" >> .env
```

---

## 5. Stripe Payments

### Difficulty: Easy | Time: 20 min

### Get API Key

1. Go to [Stripe Dashboard](https://dashboard.stripe.com)
2. Settings → API Keys
3. Copy "Secret key" (starts with `sk_test_` or `sk_live_`)

### Code Integration

```python
# In src/data_collector.py

import stripe

def fetch_stripe_campaigns(self):
    """Fetch Stripe payment data"""
    
    api_key = os.getenv('STRIPE_API_KEY')
    stripe.api_key = api_key
    
    try:
        # Get payment intents (charges)
        charges = stripe.Charge.list(limit=100)
        
        # Group by campaign source
        campaigns = {}
        for charge in charges.data:
            source = charge.metadata.get('campaign', 'default')
            
            if source not in campaigns:
                campaigns[source] = {
                    'revenue': 0,
                    'conversions': 0,
                    'amount': 0
                }
            
            campaigns[source]['revenue'] += charge.amount / 100
            campaigns[source]['conversions'] += 1
            campaigns[source]['amount'] = charge.amount
        
        results = []
        for campaign_name, data in campaigns.items():
            campaign_data = {
                'campaign_name': campaign_name,
                'channel': 'stripe',
                'platform': 'Stripe',
                'budget': 0,
                'spend': 0,
                'impressions': 0,
                'clicks': data['conversions'],
                'conversions': data['conversions'],
                'revenue': data['revenue'],
                'date': datetime.now().isoformat()
            }
            results.append(campaign_data)
        
        print(f"✓ Fetched {len(results)} Stripe campaigns")
        return results
        
    except stripe.error.StripeError as e:
        print(f"✗ Stripe error: {e}")
        return []
```

### Installation
```bash
pip install stripe
```

### Environment Variables
```bash
echo "STRIPE_API_KEY=sk_test_xxxxx" >> .env  # Use sk_test_ for testing
```

### Metadata Tag for Campaign Tracking
In your Stripe integration code, tag charges:
```python
stripe.Charge.create(
    amount=5000,  # $50.00
    currency="usd",
    source="tok_visa",
    metadata={'campaign': 'summer_sale'}
)
```

---

## 6. TikTok Ads

### Difficulty: Medium | Time: 35 min

### Get Access Token

1. Go to [TikTok Developer](https://developer.tiktok.com)
2. Create app and get credentials
3. Use OAuth 2.0 to get access token
4. Token valid for 24 hours, use refresh token

### Code Integration

```python
# In src/data_collector.py

import requests

def fetch_tiktok_campaigns(self):
    """Fetch TikTok Ads campaign data"""
    
    access_token = os.getenv('TIKTOK_ACCESS_TOKEN')
    advertiser_id = os.getenv('TIKTOK_ADVERTISER_ID')
    
    try:
        # Get campaigns list
        response = requests.get(
            'https://business-api.tiktok.com/open_api/v1.3/campaign/get/',
            headers={'Access-Token': access_token},
            params={'advertiser_id': advertiser_id}
        )
        response.raise_for_status()
        campaigns = response.json()['data']['list']
        
        results = []
        for campaign in campaigns:
            # Get campaign insights
            insights_response = requests.get(
                'https://business-api.tiktok.com/open_api/v1.3/reports/integrated/get/',
                headers={'Access-Token': access_token},
                params={
                    'advertiser_id': advertiser_id,
                    'campaign_id': campaign['campaign_id'],
                    'metrics': 'spend,impressions,clicks,conversions'
                }
            )
            
            insights = insights_response.json()['data']
            
            campaign_data = {
                'campaign_name': campaign['campaign_name'],
                'channel': 'tiktok',
                'platform': 'TikTok Ads',
                'budget': float(campaign['budget']),
                'spend': float(insights.get('spend', 0)),
                'impressions': int(insights.get('impressions', 0)),
                'clicks': int(insights.get('clicks', 0)),
                'conversions': int(insights.get('conversions', 0)),
                'date': datetime.now().isoformat()
            }
            results.append(campaign_data)
        
        print(f"✓ Fetched {len(results)} TikTok campaigns")
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"✗ TikTok API error: {e}")
        return []
```

### Environment Variables
```bash
echo "TIKTOK_ACCESS_TOKEN=your_token" >> .env
echo "TIKTOK_ADVERTISER_ID=your_advertiser_id" >> .env
```

---

## 7. LinkedIn Ads

### Difficulty: Medium | Time: 30 min

### Get Access Token

1. Go to [LinkedIn Developer](https://www.linkedin.com/developers)
2. Create app and get credentials
3. Use OAuth 2.0 to get access token
4. Request `adAccount_access` scope

### Code Integration

```python
# In src/data_collector.py

import requests

def fetch_linkedin_campaigns(self):
    """Fetch LinkedIn Ads campaign data"""
    
    access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    ad_account = os.getenv('LINKEDIN_AD_ACCOUNT')
    
    try:
        # Get all campaigns
        response = requests.get(
            f'https://api.linkedin.com/v2/adCampaigns',
            headers={'Authorization': f'Bearer {access_token}'},
            params={'q': 'search', 'account': ad_account}
        )
        response.raise_for_status()
        campaigns = response.json()['elements']
        
        results = []
        for campaign in campaigns:
            campaign_id = campaign['id']
            
            # Get campaign analytics
            analytics = requests.get(
                f'https://api.linkedin.com/v2/adAnalyticsByCampaign',
                headers={'Authorization': f'Bearer {access_token}'},
                params={'campaigns': campaign_id}
            )
            
            data = analytics.json()['elements'][0]
            
            campaign_data = {
                'campaign_name': campaign['name'],
                'channel': 'linkedin',
                'platform': 'LinkedIn Ads',
                'budget': float(campaign.get('dailyBudget', 0)) / 100,
                'spend': float(data.get('costInLocalCurrency', 0)) / 100,
                'impressions': int(data.get('impressions', 0)),
                'clicks': int(data.get('clicks', 0)),
                'conversions': int(data.get('conversions', 0)),
                'date': datetime.now().isoformat()
            }
            results.append(campaign_data)
        
        print(f"✓ Fetched {len(results)} LinkedIn campaigns")
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"✗ LinkedIn API error: {e}")
        return []
```

### Environment Variables
```bash
echo "LINKEDIN_ACCESS_TOKEN=AQVxxx..." >> .env
echo "LINKEDIN_AD_ACCOUNT=urn:li:sponsoredAccount:123" >> .env
```

---

## API Error Handling Best Practices

```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def get_with_retry(url, **kwargs):
    """Make request with automatic retries"""
    
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=(500, 502, 504)
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    try:
        response = session.get(url, timeout=10, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("Request timeout - API took too long")
        return None
    except requests.exceptions.ConnectionError:
        print("Connection error - check internet")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e.response.status_code}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
```

---

## Rate Limiting Strategy

```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, calls_per_minute=60):
        self.calls_per_minute = calls_per_minute
        self.calls = deque()
    
    def wait(self):
        """Wait if needed to respect rate limit"""
        now = time.time()
        minute_ago = now - 60
        
        # Remove old calls
        while self.calls and self.calls[0] < minute_ago:
            self.calls.popleft()
        
        # Wait if needed
        if len(self.calls) >= self.calls_per_minute:
            sleep_time = 60 - (now - self.calls[0])
            if sleep_time > 0:
                print(f"Rate limit: waiting {sleep_time:.1f}s")
                time.sleep(sleep_time)
        
        self.calls.append(now)

# Usage
limiter = RateLimiter(calls_per_minute=200)
for campaign in campaigns:
    limiter.wait()
    response = requests.get(f"https://api.example.com/campaign/{campaign['id']}")
```

---

## Testing API Integration

```python
# In tests/test_tracker.py

import unittest
from unittest.mock import patch, MagicMock
from src.data_collector import DataCollector

class TestAPIIntegrations(unittest.TestCase):
    
    @patch('requests.get')
    def test_facebook_api(self, mock_get):
        """Test Facebook API integration"""
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'data': [{
                'id': '123',
                'name': 'Test Campaign',
                'spend': 100,
                'impressions': 10000
            }]
        }
        mock_get.return_value = mock_response
        
        collector = DataCollector()
        result = collector.fetch_facebook_campaigns()
        
        self.assertGreater(len(result), 0)
        self.assertEqual(result[0]['channel'], 'facebook')
    
    @patch('google.analytics.data_v1beta.BetaAnalyticsDataClient')
    def test_google_analytics(self, mock_client):
        """Test Google Analytics integration"""
        
        # Mock GA4 response
        mock_response = MagicMock()
        mock_response.rows = []
        
        collector = DataCollector()
        result = collector.fetch_google_analytics_data()
        
        self.assertIsInstance(result, list)
```

---

**Choose your integration, follow the setup steps, and start collecting real data!** 🚀
