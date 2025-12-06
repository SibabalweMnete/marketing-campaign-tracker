# ✅ Integration Checklist

Fast-track guide to get real data flowing in 30-60 minutes.

---

## Choose Your Platform

Pick ONE to start (easiest first):

```
Easiest:     Email (Mailchimp) - 15 min ✓
Simple:      Google Analytics - 25 min ✓
Medium:      Facebook/Instagram Ads - 30 min ✓
Professional: Google Ads API - 45 min
Advanced:    TikTok/LinkedIn/Stripe - 35-45 min
```

---

## OPTION 1: Email (Mailchimp) - 15 Minutes ⏱️

### Step 1: Get API Key (5 min)
- [ ] Go to https://mailchimp.com/account/
- [ ] Click "Settings" → "API keys"
- [ ] Click "Create Key"
- [ ] Copy key (looks like: `xxxxxxxxxxxxx-us1`)

### Step 2: Install Package (2 min)
```bash
pip install mailchimp-marketing
```

### Step 3: Create .env File (3 min)
```bash
echo "MAILCHIMP_API_KEY=xxxxxxxxxxxxx-us1" > .env
```

### Step 4: Update Code (5 min)

Edit `src/data_collector.py`, add to imports:
```python
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
```

Add this method to `DataCollector` class:
```python
def fetch_mailchimp_campaigns(self):
    """Fetch Mailchimp email campaign data"""
    api_key = os.getenv('MAILCHIMP_API_KEY')
    
    try:
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": api_key,
            "region": api_key.split('-')[1]
        })
        
        campaigns_response = client.campaigns.list(get_all=True)
        
        results = []
        for campaign in campaigns_response['campaigns']:
            campaign_data = {
                'campaign_name': campaign['settings']['title'],
                'channel': 'email',
                'platform': 'Mailchimp',
                'budget': 0,
                'spend': 0,
                'impressions': campaign['emails_sent'],
                'clicks': int(campaign['report_summary'].get('click_count', 0)),
                'conversions': int(campaign['report_summary'].get('opens', 0)),
                'revenue': 0,
                'date': datetime.now().isoformat()
            }
            results.append(campaign_data)
        
        print(f"✓ Fetched {len(results)} Mailchimp campaigns")
        return results
        
    except ApiClientError as e:
        print(f"✗ Mailchimp error: {e}")
        return self.get_demo_data()  # Fallback to demo
```

### Step 5: Add to collect_all_campaigns() (2 min)

In `collect_all_campaigns()` method, add:
```python
all_campaigns.extend(self.fetch_mailchimp_campaigns())
```

### Step 6: Test It (5 min)
```bash
python3 main.py --collect
python3 main.py --summary
```

Expected output:
```
Collecting campaigns from all platforms...
✓ Fetched X Facebook campaigns
✓ Fetched X Google Analytics campaigns
✓ Fetched X Mailchimp campaigns
...
```

---

## OPTION 2: Google Analytics - 25 Minutes ⏱️

### Step 1: Setup Google Cloud (10 min)
- [ ] Go to https://console.cloud.google.com
- [ ] Create new project (name: `marketing-tracker`)
- [ ] Enable "Google Analytics Data API"
- [ ] Go to Credentials → Create Service Account
- [ ] Download JSON key file
- [ ] Save as `credentials.json` in project root

### Step 2: Get GA4 Property ID (5 min)
- [ ] Go to Google Analytics 4 account
- [ ] Click "Admin" (gear icon)
- [ ] Click "Property" → "Property Settings"
- [ ] Copy "Property ID" (number like 123456789)

### Step 3: Share with Service Account (5 min)
- [ ] Open `credentials.json`, find `client_email`
- [ ] In Google Analytics, go to Admin → Property Access Management
- [ ] Add that email with "Editor" permission

### Step 4: Install Package (2 min)
```bash
pip install google-analytics-data google-auth
```

### Step 5: Create .env File (2 min)
```bash
cat >> .env << EOF
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
GOOGLE_GA4_PROPERTY_ID=123456789
EOF
```

### Step 6: Update Code (5 min)

Add to imports in `src/data_collector.py`:
```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, Dimension, Metric, DateRange
from google.oauth2 import service_account
```

Add method to `DataCollector` class:
```python
def fetch_google_analytics(self):
    """Fetch Google Analytics data"""
    import os
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import RunReportRequest, Dimension, Metric, DateRange
    from google.oauth2 import service_account
    
    cred_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json')
    property_id = os.getenv('GOOGLE_GA4_PROPERTY_ID')
    
    try:
        credentials = service_account.Credentials.from_service_account_file(cred_file)
        client = BetaAnalyticsDataClient(credentials=credentials)
        
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
            dimensions=[Dimension(name="sessionSource")],
            metrics=[
                Metric(name="sessions"),
                Metric(name="activeUsers"),
                Metric(name="totalRevenue")
            ]
        )
        
        response = client.run_report(request)
        
        results = []
        for row in response.rows:
            campaign_data = {
                'campaign_name': row.dimension_values[0].value,
                'channel': 'organic',
                'platform': 'Google Analytics',
                'budget': 0,
                'spend': 0,
                'impressions': int(row.metric_values[0].value),
                'clicks': int(row.metric_values[1].value),
                'conversions': 0,
                'revenue': float(row.metric_values[2].value),
                'date': datetime.now().isoformat()
            }
            results.append(campaign_data)
        
        print(f"✓ Fetched {len(results)} GA4 data points")
        return results
        
    except Exception as e:
        print(f"✗ Google Analytics error: {e}")
        return self.get_demo_data()
```

