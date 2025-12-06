# 🎯 5-Step Quick Start

Get your marketing tracker running **right now** in 5 minutes.

---

## Step 1: Install (1 minute)

```bash
# Navigate to project
cd marketing-campaign-tracker

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

✅ **Done!** Dependencies installed.

---

## Step 2: Run Demo (1 minute)

```bash
# Try the tracker with demo data
python3 main.py --auto
```

You'll see:
- ✓ Campaigns collected
- ✓ Reports generated
- ✓ Insights created

✅ **Done!** Demo working.

---

## Step 3: View Results (1 minute)

```bash
# See all your campaigns
python3 main.py --summary

# View dashboard
python3 main.py --dashboard

# Check reports
python3 main.py --compare
python3 main.py --insights
```

✅ **Done!** Data visible.

---

## Step 4: Export Data (1 minute)

```bash
# Generate reports
python3 main.py --report

# Check reports created
ls -la reports/

# View CSV
cat reports/campaigns.csv

# View JSON
cat reports/campaigns.json
```

✅ **Done!** Reports exported.

---

## Step 5: Add Real Data (1 minute setup, then 15-45 min integration)

### Option A: Quick Setup (Easiest)

```bash
# Create .env file for API credentials
cat > .env << EOF
MAILCHIMP_API_KEY=your_key_here
EOF

# Then follow INTEGRATION_CHECKLIST.md to get your API key (15 min)
```

### Option B: Skip for Now

```bash
# Continue using demo data
# Follow up with INTEGRATION_CHECKLIST.md later
```

✅ **Done!** Ready for real data.

---

## All 5 Steps in One Command

```bash
# Setup
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Run demo
python3 main.py --auto

# View results
python3 main.py --summary
```

**Total time: ~5 minutes** ⏱️

---

## What You Have Now

✅ **Working tracker** with demo data
✅ **All reports generated** (CSV, JSON)
✅ **Dashboard** displaying campaigns
✅ **Analytics** with insights
✅ **CLI interface** for everything

---

## Next: Add Real Data

Ready to track real campaigns?

👉 **Follow [INTEGRATION_CHECKLIST.md](INTEGRATION_CHECKLIST.md)**

Pick your platform (15-45 min):
- 📧 **Mailchimp** (email) - 15 min ⭐ Easiest
- 📊 **Google Analytics** - 25 min
- 📱 **Facebook/Instagram** - 30 min
- 🔍 **Google Ads** - 45 min
- 💳 **Stripe** - 20 min

---

## Command Cheat Sheet

```bash
# Core commands
python3 main.py --collect           # Gather data
python3 main.py --summary           # View campaigns
python3 main.py --report            # Generate reports
python3 main.py --dashboard         # Live view
python3 main.py --auto              # Do everything

# Analysis
python3 main.py --insights          # Smart recommendations
python3 main.py --compare           # Compare campaigns
python3 main.py --channels          # By channel breakdown
python3 main.py --efficiency        # Efficiency metrics

# Testing
pytest tests/ -v                    # Run tests
python3 main.py --help              # See all options
```

See [COMMANDS.md](COMMANDS.md) for complete reference.

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Database error"
```bash
rm campaigns.db
python3 main.py --summary  # Creates fresh database
```

### "No data showing"
```bash
# First, collect data
python3 main.py --collect

# Then view
python3 main.py --summary
```

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more help.

---

## Documentation Map

| Need | File |
|------|------|
| **Full guide** | [QUICKSTART.md](QUICKSTART.md) |
| **All features** | [FEATURES.md](FEATURES.md) |
| **Command help** | [COMMANDS.md](COMMANDS.md) |
| **Add real data** | [INTEGRATION_CHECKLIST.md](INTEGRATION_CHECKLIST.md) |
| **API details** | [API_REFERENCE.md](API_REFERENCE.md) |
| **Deploy it** | [DEPLOYMENT.md](DEPLOYMENT.md) |
| **Fix issues** | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| **All docs** | [INDEX.md](INDEX.md) |

---

## File Structure

```
marketing-campaign-tracker/
├── main.py                    # Run this!
├── requirements.txt           # Dependencies
├── .env                       # Your API keys (keep secret)
├── campaigns.db              # Auto-created database
├── src/
│   ├── database.py
│   ├── data_collector.py
│   ├── analyzer.py
│   ├── report_generator.py
│   ├── dashboard.py
│   └── comparator.py
├── tests/
│   └── test_tracker.py
├── reports/                   # Generated CSV/JSON
└── data/                      # Data storage
```

---

## Stats

- **Lines of code:** ~1,500 (lean & efficient)
- **Lines of docs:** ~7,000 (comprehensive)
- **Test coverage:** 11 unit tests
- **Platforms supported:** 7 major marketing platforms
- **Deployment options:** 6 different methods
- **Python versions:** 3.8, 3.9, 3.10, 3.11 (all tested)

---

## You're All Set! 🎉

**Next:**
1. Run `python3 main.py --auto` to see it work
2. Check [INTEGRATION_CHECKLIST.md](INTEGRATION_CHECKLIST.md) to add real data
3. Deploy with [DEPLOYMENT.md](DEPLOYMENT.md)
4. Monitor with [MONITORING.md](MONITORING.md)

**Questions?** Check [INDEX.md](INDEX.md) for full documentation.

---

*Happy tracking!* 📈
