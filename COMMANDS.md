# 🎛️ Command Reference Guide

Complete list of all available commands for your Marketing Campaign Tracker.

---

## 🚀 Setup Commands

### Initialize Database
```bash
python3 main.py --init
```
**Purpose:** Create the SQLite database and initialize all tables  
**Output:** Database file at `data/campaigns.db`  
**Run:** Once per project setup

---

### Collect Campaign Data
```bash
python3 main.py --collect
```
**Purpose:** Fetch campaign data from all marketing channels  
**Sources:** Facebook, Google Ads, Email Marketing  
**Output:** Data stored in database  
**Run:** Daily/weekly as needed

---

## 📊 Reporting Commands

### Full Reporting Suite
```bash
python3 main.py --report
```
**Purpose:** Generate comprehensive performance analysis  
**Output:**
- Console: Daily performance report
- Console: Intelligent insights & recommendations
- File: `reports/campaign_performance.csv`
- File: `reports/campaign_data.json`  
**Run:** Weekly for stakeholder updates

---

### Insights & Recommendations
```bash
python3 main.py --insights
```
**Purpose:** Get AI-powered recommendations  
**Shows:**
- 💡 Scaling opportunities for top performers
- ⚠️ Optimization alerts for underperformers
- 📊 Channel performance analysis  
**Run:** When making budget allocation decisions

---

## 📈 Dashboard & Views

### Live Dashboard
```bash
python3 main.py --dashboard
```
**Purpose:** Monitor campaigns in real-time  
**Features:**
- 🔄 Auto-refreshes every 3 seconds
- 🟢🟡🔴 Color-coded status
- 📊 Live metrics
- ⏱️ Runs for 60 seconds  
**Run:** Monitor active campaigns  
**Exit:** Press Ctrl+C

---

### Portfolio Summary
```bash
python3 main.py --summary
```
**Purpose:** Quick snapshot of all campaigns  
**Shows:**
- All campaigns with metrics
- Color-coded performance
- Total spend & revenue
- Overall ROI & net profit  
**Run:** Daily check-ins (10 seconds)

---

## 🔍 Analysis Commands

### Compare All Campaigns
```bash
python3 main.py --compare
```
**Purpose:** Side-by-side comparison of all campaigns  
**Shows:**
- Performance metrics table
- Detailed metrics breakdown
- Cost per conversion
- Revenue per ad spend  
**Run:** Weekly analysis

---

### Compare Specific Campaigns
```bash
python3 main.py --compare FB_001 GOOGLE_001 EMAIL_001
```
**Purpose:** Compare selected campaigns  
**Args:** Space-separated campaign IDs  
**Shows:** Same as above but filtered  
**Run:** When analyzing specific campaigns

---

### Channel Performance Analysis
```bash
python3 main.py --channels
```
**Purpose:** Compare performance across marketing channels  
**Shows:**
- Average ROI by channel
- Total campaigns per channel
- Channel recommendations
- Best vs underperforming channels  
**Run:** Budget allocation planning

---

### Efficiency Metrics
```bash
python3 main.py --efficiency
```
**Purpose:** Cost optimization analysis  
**Shows:**
- Cost per conversion (lower = better)
- Revenue per ad spend (higher = better)
- Efficiency ranking  
**Run:** Optimize campaign spending

---

## 🤖 Automation Commands

### Full Automated Workflow
```bash
python3 main.py --auto
```
**Purpose:** Run everything in one command  
**Does:**
1. Collects data from all channels
2. Analyzes performance
3. Generates daily report
4. Creates insights
5. Exports to CSV & JSON  
**Run:** Schedule as daily cron job

---

## 📅 Scheduling Examples

### Daily Reports (8 AM)
```bash
# Add to crontab: crontab -e
0 8 * * * cd /path/to/project && python3 main.py --auto
```

### Weekly Deep Dive (Monday 9 AM)
```bash
0 9 * * 1 cd /path/to/project && python3 main.py --report
```

