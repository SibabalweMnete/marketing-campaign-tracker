# 📊 Monitoring & Maintenance Guide

Keep your marketing tracker running smoothly in production.

---

## Daily Monitoring

### Check Collection Status

```bash
# View latest run
tail -f logs/tracker.log

# Check database size
du -h campaigns.db

# Verify data freshness
python3 main.py --summary | tail -10
```

### Monitor for Errors

```bash
# Check for failed collections
grep -i "error\|failed\|exception" logs/tracker.log | tail -20

# Count errors by type
grep -i "error" logs/tracker.log | wc -l

# See last run time
ls -l campaigns.db
```

---

## Weekly Tasks

### Backup Database

```bash
# Create backup
cp campaigns.db campaigns.db.backup.$(date +%Y%m%d)

# Or automated backup
mkdir -p backups
cp campaigns.db backups/campaigns.db.$(date +%Y-%m-%d)

# List backups
ls -lh backups/
```

### Review Reports

```bash
# Generate weekly report
python3 main.py --report

# Compare with previous week
python3 main.py --compare

# Check insights
python3 main.py --insights
```

### Validate Integrations

Test each API connection:

```bash
# Test Facebook
python3 -c "from src.data_collector import DataCollector; \
    dc = DataCollector(); \
    result = dc.fetch_facebook_campaigns(); \
    print(f'Facebook: {len(result)} campaigns')"

# Test Google Analytics
python3 -c "from src.data_collector import DataCollector; \
    dc = DataCollector(); \
    result = dc.fetch_google_analytics(); \
    print(f'GA4: {len(result)} records')"

# Test all
python3 main.py --collect
```

---

## Monthly Tasks

### Archive Old Data

```bash
# Export to archive
python3 main.py --report /archive/

# Delete old records (optional)
# Edit delete_campaigns() method to remove data older than 90 days
```

### Review Metrics

```bash
# Analyze performance trends
python3 main.py --dashboard

# Check ROI by channel
python3 main.py --channels

# Efficiency analysis
python3 main.py --efficiency
```

### Update API Tokens

```bash
# Check token expiration dates
# Most API tokens expire 30-90 days

# Renew tokens
# 1. Get new token from platform
# 2. Update .env file
# 3. Test connection

cat .env
# Update: FACEBOOK_ACCESS_TOKEN=new_token_here
source .env  # Reload
python3 main.py --collect
```

---

## Quarterly Tasks

### Security Audit

```bash
# Check if .env is in .gitignore
grep -i "\.env" .gitignore

# Verify no credentials in code
grep -r "ACCESS_TOKEN" src/
grep -r "SECRET_KEY" src/
# Should return nothing

# Review GitHub secrets
# GitHub → Settings → Secrets → Check all active
```

### Code Quality Review

```bash
# Run linters
flake8 src/ tests/

# Check for issues
pylint src/*.py

# Fix formatting
black src/

# Sort imports
isort src/
```

### Test Suite

```bash
# Run full test suite
pytest tests/ -v --cov=src

# Check coverage
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html

# Run with different Python versions
python3.9 -m pytest tests/
python3.10 -m pytest tests/
python3.11 -m pytest tests/
```

### Dependency Update

```bash
# Check for outdated packages
pip list --outdated

# Update all packages
pip install -U -r requirements.txt

# Or selective updates
pip install --upgrade click
pip install --upgrade pandas

# Update requirements.txt
pip freeze > requirements.txt
```

---

## Troubleshooting Production Issues

### High Memory Usage

```bash
# Check memory
python3 -c "import psutil; print(psutil.virtual_memory())"

# Reduce data in memory
# Edit main.py to use pagination/streaming
# Instead of loading all at once:

# Current (loads all):
campaigns = db.get_all_campaigns()  # 10,000+ records

# Better (streaming):
for campaign in db.get_campaigns_paginated(batch_size=100):
    process(campaign)
```

### Slow API Calls

