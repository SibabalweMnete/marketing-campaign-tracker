# 🔧 Troubleshooting Guide

## Common Issues & Solutions

---

## 1. Database Issues

### "database.db is locked"
```bash
# Solution 1: Wait a moment and try again
# SQLite locks are temporary

# Solution 2: Delete old database
rm campaigns.db
python3 main.py --summary  # Creates fresh database
```

### "table campaigns already exists"
```bash
# The database is fine - just a warning
# This happens when running init multiple times

# No action needed!
```

### "No data in reports"
```bash
# Check 1: Did you collect data?
python3 main.py --collect

# Check 2: Does database have campaigns?
python3 main.py --summary

# Check 3: Check database file exists
ls -la campaigns.db
```

---

## 2. API Connection Issues

### "FACEBOOK_ACCESS_TOKEN not found"
```bash
# Create .env file
cat > .env << EOF
FACEBOOK_ACCESS_TOKEN=your_token_here
GOOGLE_CUSTOMER_ID=your_id_here
EOF

# Or set environment variable
export FACEBOOK_ACCESS_TOKEN=your_token_here
python3 main.py --collect
```

### "Connection timeout when collecting data"
```bash
# Check 1: Internet connection
ping google.com

# Check 2: API is responding
curl -I https://graph.instagram.com

# Check 3: Token is valid
# Log in to Meta Business Suite and check token

# Workaround: Use demo data
python3 main.py --summary  # Uses demo data by default
```

### "401 Unauthorized - Invalid token"
```bash
# Solutions:
# 1. Generate new token in Meta Business Suite
# 2. Check token scope has required permissions
# 3. Ensure token hasn't expired (usually 60 days)

# Update .env with new token
```

---

## 3. Installation Issues

### "ModuleNotFoundError: No module named 'src'"
```bash
# You're not in the right directory
# Make sure you're in project root:

cd /path/to/marketing-campaign-tracker
python3 main.py --help

# Check directory structure:
ls -la src/
# Should see: analyzer.py, data_collector.py, database.py, report_generator.py
```

### "ModuleNotFoundError: No module named 'click'"
```bash
# Install dependencies:
pip install -r requirements.txt

# Or install manually:
pip install click pandas
```

### "pip: command not found"
```bash
# You might be using Python 2
# Use pip3 instead:

pip3 install -r requirements.txt
python3 main.py --help
```

### "venv: command not found"
```bash
# Install Python venv:

# Ubuntu/Debian:
sudo apt-get install python3-venv

# macOS:
brew install python3

# Then create venv:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 4. CSV/JSON Export Issues

### "No reports found"
```bash
# Check 1: Did you generate reports?
python3 main.py --report --insights

# Check 2: Check reports directory
ls -la reports/

# Check 3: Create reports first
python3 main.py --collect
python3 main.py --report
```

### "Permission denied when saving reports"
```bash
# Check permissions
ls -la reports/

# If reports directory doesn't exist:
mkdir -p reports

# If permission issue:
chmod 755 reports/

# Or use absolute path:
python3 main.py --report /tmp/
```

### "CSV file is empty or corrupted"
```bash
# Solution: Regenerate it
python3 main.py --report
python3 main.py --insights

