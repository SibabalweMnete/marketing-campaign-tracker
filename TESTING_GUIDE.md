# 🧪 Testing Guide - From Demo to Real Campaigns

## Quick Overview

Your tracker works with **two types of data**:

1. **Demo Mode (Current)** - Simulated data for testing
2. **Production Mode (Real)** - Actual campaign data from your platforms

---

## 🎮 Phase 1: Test with Demo Data (Right Now!)

You're already here! The demo uses fake but realistic data.

### What You Can Do Right Now:

```bash
# See how reports look
python3 main.py --report

# Test the dashboard
python3 main.py --dashboard

# Check comparisons
python3 main.py --compare

# View efficiency
python3 main.py --efficiency

# Try insights
python3 main.py --insights

# Export to files
python3 main.py --auto
```

**Purpose:** Understand the tool before connecting real data

---

## 📊 Phase 2: Connect to ONE Real Platform

### Quickest Setup: Google Analytics + UTM Parameters

This is the **easiest way** to start tracking real campaigns!

### Step 1: Add UTM Codes to Your Links

Change your links from:
```
https://yoursite.com
```

To:
```
https://yoursite.com/?utm_source=facebook&utm_medium=cpc&utm_campaign=summer_sale
https://yoursite.com/?utm_source=google&utm_medium=cpc&utm_campaign=product_launch
https://yoursite.com/?utm_source=email&utm_medium=newsletter&utm_campaign=weekly
```

### Step 2: Create .env File

```bash
# In your project root directory
cat > .env << EOF
GOOGLE_ANALYTICS_PROPERTY_ID=123456789
EOF
```

### Step 3: Update data_collector.py

Find this section:
```python
def fetch_google_campaigns(self):
    """Simulate Google Ads API call"""
    print("🔍 Fetching Google Ads campaign data...")
```

Replace it with:
```python
def fetch_google_campaigns(self):
    """Fetch REAL Google Analytics data"""
    print("🔍 Fetching real Google Analytics data...")
    
    import os
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import DateRange, Metric, Dimension
    
    try:
        client = BetaAnalyticsDataClient()
        property_id = os.getenv('GOOGLE_ANALYTICS_PROPERTY_ID')
        
        request = {
            "property": f"properties/{property_id}",
            "date_ranges": [DateRange(start_date="7daysAgo", end_date="today")],
            "dimensions": [Dimension(name="campaignName")],
            "metrics": [
                Metric(name="sessions"),
                Metric(name="conversions"),
                Metric(name="totalRevenue"),
            ],
        }
        
        response = client.run_report(request)
        
        campaigns = []
        if response.rows:
            for row in response.rows:
                campaign_name = row.dimension_values[0].value
                sessions = int(row.metric_values[0].value) if row.metric_values[0].value else 0
                conversions = int(row.metric_values[1].value) if row.metric_values[1].value else 0
                revenue = float(row.metric_values[2].value) if row.metric_values[2].value else 0
                
                campaigns.append({
                    'campaign_id': f"GA_{campaign_name}",
                    'name': campaign_name,
                    'channel': 'Google Analytics',
                    'start_date': '2024-01-01',
                    'end_date': '2024-12-31',
                    'budget': revenue / 2,  # Estimate
                    'status': 'active',
                    'metrics': {
                        'impressions': sessions * 10,  # Estimate
                        'clicks': sessions,
                        'conversions': conversions,
                        'spend': revenue / 2,  # Rough estimate
                        'revenue': revenue
                    }
                })
            
            print(f"✅ Collected {len(campaigns)} real campaigns from Google Analytics")
            return campaigns
        else:
            print("⚠️ No data in Google Analytics (check your property ID)")
            return []
    
    except Exception as e:
        print(f"❌ Error connecting to Google Analytics: {e}")
        print("   Using demo data instead...")
        return []  # Falls back to demo data
```

### Step 4: Install Required Library

```bash
pip install google-analytics-data
```

### Step 5: Test It!

```bash
python3 main.py --collect
python3 main.py --summary
```

**That's it!** Now you're tracking real campaign data! 🎉

---

## 🐦 Phase 3: Add More Platforms

Once you're comfortable with Google Analytics, add more:

### Facebook (Moderate Difficulty)

```bash
pip install facebook-business python-dotenv
```

Create `.env`:
```
FACEBOOK_ACCESS_TOKEN=eaab123...
FACEBOOK_ADS_ACCOUNT=act_123456
```