### Step 7: Add to collect_all_campaigns() (2 min)
```python
all_campaigns.extend(self.fetch_google_analytics())
```

### Step 8: Test It (3 min)
```bash
python3 main.py --collect
python3 main.py --summary
```

---

## OPTION 3: Facebook/Instagram Ads - 30 Minutes ⏱️

### Step 1: Get Access Token (15 min)
- [ ] Go to https://business.facebook.com
- [ ] Click "Settings" → "Users & Assets"
- [ ] Go to "System Users"
- [ ] Create new system user or select existing
- [ ] Go to "Apps"
- [ ] Add your app
- [ ] Click user → "Generate New Token"
- [ ] Copy token

### Step 2: Install Package (2 min)
```bash
pip install requests
```

### Step 3: Create .env File (2 min)
```bash
echo "FACEBOOK_ACCESS_TOKEN=eaab...your_token_here" >> .env
```

### Step 4: Update Code (8 min)

Add to imports:
```python
import requests
```

Add method:
```python
def fetch_facebook_campaigns(self):
    """Fetch Facebook/Instagram campaign data"""
    access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
    api_version = 'v18.0'
    
    try:
        response = requests.get(
            f'https://graph.instagram.com/{api_version}/me/campaigns',
            params={
                'access_token': access_token,
                'fields': 'id,name,status,spend,reach,impressions'
            },
            timeout=10
        )
        response.raise_for_status()
        campaigns = response.json()['data']
        
        results = []
        for campaign in campaigns:
            insights_response = requests.get(
                f'https://graph.instagram.com/{api_version}/{campaign["id"]}/insights',
                params={
                    'access_token': access_token,
                    'metric': 'spend,reach,impressions,inline_link_clicks'
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
                'conversions': 0,
                'date': datetime.now().isoformat()
            }
            results.append(campaign_data)
        
        print(f"✓ Fetched {len(results)} Facebook campaigns")
        return results
        
    except Exception as e:
        print(f"✗ Facebook error: {e}")
        return self.get_demo_data()
```

### Step 5: Add to collect_all_campaigns()
```python
all_campaigns.extend(self.fetch_facebook_campaigns())
```

### Step 6: Test It (3 min)
```bash
python3 main.py --collect
python3 main.py --summary
```

---

## Verification Checklist

After you've added your integration:

- [ ] Created API credentials file/token
- [ ] Added to `.env` file (check with `cat .env`)
- [ ] Installed required package with pip
- [ ] Added code to `src/data_collector.py`
- [ ] Added call to `collect_all_campaigns()`
- [ ] Ran `python3 main.py --collect` without errors
- [ ] Data appears in summary: `python3 main.py --summary`
- [ ] Can generate reports: `python3 main.py --report`

---

## Testing Commands

```bash
# Test collection
python3 main.py --collect

# Check data was saved
python3 main.py --summary

# Generate reports
python3 main.py --report

# View insights
python3 main.py --insights

# View comparison
python3 main.py --compare

# Full auto mode
python3 main.py --auto
```

---

## Troubleshooting During Integration

### "ModuleNotFoundError"
```bash
# Install missing package
pip install mailchimp-marketing  # or google-analytics-data, etc.
```

### "API key not found in .env"
```bash
# Check .env exists
cat .env

# Should show your variable
# If missing, recreate it:
echo "FACEBOOK_ACCESS_TOKEN=xxxxx" > .env
```

### "401 Unauthorized"
```bash
# Your token/key is wrong or expired
# Get a new one from the platform
# Update .env with new value
```

### "Connection timeout"
```bash
# API took too long - try again
# Or check internet connection
ping google.com
```

### "Empty results despite correct credentials"
```bash
# You might not have campaigns yet
# Or they're in different account
# Check credentials are for right account
```

---

## Next Steps After First Integration

1. ✅ First integration working
2. Choose second platform to integrate
3. Test both platforms together
4. Set up automated collection (cron/GitHub Actions)
5. Configure dashboard for monitoring

---

## One-Liner Quick Start

```bash
# After getting API key:
echo "API_KEY=xxxxx" >> .env && \
pip install required-package && \
python3 main.py --collect && \
python3 main.py --summary
```

---

## Integration Hierarchy

Easiest to Hardest:

1. ✅ **Email (Mailchimp)** - Just need API key - 15 min
2. ✅ **Google Analytics** - Need JSON credentials file - 25 min
3. ✅ **Facebook Ads** - Need system user access token - 30 min
4. ⚠️ **Google Ads** - Complex OAuth flow - 45 min
5. ⚠️ **TikTok/LinkedIn** - Different API patterns - 35-40 min

**Recommendation: Start with Google Analytics (most data) or Mailchimp (easiest setup).**

---

**Ready to integrate? Pick a platform and follow the checklist!** 🚀
