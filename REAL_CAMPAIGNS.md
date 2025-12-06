# 🎯 How to Track Real Campaigns - Integration Guide

## Real-Life Campaign Tracking Setup

Your tracker currently uses **simulated data** for demo purposes. Here's how to connect it to your **actual marketing campaigns**!

---

## 📱 Option 1: Facebook Ads Integration

### Step 1: Get Your Facebook Ads Credentials
1. Go to [Facebook Business Manager](https://business.facebook.com)
2. Navigate to **Settings → Business Settings → Accounts**
3. Click on your **Ads Account ID** (format: `act_123456789`)
4. Go to **System User → Generate New Token**
5. Copy your **Access Token** (starts with `EAAB...`)

### Step 2: Update `src/data_collector.py`

Replace the simulated data with real API calls:

```python
import requests

def fetch_facebook_campaigns(self):
    """Fetch REAL Facebook Ads campaign data"""
    ACCESS_TOKEN = "YOUR_FACEBOOK_ACCESS_TOKEN"
    ACCOUNT_ID = "YOUR_ADS_ACCOUNT_ID"
    
    url = f"https://graph.facebook.com/v18.0/{ACCOUNT_ID}/campaigns"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,status,daily_budget,lifetime_budget,spend,created_time'
    }
    
    response = requests.get(url, params=params)
    campaigns_data = response.json()['data']
    
    campaigns = []
    for campaign in campaigns_data:
        # Fetch insights (metrics)
        insights_url = f"https://graph.facebook.com/v18.0/{campaign['id']}/insights"
        insights_params = {
            'access_token': ACCESS_TOKEN,
            'fields': 'impressions,clicks,actions,spend,action_values',
            'date_preset': 'today'
        }
        
        insights = requests.get(insights_url, params=insights_params).json()['data'][0]
        
        campaigns.append({
            'campaign_id': f"FB_{campaign['id']}",
            'name': campaign['name'],
            'channel': 'Facebook',
            'status': campaign['status'],
            'start_date': campaign['created_time'][:10],
            'budget': campaign.get('lifetime_budget', 0) / 100,
            'metrics': {
                'impressions': insights.get('impressions', 0),
                'clicks': insights.get('clicks', 0),
                'conversions': insights.get('actions', [{}])[0].get('value', 0) if insights.get('actions') else 0,
                'spend': float(insights.get('spend', 0)),
                'revenue': float(insights.get('action_values', [{}])[0].get('value', 0) * float(insights.get('spend', 0))) if insights.get('action_values') else 0
            }
        })
    
    return campaigns
```

---

## 🔍 Option 2: Google Ads Integration

### Step 1: Get Your Google Ads Credentials
1. Go to [Google Ads Account](https://ads.google.com)
2. Click **Settings → Account Settings**
3. Copy your **Customer ID** (format: `123-456-7890`)
4. Go to **Settings → Developer tokens** → Request developer token
5. Create OAuth 2.0 credentials in [Google Cloud Console](https://console.cloud.google.com)

### Step 2: Install Google Ads Library
```bash
pip install google-ads
```

### Step 3: Update `src/data_collector.py`

```python
from google.ads.googleads.client import GoogleAdsClient

def fetch_google_campaigns(self):
    """Fetch REAL Google Ads campaign data"""
    
    client = GoogleAdsClient.load_from_storage(
        'google_ads_config.yaml'  # Create this file with credentials
    )
    
    customer_service = client.get_service("GoogleAdsService")
    
    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.budget_settings.amount_micros,
            metrics.impressions,
            metrics.clicks,
            metrics.conversions,
            metrics.cost_micros
        FROM campaign
        WHERE campaign.status = ENABLED
        ORDER BY metrics.cost_micros DESC
    """
    
    response = customer_service.search_stream(
        customer_id=YOUR_CUSTOMER_ID,
        query=query
    )
    
    campaigns = []
    for batch in response:
        for row in batch.results:
            campaign = row.campaign
            metrics = row.metrics
            
            campaigns.append({
                'campaign_id': f"GOOGLE_{campaign.id}",
                'name': campaign.name,
                'channel': 'Google Ads',
                'status': campaign.status.name,
                'budget': campaign.budget_settings.amount_micros / 1_000_000,
                'metrics': {
                    'impressions': metrics.impressions,
                    'clicks': metrics.clicks,
                    'conversions': int(metrics.conversions),
                    'spend': metrics.cost_micros / 1_000_000,
                    'revenue': 0  # Calculate from conversion value API
                }
            })
    
    return campaigns
```

### Step 3: Create `google_ads_config.yaml`
```yaml
developer_token: "YOUR_DEVELOPER_TOKEN"
client_id: "YOUR_CLIENT_ID"
client_secret: "YOUR_CLIENT_SECRET"
refresh_token: "YOUR_REFRESH_TOKEN"
use_proto_plus: true
```

---

## 📧 Option 3: Email Marketing Integration

### For Mailchimp:
```python
def fetch_mailchimp_campaigns(self):
    """Fetch real Mailchimp email campaign data"""
    import mailchimp_marketing as MailchimpMarketing
    
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": "YOUR_MAILCHIMP_API_KEY",
        "server": "us19"  # Change to your region
    })
    
    response = client.campaigns.all(count=100)
    
    campaigns = []
    for campaign in response['campaigns']:
        report = client.reports.get_campaign_details(campaign['id'])
        
        campaigns.append({
            'campaign_id': f"EMAIL_{campaign['id']}",
            'name': campaign['settings']['title'],
            'channel': 'Email',
            'status': campaign['status'],
            'metrics': {
                'impressions': report['emails_sent'],
                'clicks': report['clicks'],
                'conversions': report['conversions'],
                'spend': 0,  # Usually included in subscription
                'revenue': report['revenue']
            }
        })
    
    return campaigns
```

### For ConvertKit:
```python
def fetch_convertkit_campaigns(self):
    """Fetch real ConvertKit data"""
    import requests
    
    headers = {'Authorization': f'Bearer YOUR_CONVERTKIT_API_KEY'}
    
    # Get broadcasts
    response = requests.get(
        'https://api.convertkit.com/v3/broadcasts',
        headers=headers
    )
    
    campaigns = []
    for broadcast in response.json()['broadcasts']:
        campaigns.append({
            'campaign_id': f"CONVERTKIT_{broadcast['id']}",
            'name': broadcast['subject'],
            'channel': 'Email',
            'status': 'active' if broadcast['published_at'] else 'draft',
            'metrics': {
                'impressions': broadcast['subscribers'],
                'clicks': broadcast['click_count'],
                'conversions': broadcast['open_count'],
                'spend': 0,
                'revenue': 0
            }
        })
    
    return campaigns
```

---

## 💰 Option 4: Stripe/Payment Integration

Track actual revenue from campaigns:

```python
def fetch_revenue_by_campaign(self):
    """Get actual revenue from Stripe"""
    import stripe
    
    stripe.api_key = "YOUR_STRIPE_SECRET_KEY"
    
    # Fetch orders with campaign tracking
    charges = stripe.Charge.list(limit=100)
    
    revenue_by_campaign = {}
    
    for charge in charges['data']:
        campaign_id = charge['metadata'].get('campaign_id')
        if campaign_id:
            if campaign_id not in revenue_by_campaign:
                revenue_by_campaign[campaign_id] = 0
            revenue_by_campaign[campaign_id] += charge['amount'] / 100  # Convert from cents
    
    return revenue_by_campaign
```

---

## 🔗 Option 5: UTM Parameter Tracking (Simplest!)

### The Easiest Way to Track Everything:

1. **Add UTM parameters to ALL your campaign links:**
```
https://yoursite.com/?utm_source=facebook&utm_medium=cpc&utm_campaign=summer_sale
https://yoursite.com/?utm_source=google&utm_medium=cpc&utm_campaign=product_launch
https://yoursite.com/?utm_source=email&utm_medium=newsletter&utm_campaign=weekly_01
```

2. **Set up Google Analytics to track these**

3. **Pull data from Google Analytics:**
```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, Dimension

def fetch_analytics_campaigns(self):
    """Fetch campaign data from Google Analytics"""
    client = BetaAnalyticsDataClient()
    
    request = {
        "property": f"properties/YOUR_GA_PROPERTY_ID",
        "date_ranges": [DateRange(start_date="30daysAgo", end_date="today")],
        "dimensions": [Dimension(name="campaignName")],
        "metrics": [
            Metric(name="sessions"),
            Metric(name="conversions"),
            Metric(name="totalRevenue"),
        ],
    }
    
    response = client.run_report(request)
    
    campaigns = []
    for row in response.rows:
        campaigns.append({
            'campaign_id': f"GA_{row.dimension_values[0].value}",
            'name': row.dimension_values[0].value,
            'channel': 'Google Analytics',
            'metrics': {
                'impressions': 0,
                'clicks': int(row.metric_values[0].value),
                'conversions': int(row.metric_values[1].value),
                'spend': 0,
                'revenue': float(row.metric_values[2].value)
            }
        })
    
    return campaigns
```

---

## 🧪 Testing with Real Data - Step by Step

### Step 1: Choose Your Integration
Pick one of the options above based on where you run campaigns.

### Step 2: Get Your API Credentials
```bash
# Store securely in .env file (DON'T commit this!)
FACEBOOK_ACCESS_TOKEN=eaab...
FACEBOOK_ADS_ACCOUNT=act_123...
GOOGLE_CUSTOMER_ID=123-456-7890
MAILCHIMP_API_KEY=xyz...
STRIPE_SECRET_KEY=sk_live_...
```

### Step 3: Install Required Libraries
```bash
pip install requests python-dotenv google-ads mailchimp-marketing stripe
```

### Step 4: Create `.env` file
```
FACEBOOK_ACCESS_TOKEN=your_token_here
GOOGLE_CUSTOMER_ID=your_id_here
MAILCHIMP_API_KEY=your_key_here
```

### Step 5: Update `src/data_collector.py`
Replace simulated data with real API calls.

### Step 6: Test It!
```bash
# First, just collect data
python3 main.py --collect

# Then view it
python3 main.py --summary

# Generate report
python3 main.py --report
```

---

## 🔐 Security Best Practices

### ✅ DO:
- Store API keys in `.env` file
- Add `.env` to `.gitignore`
- Use environment variables
- Rotate tokens regularly
- Use read-only API keys when possible

### ❌ DON'T:
- Hardcode credentials in code
- Commit `.env` to git
- Share API tokens
- Use production keys in testing

### Example: Safe Credentials
```python
import os
from dotenv import load_dotenv

load_dotenv()

FACEBOOK_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
GOOGLE_ID = os.getenv('GOOGLE_CUSTOMER_ID')
```

---

## 📊 Real-Life Example: Complete Setup

### Your Complete Workflow:

```bash
# 1. Create .env file with your credentials
echo "FACEBOOK_ACCESS_TOKEN=eaab123..." > .env
echo "GOOGLE_CUSTOMER_ID=123-456-7890" >> .env

# 2. Install dependencies
pip install -r requirements.txt
pip install requests google-ads mailchimp-marketing python-dotenv

# 3. Update data_collector.py with real API calls

# 4. Initialize database
python3 main.py --init

# 5. Collect real data
python3 main.py --collect

# 6. See your real campaigns!
python3 main.py --summary

# 7. Generate reports
python3 main.py --report

# 8. Schedule daily automatic collection
# Add to crontab: 0 8 * * * cd /path && python3 main.py --auto
```

---

## 🎯 Which Option Should I Choose?

| Channel | Easiest | Most Detailed | Recommended |
|---------|---------|---------------|------------|
| **Facebook** | Google Ads Manager | Official API | Official API |
| **Google Ads** | Google Ads Manager | Official API | Official API |
| **Email** | Mailchimp API | Mailchimp API | Mailchimp API |
| **ALL Channels** | Google Analytics | UTM + Analytics | UTM + Analytics |

---

## 📈 Advanced: Multi-Channel Dashboard

Once you integrate all channels:

```python
# In src/data_collector.py

def collect_all_campaigns(self):
    """Collect from ALL real channels"""
    all_campaigns = []
    
    all_campaigns.extend(self.fetch_facebook_campaigns())
    all_campaigns.extend(self.fetch_google_campaigns())
    all_campaigns.extend(self.fetch_mailchimp_campaigns())
    all_campaigns.extend(self.fetch_analytics_campaigns())
    
    return all_campaigns
```

Then run:
```bash
python3 main.py --collect
python3 main.py --report
python3 main.py --channels  # See all channels side by side!
```

---

## ✅ Checklist for Real Implementation

- [ ] Choose integration method(s)
- [ ] Get API credentials from platform(s)
- [ ] Create `.env` file with credentials
- [ ] Install required Python libraries
- [ ] Update `src/data_collector.py` with real API calls
- [ ] Test with `python3 main.py --collect`
- [ ] View data with `python3 main.py --summary`
- [ ] Set up automated daily collection (cron job)
- [ ] Share reports with team/stakeholders

---

## 🚀 Next Steps

1. **Pick your platform** (Facebook, Google, Email, etc.)
2. **Get API credentials** from that platform
3. **Install libraries**: `pip install requests google-ads`
4. **Update data_collector.py** with real API calls
5. **Test it**: `python3 main.py --collect`
6. **Monitor real campaigns**: `python3 main.py --dashboard`

Your tracker will then **automatically pull real data** from your campaigns and generate insights!

---

**Questions?** Each integration is slightly different, but the pattern is the same:
1. Get credentials
2. Connect to API
3. Fetch data
4. Parse into tracker format
5. Profit! 📈
