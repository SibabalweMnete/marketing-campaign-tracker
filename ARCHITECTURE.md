# 🏗️ Architecture Guide - How It All Works

## System Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    YOUR MARKETING PLATFORMS                      │
├──────────────────────────────────────────────────────────────────┤
│  📱 Facebook Ads  │  🔍 Google Ads  │  📧 Email  │  📊 Analytics │
└─────────┬────────────────┬────────────────┬────────────────┬─────┘
          │                │                │                │
          │ API Requests   │ API Requests   │ API Requests   │
          ▼                ▼                ▼                ▼
┌──────────────────────────────────────────────────────────────────┐
│           src/data_collector.py (Data Collection Layer)          │
├──────────────────────────────────────────────────────────────────┤
│  • fetch_facebook_campaigns()                                    │
│  • fetch_google_campaigns()                                      │
│  • fetch_email_campaigns()                                       │
│  • fetch_analytics_campaigns()                                   │
│  • collect_all_campaigns() ← Main entry point                    │
└─────────────────────────────┬──────────────────────────────────┘
                              │
                    Campaign Data Objects
                    (with metrics)
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│          src/database.py (Data Storage Layer)                    │
├──────────────────────────────────────────────────────────────────┤
│  SQLite Database: data/campaigns.db                              │
│  ├─ campaigns table (campaign info)                              │
│  └─ metrics table (performance metrics)                          │
└─────────────────────────────┬──────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│          src/analyzer.py (Analysis Layer)                        │
├──────────────────────────────────────────────────────────────────┤
│  • calculate_roi()                                               │
│  • calculate_ctr()                                               │
│  • calculate_conversion_rate()                                   │
│  • get_campaign_summary()                                        │
└─────────────────────────────┬──────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│         Report/View Generation Layers                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📊 ReportGenerator          📺 Dashboard        ⚖️  Comparator │
│  ├─ Daily Reports           ├─ Live View       ├─ Compare      │
│  ├─ CSV Export              ├─ Summary View    ├─ Channels     │
│  ├─ JSON Export             └─ Progress Bars   └─ Efficiency   │
│  └─ Insights                                                    │
│                                                                  │
└─────────────────────────────┬──────────────────────────────────┘
                              │
                ┌─────────────┴──────────────┐
                ▼                            ▼
        ┌──────────────────┐       ┌──────────────────┐
        │ Console Output   │       │ File Exports     │
        │ • Reports        │       │ • CSV file       │
        │ • Dashboard      │       │ • JSON file      │
        │ • Insights       │       │ • Database       │
        └──────────────────┘       └──────────────────┘
```

---

## File Structure & Dependencies

```
marketing-campaign-tracker/
│
├── main.py                          ← Entry point (CLI interface)
│   └─ imports: all modules below
│
├── src/
│   ├── database.py                  ← SQLite operations
│   │   └─ Stores/retrieves campaign data
│   │
│   ├── data_collector.py            ← API calls to platforms
│   │   └─ Fetches: Facebook, Google, Email, Analytics
│   │
│   ├── analyzer.py                  ← Calculations & analysis
│   │   └─ ROI, CTR, Conversion rates
│   │
│   ├── report_generator.py          ← Reports & exports
│   │   ├─ Daily reports
│   │   ├─ CSV export
│   │   ├─ JSON export
│   │   └─ Insights generation
│   │
│   ├── dashboard.py                 ← Live dashboards
│   │   ├─ Real-time dashboard
│   │   ├─ Summary view
│   │   └─ Visual indicators
│   │
│   └── comparator.py                ← Campaign comparison
│       ├─ Campaign comparison
│       ├─ Channel analysis
│       └─ Efficiency metrics
│
├── data/
│   └── campaigns.db                 ← SQLite database (auto-created)
│
├── reports/
│   ├── campaign_performance.csv     ← Excel export
│   └── campaign_data.json           ← API-ready export
│
└── .env                             ← API credentials (NOT in git!)
```

---

## Data Flow: From API to Report

### Step 1: Data Collection
```
User runs: python3 main.py --collect
         │
         ▼
main.py calls DataCollector.collect_all_campaigns()
         │
         ├─ fetch_facebook_campaigns()  ──→ Makes API call to Facebook
         ├─ fetch_google_campaigns()    ──→ Makes API call to Google
         ├─ fetch_email_campaigns()     ──→ Makes API call to Email Service
         └─ fetch_analytics_campaigns() ──→ Makes API call to Analytics
         │
         ▼
Returns list of campaign objects with metrics
```

### Step 2: Data Storage
```
Campaign objects
         │
         ▼
