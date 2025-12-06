# 🚀 Deployment Guide for Marketing Campaign Tracker

## Deployment Options

Choose based on your needs:

---

## Option 1: GitHub Pages (Free Dashboards)

Host static reports on GitHub Pages.

### Setup:
```bash
# Create gh-pages branch
git checkout --orphan gh-pages
git reset --hard
git commit --allow-empty -m "Initial commit"
git push origin gh-pages

# Go back to main
git checkout main
```

### Add workflow file

Create `.github/workflows/deploy-pages.yml`:

```yaml
name: Deploy Reports

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 8 * * *'  # Daily at 8 AM

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Generate reports
      run: |
        python3 main.py --auto
    
    - name: Deploy to Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./reports
```

---

## Option 2: Docker Container

Deploy as a containerized service.

### Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy project
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory
RUN mkdir -p data reports

# Set environment
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["python3", "main.py", "--auto"]
```

### Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  tracker:
    build: .
    container_name: marketing-tracker
    volumes:
      - ./data:/app/data
      - ./reports:/app/reports
      - ./.env:/app/.env
    environment:
      - FACEBOOK_ACCESS_TOKEN=${FACEBOOK_ACCESS_TOKEN}
      - GOOGLE_CUSTOMER_ID=${GOOGLE_CUSTOMER_ID}
    schedule: "0 8 * * *"
```

### Deploy to Docker Hub:

```bash
# Build image
docker build -t your-username/marketing-tracker .

# Login to Docker Hub
docker login

# Push image
docker push your-username/marketing-tracker
```

---

## Option 3: Heroku (Easy Cloud Deployment)

Deploy to Heroku for automatic daily runs.

### 1. Create `Procfile`:

```
worker: python3 main.py --auto
```

### 2. Create `runtime.txt`:

```
python-3.11.0
```

### 3. Deploy:

```bash
# Install Heroku CLI
# Then:

heroku login
heroku create marketing-tracker
git push heroku main

# Set environment variables
heroku config:set FACEBOOK_ACCESS_TOKEN=eaab...
heroku config:set GOOGLE_CUSTOMER_ID=123...

# Schedule daily runs
heroku addons:create scheduler:standard

# Add task
heroku run "python3 main.py --auto" --exit-code
```

---

## Option 4: AWS Lambda (Serverless)

Run automated reports on a schedule.

### Create `handler.py`:

```python
import subprocess
import os

def run_tracker(event, context):
    """Handler for AWS Lambda"""
    
    os.environ['FACEBOOK_TOKEN'] = os.getenv('FACEBOOK_TOKEN')
    os.environ['GOOGLE_ID'] = os.getenv('GOOGLE_ID')
    
    # Run collection and report
    result = subprocess.run(['python3', 'main.py', '--auto'], capture_output=True)
    
    return {
        'statusCode': 200,
        'body': result.stdout.decode()
    }
```

### Deploy:

```bash
# Create deployment package
zip -r function.zip . -x ".*" "*.git*"

# Upload via AWS Console or CLI
aws lambda create-function \
  --function-name marketing-tracker \
  --runtime python3.11 \
  --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-role \
  --handler handler.run_tracker \
  --zip-file fileb://function.zip

# Add CloudWatch trigger for daily execution
```

---

## Option 5: Linux Cron Job (Simple & Effective)

Run on your own server or VPS.

### 1. Copy project:

```bash
git clone https://github.com/YOUR_USERNAME/marketing-tracker
cd marketing-tracker
```

### 2. Install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Create `.env`:

```bash
cat > .env << EOF
FACEBOOK_ACCESS_TOKEN=eaab...
GOOGLE_CUSTOMER_ID=123...
EOF
```

### 4. Add cron job:

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 8 AM):
0 8 * * * cd /path/to/marketing-tracker && source venv/bin/activate && python3 main.py --auto >> /var/log/tracker.log 2>&1