# Check file size
ls -lh reports/*.csv

# View content
head -20 reports/campaigns.csv
```

---

## 5. Dashboard Issues

### "dashboard: command not found"
```bash
# Don't use 'dashboard' directly
# Use the main.py interface:

python3 main.py --dashboard

# Or use auto mode for everything:
python3 main.py --auto
```

### "Dashboard looks corrupted/misaligned"
```bash
# Terminal window too small
# Resize your terminal to be wider

# Or clear screen issues:
clear
python3 main.py --dashboard

# If still broken, might be terminal encoding:
export LANG=en_US.UTF-8
python3 main.py --dashboard
```

### "Dashboard not refreshing"
```bash
# It refreshes every 5 seconds automatically
# If stuck, press Ctrl+C and restart

# Or check if data exists:
python3 main.py --summary
```

---

## 6. Comparison & Insights Issues

### "Cannot compare campaigns - not enough data"
```bash
# Need at least 2 campaigns:
python3 main.py --collect

# Then compare:
python3 main.py --compare
python3 main.py --insights
```

### "Insights are empty"
```bash
# Need complete metrics for insights to work
# Make sure you have:
# - Multiple campaigns
# - Each with budget and spend
# - Each with impressions and clicks

# Check what you have:
python3 main.py --summary

# Regenerate insights:
python3 main.py --insights
```

---

## 7. Testing Issues

### "pytest: command not found"
```bash
# Install pytest
pip install pytest pytest-cov

# Then run tests
pytest tests/ -v
```

### "Tests fail with 'database locked'"
```bash
# Tests create temporary databases
# Wait a moment and retry:

pytest tests/ -v

# If persistent, remove test databases:
rm test_*.db 2>/dev/null
pytest tests/ -v
```

### "Tests pass but coverage is low"
```bash
# Run with coverage report:
pytest tests/ -v --cov=src --cov-report=html

# View report:
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

---

## 8. Git & GitHub Issues

### "fatal: not a git repository"
```bash
# You're not in a git project
# Navigate to project root:

cd /path/to/marketing-campaign-tracker
git status

# Or initialize git:
git init
git add .
git commit -m "Initial commit"
```

### "fatal: 'origin' does not appear to be a 'git' repository"
```bash
# Need to add remote
git remote add origin https://github.com/YOUR_USERNAME/marketing-tracker.git
git branch -M main
git push -u origin main
```

### "CI/CD workflow not running"
```bash
# Check 1: Workflow file exists
ls -la .github/workflows/

# Check 2: Push was successful
git log --oneline

# Check 3: Check GitHub Actions tab
# Go to your repo → Actions → see runs

# Check 4: Verify main branch
git branch
# Should show: * main
```

---

## 9. Environment Variable Issues

### "Environment variables not working"
```bash
# Wrong way:
FACEBOOK_TOKEN=xyz python3 main.py  # Might not work

# Right way:
export FACEBOOK_TOKEN=xyz
python3 main.py

# Or use .env file:
echo "FACEBOOK_TOKEN=xyz" > .env
python3 main.py
```

### "GitHub Actions can't find secrets"
```bash
# Check 1: Secrets are set
# Settings → Secrets and variables → Actions

# Check 2: Workflow is using them
# Should have: ${{ secrets.FACEBOOK_TOKEN }}

# Check 3: Secret names match
# If using FACEBOOK_TOKEN in code, must be FACEBOOK_TOKEN in secrets
```

---

## 10. Performance Issues

### "Script takes too long"
```bash
# Collecting data is slow:
python3 main.py --collect --summary

# To speed up:
# 1. Use fewer API calls (limit to 1-2 platforms)
# 2. Use cached demo data
# 3. Schedule collection less frequently

# Skip collection, use existing data:
python3 main.py --report --insights
```

### "Memory usage is high"
```bash
# Check memory:
python3 -c "import psutil; print(psutil.virtual_memory())"

# If using lots of data, use filtering:
python3 main.py --summary | head -20

# Or export in chunks:
python3 main.py --report --channels facebook
```

---

## 11. Report Generation Issues

### "Report doesn't match data"
```bash
# Regenerate from scratch:
rm campaigns.db
python3 main.py --collect
python3 main.py --report

# Or verify data:
python3 main.py --summary
```

### "CSV has encoding issues"
```bash
# Export with UTF-8 encoding:
# Already handled in code, but if issues:

# Check encoding:
file reports/campaigns.csv

# Reimport in Excel with UTF-8:
# File → Open → Select UTF-8 encoding
```

---

## 12. Dashboard Performance

### "Dashboard refreshes too fast/slow"
```bash
# Edit main.py line with:
# Change refresh interval (currently 5 seconds)

# Or use no-refresh mode:
python3 main.py --dashboard --no-refresh
```

### "Dashboard uses too much CPU"
```bash
# Reduce refresh frequency in dashboard.py
# Change: time.sleep(5) to time.sleep(30)

# Or use summary instead:
python3 main.py --summary  # One-time display
```

---

## Getting Help

### Check Version
```bash
python3 --version
pip --version
python3 -m sqlite3 --version
```

### View Full Logs
```bash
# Run with verbose output:
python3 main.py --report -v  # If -v supported

# Or redirect to file:
python3 main.py --auto 2>&1 | tee output.log
cat output.log
```

### Search for Errors
```bash
# Search logs for errors
grep -i error output.log

# Search for specific issue
grep -i "token\|permission\|not found" output.log
```

### Test Individual Components
```bash
# Test database
python3 -c "from src.database import CampaignDatabase; db = CampaignDatabase(); print('✓ Database OK')"

# Test analyzer
python3 -c "from src.analyzer import CampaignAnalyzer; print('✓ Analyzer OK')"

# Test collector
python3 -c "from src.data_collector import DataCollector; print('✓ Collector OK')"
```

---

## Still Having Issues?

### Debug Checklist

- [ ] Python version is 3.8+ (`python3 --version`)
- [ ] All dependencies installed (`pip list | grep -i click`)
- [ ] In correct directory (`pwd` shows project root)
- [ ] Database file exists (`ls campaigns.db`)
- [ ] Reports directory exists (`mkdir -p reports`)
- [ ] API tokens are valid (test with curl)
- [ ] No permission issues (`ls -la | grep campaigns.db`)
- [ ] Enough disk space (`df -h`)
- [ ] Internet connection working (`ping google.com`)

### Get More Details

```bash
# Full traceback
python3 -u main.py --collect 2>&1

# Check imports
python3 -c "import src.database; import src.analyzer; print('All imports OK')"

# List all files
find . -type f -name "*.py" | head -20
```

---

**Still stuck? Check the logs and error messages carefully—they usually tell you exactly what's wrong!** 📋
