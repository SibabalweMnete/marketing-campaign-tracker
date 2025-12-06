# 🚀 GitHub Actions CI/CD Setup Guide

## What is CI/CD?

**CI/CD** = **Continuous Integration** / **Continuous Deployment**

- **CI:** Automatically test code on every push
- **CD:** Automatically deploy/build on success

---

## ✅ What This Setup Does

### Automated Testing
```
You push code
    ↓
GitHub automatically runs tests
    ↓
✅ All tests pass → Merge is green
❌ Tests fail → You see the error immediately
```

### Quality Checks
- 🧪 **Unit Tests** - 5 comprehensive tests for core features
- 🔍 **Code Linting** - Checks for style issues
- 🔐 **Security Scan** - Looks for vulnerabilities
- 📝 **Code Formatting** - Ensures consistent style
- 📚 **Documentation** - Verifies required docs exist

### Multi-Version Testing
- Tests on Python 3.8, 3.9, 3.10, 3.11
- Ensures compatibility across versions

---

## 🎯 Quick Start

### Step 1: Push to GitHub

Make sure your project is on GitHub:
```bash
cd /home/wtc/Desktop/side_quests/marketing-campaign-tracker

# If not already a git repo
git init
git add .
git commit -m "Add CI/CD workflow and tests"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/marketing-campaign-tracker.git
git push -u origin main
```

### Step 2: GitHub Creates Workflow Automatically

The `.github/workflows/ci-cd.yml` file I created will:
1. Run automatically on every push
2. Run on every pull request
3. Show status in GitHub interface

### Step 3: View Results

After push:
1. Go to GitHub repo
2. Click **"Actions"** tab
3. See your workflow running!

---

## 📋 Workflow Breakdown

### 1. **Test Job** (5-10 minutes)
Tests code on multiple Python versions
```
✓ Checkout code
✓ Setup Python 3.8, 3.9, 3.10, 3.11
✓ Install dependencies
✓ Run unit tests
✓ Generate coverage report
✓ Upload to Codecov
```

### 2. **Lint Job** (1-2 minutes)
Checks code quality with pylint
```
✓ Static code analysis
✓ Reports any style issues
```

### 3. **Security Job** (1-2 minutes)
Scans for vulnerabilities
```
✓ Bandit security check
✓ Safety vulnerability check
```

### 4. **Build Job** (1-2 minutes)
Creates distributable package
```
✓ Build wheel and tarball
✓ Validate distribution
```

### 5. **Documentation Job** (30 seconds)
Verifies required docs exist
```
✓ Check README.md exists
✓ Check QUICKSTART.md exists
```

### 6. **Notify Job** (30 seconds)
Shows overall status
```
✓ Displays results of all jobs
```

---

## 🧪 Unit Tests Included

Located in `tests/test_tracker.py`:

### Database Tests
```python
✓ test_database_initialization()
✓ test_insert_campaign()
✓ test_insert_metrics()
```

### Analyzer Tests
```python
✓ test_calculate_roi()
✓ test_calculate_ctr()
✓ test_calculate_conversion_rate()
✓ test_get_campaign_summary()
```

### Report Generator Tests
```python
✓ test_csv_export()
✓ test_json_export()
```

### Data Type Tests
```python
✓ test_roi_is_float()
```

---

## 🔧 Required Tools (Auto-Installed)

CI/CD installs these automatically:

```
Testing:
  - pytest           # Test runner
  - pytest-cov       # Coverage reports

Code Quality:
  - flake8           # Style linter
  - black            # Code formatter
  - isort            # Import organizer
  - pylint           # Static analyzer

Security:
  - bandit           # Security issues
  - safety           # Vulnerability check

Build:
  - build            # Package builder
  - twine            # Package validator
```

---

## 📊 View Test Coverage

After CI/CD runs:

1. Go to GitHub Actions
2. Click on the workflow run
3. Click on "test" job
4. Scroll to see coverage report
5. See which lines are tested

Example output:
```
src/analyzer.py ................. 95%
src/database.py ................. 92%
src/report_generator.py ......... 88%
Overall coverage: 92%
```

---

## 🎯 GitHub Status Checks

### Pull Request Status

When you create a PR, GitHub shows:
```
✓ test (3.8)
✓ test (3.9)
✓ test (3.10)
✓ test (3.11)
✓ lint
✓ security
✓ build
✓ documentation
✓ notify

All checks passed! Ready to merge ✅
```