database.py insert_campaign() ──→ Stores campaign info in DB
         │
         ├─ campaign_id, name, channel, budget, status
         │
         └─ Related metrics rows in metrics table
                     │
                     ├─ impressions, clicks, conversions
                     ├─ spend, revenue, date
                     └─ (time-series data)
```

### Step 3: Analysis
```
User runs: python3 main.py --report
         │
         ▼
analyzer.py (for each campaign):
         │
         ├─ get_campaign_summary()
         │   ├─ calculate_roi()
         │   ├─ calculate_ctr()
         │   └─ calculate_conversion_rate()
         │
         └─ Returns: {roi, ctr, conversion_rate, spend, revenue}
```

### Step 4: Report Generation
```
report_generator.py receives analysis data
         │
         ├─ generate_daily_report()    ──→ Pretty console output
         │
         ├─ export_to_csv()            ──→ reports/campaign_performance.csv
         │
         ├─ export_to_json()           ──→ reports/campaign_data.json
         │
         └─ generate_insights()        ──→ Smart recommendations
```

---

## Class Structure

### CampaignDatabase
```python
class CampaignDatabase:
    - init_database()           # Create tables
    - insert_campaign()         # Add campaign
    - insert_metrics()          # Add metrics
    - get_all_campaigns()       # List all
    - get_campaign_metrics()    # Get campaign data
```

### DataCollector
```python
class DataCollector:
    - fetch_facebook_campaigns()    # Get FB data
    - fetch_google_campaigns()      # Get Google data
    - fetch_email_campaigns()       # Get Email data
    - fetch_analytics_campaigns()   # Get Analytics data
    - collect_all_campaigns()       # Main method
```

### CampaignAnalyzer
```python
class CampaignAnalyzer:
    - calculate_roi()               # ROI calculation
    - calculate_ctr()               # CTR calculation
    - calculate_conversion_rate()   # Conversion calc
    - get_campaign_summary()        # Full analysis
```

### ReportGenerator
```python
class ReportGenerator:
    - generate_daily_report()       # Console report
    - export_to_csv()               # CSV export
    - export_to_json()              # JSON export
    - generate_insights()           # AI insights
```

### Dashboard
```python
class Dashboard:
    - live_dashboard()              # Real-time view
    - summary_view()                # Static summary
    - display_campaign_card()       # Visual card
    - render_progress_bar()         # Visual bar
```

### CampaignComparator
```python
class CampaignComparator:
    - compare_campaigns()           # Compare specific
    - compare_by_channel()          # Channel analysis
    - efficiency_report()           # Cost metrics
```

---

## Database Schema

### campaigns table
```sql
CREATE TABLE campaigns (
    campaign_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    channel TEXT NOT NULL,        -- Facebook, Google, Email, etc.
    start_date DATE,
    end_date DATE,
    budget REAL,
    status TEXT                   -- active, paused, completed
)
```

### metrics table
```sql
CREATE TABLE metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id TEXT,             -- Foreign key to campaigns
    date DATE,                    -- When data was collected
    impressions INTEGER,
    clicks INTEGER,
    conversions INTEGER,
    spend REAL,                   -- How much was spent
    revenue REAL                  -- How much was earned
)
```

---

## Command Flow

### Command: `python3 main.py --collect`
```
main() ─────┐
    parser ─┼─ args = parser.parse_args()
            │
            ├─ if args.collect:
            │   ├─ DataCollector.collect_all_campaigns()
            │   └─ db.insert_campaign() + db.insert_metrics()
            │
            └─ Print success message
```

### Command: `python3 main.py --report`
```
main() ─────┐
    parser ─┼─ args = parser.parse_args()
            │
            ├─ if args.report:
            │   ├─ analyzer = CampaignAnalyzer()
            │   ├─ report_gen = ReportGenerator()
            │   │
            │   ├─ report_gen.generate_daily_report()    → Console
            │   ├─ report_gen.generate_insights()        → Console
            │   ├─ report_gen.export_to_csv()            → File
            │   └─ report_gen.export_to_json()           → File
            │
            └─ Print completion message
```

### Command: `python3 main.py --auto`
```
main() ─────┐
    parser ─┼─ args = parser.parse_args()
            │
            ├─ if args.auto:
            │   ├─ collect_all_campaigns()
            │   ├─ generate_daily_report()
            │   ├─ generate_insights()
            │   ├─ export_to_csv()
            │   └─ export_to_json()
            │
            └─ Print: "🎉 Full reporting suite generated successfully!"
