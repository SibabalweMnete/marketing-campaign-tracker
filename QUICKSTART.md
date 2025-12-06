# 🎯 Quick Start Guide - Marketing Campaign Tracker

## Getting Started

### 1️⃣ First Time Setup
```bash
python3 main.py --init
```
This creates the SQLite database and initializes all tables.

### 2️⃣ Collect Campaign Data
```bash
python3 main.py --collect
```
Simulates collecting data from:
- 📱 Facebook Ads
- 🔍 Google Ads
- 📧 Email Marketing
- And more!

---

## 📊 View Your Data

### Quick Summary (Best for Daily Check-ins)
```bash
python3 main.py --summary
```
Shows all campaigns with:
- ✅ Real-time metrics
- 📊 Visual performance bars
- 💰 Total spend & revenue
- 🎯 Overall ROI

Output example:
```
🟢 Newsletter Campaign
   Channel: Email
   Spend: R7,200.00 → Revenue: R35,600.00
   ROI: 394.4% | Conversion Rate: 7.86%
```

### Live Dashboard (Best for Monitoring)
```bash
python3 main.py --dashboard
```
- 🔄 Auto-refreshes every 3 seconds
- 🟢🟡🔴 Color-coded status
- 📈 Live portfolio metrics
- ⏱️ Runs for 60 seconds (Ctrl+C to exit)

---

## 📈 Generate Reports

### Full Reporting Suite
```bash
python3 main.py --report
```
Generates:
1. **Console Report** - Daily performance summary
2. **Insights** - Scaling opportunities & optimization alerts
3. **CSV Export** - `reports/campaign_performance.csv`
4. **JSON Export** - `reports/campaign_data.json`

### Insights Only
```bash
python3 main.py --insights
```
Get AI-powered recommendations:
- 💡 Scaling opportunities for top performers
- ⚠️ Optimization alerts for underperformers
- 📊 Channel performance analysis

---

## 🤖 Automated Everything
```bash
python3 main.py --auto
```
Runs the complete workflow:
1. Collects data from all channels
2. Analyzes performance
3. Generates daily report
4. Creates insights
5. Exports to CSV & JSON

Perfect for scheduling as a daily cron job!

---

## 📁 Output Files

After running reports, check:
- `reports/campaign_performance.csv` - Excel-ready performance data
- `reports/campaign_data.json` - Full metrics in JSON format
- `data/campaigns.db` - SQLite database

---

## 🎯 Key Metrics Explained

| Metric | Meaning |
|--------|---------|
| **ROI** | Return on Investment % = (Revenue - Spend) / Spend × 100 |
| **CTR** | Click-Through Rate % = Clicks / Impressions × 100 |
| **Conversion Rate** | % = Conversions / Clicks × 100 |
| **Overall ROI** | Average ROI across all campaigns |

---

## 🌟 Pro Tips

✅ **Daily Routine:**
```bash
python3 main.py --summary  # 10-second check-in
```

✅ **Weekly Analysis:**
```bash
python3 main.py --report   # Full deep dive
```

✅ **Monitor Campaigns:**
```bash
python3 main.py --dashboard  # Live dashboard
```

✅ **Share with Stakeholders:**
- Send the CSV or JSON files from `reports/` folder
- Include the console report output

✅ **Schedule Automation:**
```bash
# Add to crontab for daily reports at 8 AM
0 8 * * * cd /path/to/marketing-campaign-tracker && python3 main.py --auto
```

---

## 🚀 What Makes This Cool?

✨ **One Command Reports** - No manual Excel work!  
✨ **Smart Insights** - AI-powered recommendations  
✨ **Live Dashboard** - Monitor campaigns in real-time  
✨ **Multi-Format Export** - CSV for Excel, JSON for APIs  
✨ **Performance Tracking** - ROI, CTR, Conversion rates  
✨ **Zero Dependencies** - Pure Python, no bloat  

Enjoy! 🎉