### Hourly Efficiency Check
```bash
0 * * * * cd /path/to/project && python3 main.py --efficiency
```

### Live Monitoring (Every hour)
```bash
0 * * * * cd /path/to/project && python3 main.py --summary
```

---

## 🎯 Common Workflows

### Morning Routine (2 minutes)
```bash
python3 main.py --summary     # Quick check
python3 main.py --dashboard   # Monitor for 60 seconds
```

### Budget Optimization (5 minutes)
```bash
python3 main.py --channels    # Best channels
python3 main.py --efficiency  # Cost analysis
python3 main.py --insights    # Recommendations
```

### Stakeholder Report (3 minutes)
```bash
python3 main.py --report      # Generate report
# Share: reports/campaign_performance.csv
```

### Campaign Deep Dive (10 minutes)
```bash
python3 main.py --compare     # Compare all
python3 main.py --channels    # By channel
python3 main.py --efficiency  # Efficiency
python3 main.py --insights    # Insights
```

---

## 📁 Generated Files

### Automatically Created
```
reports/
├── campaign_performance.csv  # Excel-ready spreadsheet
└── campaign_data.json       # JSON data format

data/
└── campaigns.db             # SQLite database
```

### Share with Stakeholders
- **CSV**: Open in Excel/Google Sheets
- **JSON**: Use in APIs or dashboards
- **Console output**: Copy-paste to reports

---

## 🎨 Output Format Examples

### Report Output
```
📈 Overall Performance:
Total Campaigns: 4
Active Campaigns: 4
Total Spend: R107,200.00
Total Revenue: R314,340.00
Overall ROI: 193%

🔥 Top Performing Campaigns:
1. "Newsletter Campaign" (Email)
   - ROI: 394% | Spend: R7,200 | Revenue: R35,600
```

### Dashboard Output
```
🟢 Summer Sale 2024
   Channel: Facebook
   Spend: R34,000.00 → Revenue: R108,800.00
   ROI: 220.0% | Conversion Rate: 5.62%
   Performance: [████████████████████] 110%
```

### Comparison Output
```
Campaign                  Channel       ROI        CTR        Conv Rate   Spend
🥇 Newsletter Campaign   Email         394.4%     6.22%      7.86%       R7,200
   Summer Sale 2024      Facebook      220.0%     2.56%      5.62%       R34,000
```

---

## 💡 Tips & Tricks

### Combine Commands
```bash
# Get insights then export
python3 main.py --insights && python3 main.py --report
```

### Save Output to File
```bash
python3 main.py --report > daily_report.txt
```

### Quick Export
```bash
python3 main.py --auto > /dev/null
# CSV and JSON already exported
```

### Monitor Multiple Times
```bash
python3 main.py --summary && python3 main.py --dashboard
```

---

## 🔧 Troubleshooting

### Database Error
```bash
# Reinitialize
python3 main.py --init
```

### No Data
```bash
# Collect first
python3 main.py --collect
```

### Export Missing
```bash
# They're created by --report or --auto
python3 main.py --report
# Check: reports/ folder
```

---

## 📊 Metrics Reference

| Metric | Formula | Example |
|--------|---------|---------|
| ROI | (Revenue - Spend) / Spend × 100 | 220% |
| CTR | Clicks / Impressions × 100 | 2.56% |
| Conversion Rate | Conversions / Clicks × 100 | 5.62% |
| Cost per Conversion | Total Spend / Conversions | R47.22 |
| Revenue per Spend | Total Revenue / Spend | 3.2x |

---

## ✨ Pro Tips

✅ **Automate Everything** - Use `--auto` in cron  
✅ **Daily Summary** - Takes 10 seconds  
✅ **Weekly Report** - Get stakeholder-ready exports  
✅ **Live Monitor** - Use dashboard during campaigns  
✅ **Share CSV** - Works with Excel/Sheets  
✅ **Schedule Emails** - Use cron + mail command  

---

**Last Updated:** December 6, 2025
