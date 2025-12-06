# 🚀 Marketing Campaign Tracker
**Automated marketing analytics pipeline reducing reporting time by 8 hours/week**

---

## ✨ Features

### 📊 Core Analytics
- **Multi-channel campaign tracking** (Facebook, Google Ads, Email, etc.)
- **Real-time performance metrics** (ROI, CTR, Conversion Rate)
- **Automated database management** using SQLite
- **Comprehensive performance analysis** with intelligent insights

### 📈 Advanced Reporting
- **Daily performance reports** with visual formatting
- **CSV export** for Excel analysis and stakeholder sharing
- **JSON export** for API integration and data processing
- **Intelligent recommendations** based on campaign performance

### 📺 Interactive Dashboard
- **Live real-time dashboard** with auto-refresh
- **Portfolio summary view** with health metrics
- **Visual progress bars** and status indicators
- **Color-coded performance** (Green/Yellow/Red status)

### 🧠 Smart Insights
- **Campaign scaling recommendations** for top performers
- **Optimization alerts** for underperforming campaigns
- **Channel performance analysis** across all marketing platforms
- **ROI-based decision support**

---

## 🛠️ Installation & Usage

### Setup
```bash
# Initialize the database
python main.py --init

# Collect campaign data from all channels
python main.py --collect

# Generate full reporting suite
python main.py --report

# Run everything at once (collect + report)
python main.py --auto
```

### Dashboard & Analytics
```bash
# View live updating dashboard
python main.py --dashboard

# View quick portfolio summary
python main.py --summary

# Generate insights and recommendations
python main.py --insights
```

### Exported Files
- `reports/campaign_performance.csv` - Performance metrics in CSV format
- `reports/campaign_data.json` - Full campaign data in JSON format
- `data/campaigns.db` - SQLite database with all campaign data

---

## 📁 Project Structure
```
marketing-campaign-tracker/
├── main.py                 # Application entry point
├── requirements.txt        # Dependencies
├── data/                   # Data storage
│   └── campaigns.db       # SQLite database
├── reports/               # Export outputs
│   ├── daily/
│   ├── campaign_performance.csv
│   └── campaign_data.json
└── src/
    ├── dashboard.py       # Live dashboard & visualization
    ├── report_generator.py # Report creation & exports
    ├── analyzer.py        # Performance analysis
    ├── data_collector.py  # Data collection
    └── database.py        # Database operations
```

---

## 📊 Metrics Tracked
- **Impressions** - Total ad impressions
- **Clicks** - Click-through count
- **Conversions** - Number of conversions
- **Spend** - Campaign budget spent
- **Revenue** - Generated revenue
- **ROI** - Return on investment percentage
- **CTR** - Click-through rate
- **Conversion Rate** - Conversion percentage

---

## 🎯 Key Insights Generated
✅ **Top performers** - Campaigns exceeding targets  
⚠️ **Scaling opportunities** - High-ROI campaigns ready for expansion  
🔴 **Optimization needed** - Underperforming campaigns requiring review  
📊 **Channel analysis** - Best performing marketing channels  
💰 **Portfolio health** - Overall campaign performance metrics  

---

## 🚀 Tech Stack
- **Python 3.x** - Core language
- **SQLite** - Lightweight database
- **CSV/JSON** - Data export formats
- **No external dependencies** - Pure Python standard library

Made with ❤️ by Sibabalwe Mnete