Or if something fails:
```
✗ test (3.10) - Failed
  Error: TestCampaignAnalyzer.test_calculate_roi
  Expected 200.0 but got 100.0

Click to view full error
```

---

## 🚀 Running Tests Locally

Before pushing, test locally:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_tracker.py::TestCampaignDatabase::test_insert_campaign -v

# Run with detailed output
pytest tests/ -vv -s
```

---

## 💡 Workflow Features

### Badge in README
Add this to your README to show build status:

```markdown
[![CI/CD](https://github.com/YOUR_USERNAME/marketing-campaign-tracker/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/YOUR_USERNAME/marketing-campaign-tracker/actions)
```

### Automatic Coverage Reports
Coverage badges show test coverage:

```markdown
[![Coverage](https://codecov.io/github/YOUR_USERNAME/marketing-campaign-tracker/coverage.svg?branch=main)](https://codecov.io/github/YOUR_USERNAME/marketing-campaign-tracker)
```

### Required Status Checks
Make these required before merging:

In GitHub repo:
1. Settings → Branches
2. Add rule for `main`
3. Require status checks to pass:
   - test (Python 3.10)
   - lint
   - security
   - build

---

## ⚙️ Customize Workflow

### To run on different branches:

Edit `.github/workflows/ci-cd.yml`:
```yaml
on:
  push:
    branches: [ main, develop, staging ]  # Add branches
```

### To add more tests:

Add test files to `tests/`:
```bash
touch tests/test_dashboard.py
touch tests/test_comparator.py
```

Workflow automatically picks them up!

### To skip CI/CD on specific commit:

```bash
git commit -m "WIP: fixing bug [skip ci]"
```

---

## 🔐 Security Features

### Secret Management
Store sensitive data as GitHub Secrets:

1. Go to GitHub repo
2. Settings → Secrets and variables → Actions
3. Add secrets:
   ```
   FACEBOOK_TOKEN=eaab...
   GOOGLE_CUSTOMER_ID=123...
   ```

4. Use in workflow:
   ```yaml
   env:
     FACEBOOK_TOKEN: ${{ secrets.FACEBOOK_TOKEN }}
   ```

Never commit credentials! ✅

---

## 📈 Example Workflow Run

### Step 1: Push Code
```bash
git add .
git commit -m "Add new feature"
git push origin main
```

### Step 2: GitHub Workflow Starts
```
⏳ Setting up test environment...
⏳ Installing dependencies...
⏳ Running tests...
⏳ Running linters...
⏳ Running security checks...
⏳ Building package...
⏳ Checking documentation...
```

### Step 3: Get Results
```
✅ All tests passed on Python 3.8
✅ All tests passed on Python 3.9
✅ All tests passed on Python 3.10
✅ All tests passed on Python 3.11
✅ Linting passed
✅ Security passed
✅ Build successful
✅ Documentation verified

🎉 Ready to merge!
```

---

## 🐛 Troubleshooting

### Workflow Not Running
- ✓ Commit `.github/workflows/ci-cd.yml` to repo
- ✓ Push to GitHub
- ✓ Check "Actions" tab

### Tests Failing
- ✓ Run locally: `pytest tests/ -v`
- ✓ Check error message in GitHub
- ✓ Fix code
- ✓ Push again

### Dependencies Not Found
- ✓ Add to `requirements.txt`
- ✓ Workflow reinstalls each time
- ✓ Push again

### Coverage Not Uploading
- ✓ Codecov integration is optional
- ✓ Tests still run without it
- ✓ Check Codecov token if needed

---

## 📚 Learn More

### GitHub Actions Docs
https://docs.github.com/en/actions

### Example Workflows
https://github.com/actions/starter-workflows

### Python Testing
https://docs.pytest.org

---

## ✅ Checklist

- [ ] Push code to GitHub
- [ ] See Actions tab light up
- [ ] Wait for workflow to complete
- [ ] All checks pass ✅
- [ ] Create PR to test branch protection
- [ ] See status checks on PR
- [ ] Merge when ready

---

## 🎉 You're All Set!

Your project now has professional CI/CD! Every push:
- ✅ Runs tests automatically
- ✅ Checks code quality
- ✅ Scans for security issues
- ✅ Validates documentation
- ✅ Reports results instantly

No more manual testing! 🚀