```bash
# Add timeout
response = requests.get(url, timeout=5)  # 5 second timeout

# Add retry logic
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
```

### Database Corruption

```bash
# Check database integrity
python3 -c "import sqlite3; conn = sqlite3.connect('campaigns.db'); \
    conn.execute('PRAGMA integrity_check'); \
    print('Database OK')"

# Repair if needed
sqlite3 campaigns.db < /dev/null

# If severely corrupted, restore backup
cp campaigns.db.backup campaigns.db
```

### Missing Data After Collection

```bash
# Check database wasn't reset
ls -l campaigns.db
# Look for recent modification time

# Verify collection completed
grep "Fetched" logs/tracker.log | tail -5

# Check for errors
grep "error" logs/tracker.log | tail -5

# Force recollection
rm campaigns.db  # Start fresh
python3 main.py --collect
```

---

## Performance Optimization

### Speed Up Collections

```python
# Parallel API calls instead of sequential

import concurrent.futures
from src.data_collector import DataCollector

def fetch_all_platforms():
    """Fetch from multiple platforms in parallel"""
    dc = DataCollector()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        facebook = executor.submit(dc.fetch_facebook_campaigns)
        google = executor.submit(dc.fetch_google_analytics)
        mailchimp = executor.submit(dc.fetch_mailchimp_campaigns)
        
        results = []
        results.extend(facebook.result() or [])
        results.extend(google.result() or [])
        results.extend(mailchimp.result() or [])
    
    return results
```

### Cache API Results

```python
# Cache results to avoid repeated calls

import time
from functools import lru_cache

class DataCollectorWithCache:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour
    
    def fetch_facebook_campaigns(self):
        """Cached Facebook fetch"""
        key = 'facebook_campaigns'
        now = time.time()
        
        # Return cached if fresh
        if key in self.cache and (now - self.cache[key]['time']) < self.cache_ttl:
            return self.cache[key]['data']
        
        # Fetch fresh
        data = self._fetch_facebook_real()
        self.cache[key] = {'data': data, 'time': now}
        return data
```

### Database Indexing

```python
# Add indexes for faster queries

def create_indexes(self):
    """Create database indexes"""
    queries = [
        "CREATE INDEX IF NOT EXISTS idx_campaign_name ON campaigns(name)",
        "CREATE INDEX IF NOT EXISTS idx_metric_date ON metrics(date)",
        "CREATE INDEX IF NOT EXISTS idx_campaign_id ON metrics(campaign_id)",
    ]
    
    for query in queries:
        self.conn.execute(query)
    self.conn.commit()
```

---

## Logging Setup

### Configure Logging

```python
# In main.py

import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    """Configure logging with rotation"""
    
    # Create logger
    logger = logging.getLogger('tracker')
    logger.setLevel(logging.DEBUG)
    
    # File handler (rotating)
    handler = RotatingFileHandler(
        'logs/tracker.log',
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5  # Keep 5 files
    )
    
    # Console handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    console.setFormatter(formatter)
    
    logger.addHandler(handler)
    logger.addHandler(console)
    
    return logger

# Usage
logger = setup_logging()
logger.info("Starting collection")
logger.error("API error occurred")
logger.debug("Debug information")
```

---

## Alert System

### Set Up Email Alerts

```python
# Send email on errors

import smtplib
from email.mime.text import MIMEText

def send_alert(subject, message):
    """Send email alert"""
    
    sender = os.getenv('ALERT_EMAIL')
    password = os.getenv('ALERT_PASSWORD')
    recipient = os.getenv('ALERT_RECIPIENT')
    
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send alert: {e}")

# Usage
try:
    collect_campaigns()
except Exception as e:
    send_alert(
        subject="Tracker Error - Action Required",
        message=f"Collection failed: {str(e)}"
    )
```

### Webhook Alerts