```

---

## Data Types & Formats

### Campaign Object (from API)
```python
{
    'campaign_id': 'FB_001',
    'name': 'Summer Sale 2024',
    'channel': 'Facebook',
    'start_date': '2024-06-01',
    'end_date': '2024-12-31',
    'budget': 10000.00,
    'status': 'active',
    'metrics': {
        'impressions': 125000,
        'clicks': 3200,
        'conversions': 180,
        'spend': 8500.00,
        'revenue': 27200.00
    }
}
```

### Summary Object (from Analyzer)
```python
{
    'roi': 220.0,                    # Percent
    'ctr': 2.56,                     # Percent
    'conversion_rate': 5.62,         # Percent
    'total_spend': 8500.00,          # Currency
    'total_revenue': 27200.00,       # Currency
    'total_conversions': 180         # Count
}
```

### CSV Row Format
```csv
campaign_id,name,channel,status,roi,ctr,conversion_rate,total_spend,total_revenue,total_conversions
FB_001,Summer Sale 2024,Facebook,active,220.00%,2.56%,5.62%,"R8,500.00","R27,200.00",180
```

### JSON Export Format
```json
{
  "generated_at": "2024-12-06T19:15:00",
  "total_campaigns": 4,
  "campaigns": [
    {
      "campaign_id": "FB_001",
      "name": "Summer Sale 2024",
      "metrics": {
        "roi_percent": 220.0,
        "ctr_percent": 2.56
      }
    }
  ],
  "summary": {
    "overall_roi_percent": 193.0
  }
}
```

---

## Integration Points (For Real Data)

### To Add Facebook Ads:
1. User gets Access Token from Facebook
2. Update `.env` with token
3. In `data_collector.py`, replace `fetch_facebook_campaigns()`
4. Use Facebook Business SDK to call API
5. Parse response into campaign objects
6. Return list of campaigns

### Pattern for Any Platform:
```python
def fetch_xyz_platform(self):
    """Fetch from XYZ platform"""
    
    # 1. Get credentials
    token = os.getenv('XYZ_API_TOKEN')
    
    # 2. Make API call
    response = requests.get(
        'https://api.xyz.com/campaigns',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    # 3. Parse response
    campaigns = []
    for item in response.json():
        campaigns.append({
            'campaign_id': f"XYZ_{item['id']}",
            'name': item['name'],
            'channel': 'XYZ Platform',
            'metrics': {
                'impressions': item['impressions'],
                'clicks': item['clicks'],
                'conversions': item['conversions'],
                'spend': item['spend'],
                'revenue': item['revenue']
            }
        })
    
    # 4. Return campaigns
    return campaigns
```

---

## Performance Considerations

### Database Queries
- `get_all_campaigns()` - O(n) where n = number of campaigns
- `get_campaign_metrics()` - O(m) where m = number of metrics rows
- Consider indexing if > 100,000 metrics rows

### API Calls
- Each `--collect` makes up to 4 API calls (one per platform)
- Each platform might take 1-5 seconds
- Total collection time: ~5-20 seconds per run

### Report Generation
- CSV export: O(n) - scales with campaigns
- JSON export: O(n * m) - scales with campaigns and metrics
- Typical execution: < 1 second for < 1000 campaigns

---

## Error Handling

### API Failure Handling
```python
try:
    campaigns = fetch_facebook_campaigns()
except Exception as e:
    print(f"❌ Error: {e}")
    print("Using demo data instead...")
    return []  # Falls back to simulated data
```

### Database Error Handling
```python
try:
    conn = sqlite3.connect(self.db_path)
except sqlite3.Error as e:
    print(f"❌ Database error: {e}")
    # Appropriate error recovery
```

---

## Scaling Considerations

### For 10+ Campaigns
- ✅ Current system works fine
- Database remains fast
- Reports generate in < 1 second

### For 100+ Campaigns
- ✅ Still works well
- Consider adding database indexing
- Reports might take 2-3 seconds

### For 1000+ Campaigns
- ⚠️ Might need optimization
- Consider pagination for API calls
- Archive old metrics data
- Optimize database queries

---

## Security Architecture

```
┌────────────────────────────────────┐
│  main.py (Entrypoint)              │
│  • No hardcoded credentials        │
│  • Uses environment variables      │
└────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│  .env file (Local, NOT in git)     │
│  • API tokens                      │
│  • Credentials                     │
│  • Database passwords              │
└────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│  src/data_collector.py             │
│  • Loads from environment          │
│  • Never logs credentials          │
│  • Secure API calls                │
└────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│  Credentials are never exposed     │
│  • Not in console output           │
│  • Not in logs                     │
│  • Not in exported files           │
└────────────────────────────────────┘
```

---

This architecture is scalable, maintainable, and ready for real-world use! 🚀