# Or run every 6 hours:
0 */6 * * * cd /path/to/marketing-tracker && source venv/bin/activate && python3 main.py --auto >> /var/log/tracker.log 2>&1
```

### 5. Check logs:

```bash
tail -f /var/log/tracker.log
```

---

## Option 6: GitHub Actions (Simplest for GitHub!)

Already set up! This is the easiest option.

### How it works:

1. ✅ Already configured in `.github/workflows/ci-cd.yml`
2. ✅ Runs on every push for testing
3. ✅ Can be scheduled for daily collection

### Add scheduling:

Edit `.github/workflows/ci-cd.yml`, add `schedule`:

```yaml
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 8 * * *'  # Daily at 8 AM UTC
```

### Set secrets:

1. Go to GitHub repo
2. Settings → Secrets and variables → Actions
3. Add:
   ```
   FACEBOOK_ACCESS_TOKEN=eaab...
   GOOGLE_CUSTOMER_ID=123...
   ```

### Use in workflow:

```yaml
env:
  FACEBOOK_ACCESS_TOKEN: ${{ secrets.FACEBOOK_ACCESS_TOKEN }}
  GOOGLE_CUSTOMER_ID: ${{ secrets.GOOGLE_CUSTOMER_ID }}
```

---

## Comparison Table

| Option | Setup Time | Cost | Best For | Automation |
|--------|-----------|------|----------|-----------|
| **GitHub Pages** | 10 min | Free | Static reports | ✅ Built-in |
| **Docker** | 30 min | $5-50/mo | Anywhere | ✅ Easy |
| **Heroku** | 15 min | Free-$7/mo | Quick deploy | ✅ Dyno scheduler |
| **AWS Lambda** | 45 min | Pay-per-use | Serverless | ✅ CloudWatch |
| **Cron Job** | 20 min | Free | VPS/Server | ✅ Crontab |
| **GitHub Actions** | 5 min | Free | GitHub users | ✅ Built-in |

---

## Recommended Setup

### For Quick Start:
**GitHub Actions** (already configured!)
- Free
- No server needed
- Automatic scheduling
- Results in GitHub

### For Production:
**Docker + Your Server** or **Heroku**
- Reliable
- Easy to scale
- Professional setup
- Full control

### For Minimal Cost:
**Cron Job on Linux VPS**
- $5/month VPS
- Simple setup
- Full control
- No dependencies

---

## Next Steps

1. Choose your deployment option
2. Follow setup instructions
3. Set environment variables (API credentials)
4. Configure scheduling
5. Test with a manual run
6. Monitor logs

---

## Troubleshooting Deployment

### "Cannot find .env file"
- Set environment variables in deployment platform
- Don't rely on .env in production

### "API token not working"
- Verify token in secrets/environment
- Check token permissions
- Ensure token hasn't expired

### "Reports not generating"
- Check logs for errors
- Verify database created
- Ensure write permissions

### "Running too frequently"
- Adjust schedule in cron/workflow
- Use `schedule` in GitHub Actions
- Add rate limiting

---

## Security Best Practices

✅ **DO:**
- Store credentials in secrets/env
- Use CI/CD for automated deployment
- Monitor logs for errors
- Rotate tokens periodically
- Use HTTPS for exports

❌ **DON'T:**
- Commit .env file
- Hardcode credentials
- Share API tokens
- Log sensitive data
- Expose reports publicly

---

## Monitoring & Alerts

### GitHub Actions:
- ✓ See all runs in Actions tab
- ✓ Email notifications on failure
- ✓ Check workflow status badge

### Cron Jobs:
- ✓ Monitor logs: `tail -f /var/log/tracker.log`
- ✓ Check exit codes
- ✓ Set up email alerts

### Docker:
- ✓ Use `docker logs` to view
- ✓ Set up container monitoring
- ✓ Use health checks

---

**Ready to deploy? Start with GitHub Actions—it's already configured!** 🚀