```python
# Send alerts to Slack/Discord/Teams

import requests

def send_webhook_alert(message, webhook_url):
    """Send alert to webhook"""
    
    payload = {
        'text': f":warning: Marketing Tracker Alert:\n{message}"
    }
    
    try:
        requests.post(webhook_url, json=payload, timeout=5)
    except Exception as e:
        print(f"Webhook failed: {e}")

# Usage
webhook = os.getenv('SLACK_WEBHOOK')
send_webhook_alert("Collection failed - check logs", webhook)
```

---

## Monitoring Dashboard

### Simple Health Check

```python
# Create health check endpoint for monitoring

def get_system_health():
    """Check system health"""
    
    health = {
        'status': 'healthy',
        'checks': {},
        'timestamp': datetime.now().isoformat()
    }
    
    # Check database
    try:
        db = CampaignDatabase()
        count = len(db.get_all_campaigns())
        health['checks']['database'] = {
            'status': 'ok',
            'campaigns': count
        }
    except Exception as e:
        health['status'] = 'unhealthy'
        health['checks']['database'] = {'status': 'error', 'error': str(e)}
    
    # Check recent data
    try:
        recent = db.get_campaigns_since(datetime.now() - timedelta(hours=1))
        health['checks']['recent_data'] = {
            'status': 'ok' if recent else 'stale',
            'records': len(recent)
        }
    except Exception as e:
        health['checks']['recent_data'] = {'status': 'error'}
    
    # Check API connectivity
    try:
        response = requests.get('https://graph.instagram.com', timeout=5)
        health['checks']['api_connectivity'] = {'status': 'ok'}
    except Exception:
        health['checks']['api_connectivity'] = {'status': 'failed'}
    
    return health

# Export health status
if __name__ == '__main__':
    import json
    health = get_system_health()
    print(json.dumps(health, indent=2))
```

---

## Scheduled Maintenance Script

```bash
#!/bin/bash
# maintenance.sh - Run weekly maintenance

set -e  # Exit on error

echo "=== Marketing Tracker Maintenance ==="
echo "Date: $(date)"

# 1. Backup database
echo "Backing up database..."
cp campaigns.db backups/campaigns.db.$(date +%Y-%m-%d)

# 2. Run tests
echo "Running tests..."
pytest tests/ -q

# 3. Check code quality
echo "Checking code quality..."
flake8 src/ --count

# 4. Update dependencies
echo "Checking for updates..."
pip list --outdated

# 5. Generate fresh reports
echo "Generating reports..."
python3 main.py --report

# 6. Cleanup old logs
echo "Cleaning up old logs..."
find logs/ -type f -mtime +30 -delete

echo "=== Maintenance Complete ==="
```

Run weekly:
```bash
chmod +x maintenance.sh
0 2 * * 1 /path/to/maintenance.sh >> /var/log/tracker-maintenance.log 2>&1
```

---

## Upgrade Procedure

### Safe Upgrade Process

```bash
# 1. Backup everything
cp -r . backup.$(date +%Y%m%d)/
cp campaigns.db campaigns.db.backup

# 2. Update code
git pull origin main

# 3. Update dependencies
pip install -U -r requirements.txt

# 4. Run tests
pytest tests/ -v

# 5. Test with demo data
python3 main.py --summary

# 6. Verify all commands work
python3 main.py --report
python3 main.py --insights
python3 main.py --dashboard

# 7. Deploy!
echo "Upgrade successful"
```

---

## Disaster Recovery

### Restore from Backup

```bash
# 1. Stop current process
pkill -f "python3 main.py"

# 2. Restore database
cp campaigns.db.backup campaigns.db

# 3. Verify restore
python3 main.py --summary

# 4. Check for any issues
pytest tests/ -v

# 5. Resume operation
python3 main.py --auto &
```

---

## Documentation

### Keep Docs Updated

- [ ] Update README.md with new features
- [ ] Add runbooks for common issues
- [ ] Document any custom integrations
- [ ] Maintain API integration list
- [ ] Update architecture diagrams

---

**Regularly maintain and monitor your tracker for best results!** 📈