Update data_collector.py:
```python
def fetch_facebook_campaigns(self):
    """Fetch REAL Facebook Ads data"""
    import os
    from facebook_business.api import FacebookAdsApi
    from facebook_business.adobjects.campaign import Campaign
    
    try:
        access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        app_secret = os.getenv('FACEBOOK_APP_SECRET')
        app_id = os.getenv('FACEBOOK_APP_ID')
        ad_account_id = os.getenv('FACEBOOK_ADS_ACCOUNT')
        
        FacebookAdsApi.init(access_token=access_token)
        account = Account(ad_account_id)
        campaigns = account.get_campaigns(fields=[
            Campaign.Field.id,
            Campaign.Field.name,
            Campaign.Field.status,
            Campaign.Field.daily_budget,
        ])
        
        result_campaigns = []
        for campaign in campaigns:
            insights = campaign.get_insights(fields=[
                'impressions', 'clicks', 'spend', 'actions'
            ])
            
            if insights:
                insight = insights[0]
                result_campaigns.append({
                    'campaign_id': f"FB_{campaign[Campaign.Field.id]}",
                    'name': campaign[Campaign.Field.name],
                    'channel': 'Facebook',
                    'status': campaign[Campaign.Field.status],
                    'budget': campaign[Campaign.Field.daily_budget] / 100,
                    'metrics': {
                        'impressions': int(insight.get('impressions', 0)),
                        'clicks': int(insight.get('clicks', 0)),
                        'conversions': int(insight.get('actions', [{}])[0].get('value', 0) if insight.get('actions') else 0),
                        'spend': float(insight.get('spend', 0)),
                        'revenue': 0
                    }
                })
        
        print(f"✅ Collected {len(result_campaigns)} Facebook campaigns")
        return result_campaigns
    
    except Exception as e:
        print(f"❌ Error with Facebook: {e}")
        return []
```

---

## 🧪 Testing Workflow

### Day 1: Setup Demo
```bash
python3 main.py --init
python3 main.py --collect
python3 main.py --summary
```
✅ Understand how tool works

### Day 2: Connect First Real Platform
```bash
# Update .env with credentials
# Update data_collector.py with one real API
python3 main.py --collect
python3 main.py --summary
```
✅ See real data flowing in

### Week 1: Monitor Real Data
```bash
# Run daily
python3 main.py --auto
```
✅ Get comfortable with real insights

### Week 2: Add More Platforms
```bash
# Update data_collector.py for 2nd platform
python3 main.py --collect
python3 main.py --channels
```
✅ Compare across channels

---

## 🔄 Full Integration Timeline

### Week 1: Setup
- [ ] Understand the demo tool
- [ ] Read REAL_CAMPAIGNS.md
- [ ] Get API credentials from one platform
- [ ] Connect first platform

### Week 2: Monitor
- [ ] Collect real data daily
- [ ] Review reports
- [ ] Check insights
- [ ] Verify accuracy

### Week 3: Scale
- [ ] Connect second platform
- [ ] Connect third platform
- [ ] Set up daily automation
- [ ] Share with team

### Week 4: Optimize
- [ ] Use insights for decisions
- [ ] Adjust budgets
- [ ] Scale winners
- [ ] Optimize losers

---

## 🎯 Testing Checklist

### Demo Phase
- [ ] Run `--summary` 
- [ ] Run `--report`
- [ ] Run `--dashboard`
- [ ] Run `--insights`
- [ ] View CSV export
- [ ] View JSON export

### Real Data Phase
- [ ] Create .env file
- [ ] Get API credentials
- [ ] Update data_collector.py
- [ ] Install required libraries
- [ ] Run `--collect`
- [ ] Verify data appears
- [ ] Check `--summary`
- [ ] Review reports

### Production Phase
- [ ] Set up cron job for daily collection
- [ ] Monitor for errors
- [ ] Share reports with team
- [ ] Make budget decisions
- [ ] Adjust campaigns based on insights

---

## ⚠️ Common Issues & Solutions

### Issue: "No data collected"
```bash
# Check your API credentials
cat .env

# Verify they're correct
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('YOUR_KEY'))"
```

### Issue: "Permission denied" on API
```bash
# Make sure your API token has the right permissions
# Usually needs: campaigns:read, insights:read, ads_management:read
```

### Issue: "Module not found"
```bash
# Install missing libraries
pip install google-analytics-data facebook-business requests
```

### Issue: "Getting demo data instead of real"
```bash
# Your real API call failed, falling back to demo
# Check error messages in console
# Verify credentials in .env
```

---

## 📈 Real Data Example Output

Once connected, you'll see:

```
🟢 Summer Sale 2024
   Channel: Facebook
   Spend: R34,000.00 → Revenue: R108,800.00
   ROI: 220% | Conversion Rate: 5.62%
   Performance: [████████████░░] 110%
```

Instead of simulated data! ✅

---

## 🚀 Start Simple, Then Expand

**Recommended Path:**

1. **Week 1:** Test with demo data
2. **Week 2:** Add Google Analytics (easiest)
3. **Week 3:** Add Facebook Ads
4. **Week 4:** Add Google Ads
5. **Week 5+:** Add Email, Stripe, etc.

---

## 💡 Pro Tips

✅ **Start with Google Analytics** - Easiest integration  
✅ **Use UTM parameters** - Required for GA tracking  
✅ **Test one platform first** - Before adding others  
✅ **Keep demo mode for testing** - Keep simulated data option  
✅ **Store credentials in .env** - Never hardcode!  
✅ **Run daily collection** - Automate with cron  
✅ **Check for errors** - Monitor integration weekly  

---

## 📞 Quick Reference

### Get API Credentials

| Platform | Where to Get | Difficulty |
|----------|-------------|-----------|
| Google Analytics | Google Cloud Console | 🟡 Medium |
| Facebook Ads | Facebook Business Manager | 🟡 Medium |
| Google Ads | Google Ads Account | 🟡 Medium |
| Mailchimp | Account Settings | 🟢 Easy |
| Stripe | Account Settings | 🟢 Easy |

---

## ✅ You're Ready!

Start with the demo, then gradually add real platforms. Your tracker will grow with your needs!

**Next Step:** Read `REAL_CAMPAIGNS.md` for detailed integration steps.

