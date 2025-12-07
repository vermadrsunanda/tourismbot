# Tourism Bot - Command Reference

## Getting Started

### Initial Setup
```bash
# Navigate to project
cd "path/to/VSCode tourism Bot"

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "MISTRAL_API_KEY=your_key_here" > .env
```

## Running the Application

### Option 1: Flask Web Server
```bash
python -m src.app
# Access: http://127.0.0.1:5000
```

### Option 2: Streamlit Cloud Version
```bash
streamlit run streamlit_app.py
# Opens automatically at http://localhost:8501
```

### Option 3: Production with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 src.app:app
# Production deployment
```

## Testing APIs

### Test Chat Endpoint
```bash
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Tell me about Paris"}'
```

### Test Weather Endpoint
```bash
curl "http://127.0.0.1:5000/api/weather?destination=Paris"
```

### Test Flight Endpoint
```bash
curl "http://127.0.0.1:5000/api/flights?origin=NYC&destination=Tokyo"
```

### Test Attractions Endpoint
```bash
curl "http://127.0.0.1:5000/api/attractions?city=Paris"
```

### Test Recommendations Endpoint
```bash
curl -X POST http://127.0.0.1:5000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"preferences":"beaches and warm weather"}'
```

### Health Check
```bash
curl http://127.0.0.1:5000/api/health
```

## Running Tests

### Run All Tests
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Run Specific Test File
```bash
python -m unittest tests.test_validators -v
```

### Run with Coverage
```bash
coverage run -m unittest discover -s tests
coverage report
coverage html
```

## Package Management

### Update All Packages
```bash
pip install --upgrade -r requirements.txt
```

### Install Single Package
```bash
pip install package_name
```

### Generate Updated Requirements
```bash
pip freeze > requirements.txt
```

### Check for Outdated Packages
```bash
pip list --outdated
```

## Development Commands

### Check Python Version
```bash
python --version
```

### Check Virtual Environment
```bash
pip list
```

### Run Python Interactive Shell
```bash
python
```

### Format Code (optional)
```bash
pip install black
black src/
```

### Lint Code (optional)
```bash
pip install pylint
pylint src/
```

## Deployment Commands

### Deploy to Streamlit Cloud
```bash
# 1. Push to GitHub
git add .
git commit -m "Update"
git push

# 2. Go to https://share.streamlit.io
# 3. Follow web UI
```

### Deploy to Vercel
```bash
npm install -g vercel
vercel --prod
```

### Deploy to Railway
```bash
# Connect GitHub repo at railway.app
# Auto-deploys on push
```

### Create Docker Image
```bash
docker build -t tourism-bot:latest .
docker run -p 5000:5000 -e MISTRAL_API_KEY=your_key tourism-bot:latest
```

## Environment & Configuration

### View Environment Variables
```bash
cat .env
```

### Set Environment Variable (temporary)
```bash
$env:MISTRAL_API_KEY='your_key_here'
```

### Test Environment Variable
```bash
python -c "import os; print(os.getenv('MISTRAL_API_KEY'))"
```

## Git Commands

### Initialize Repository
```bash
git init
git remote add origin https://github.com/username/tourism-bot.git
```

### Commit Changes
```bash
git add .
git commit -m "Your message"
git push origin main
```

### Check Git Status
```bash
git status
git log
```

## Troubleshooting Commands

### Clear Python Cache
```bash
python -c "import shutil; shutil.rmtree('src/__pycache__')"
python -c "import shutil; shutil.rmtree('.pytest_cache')"
```

### Reinstall Virtual Environment
```bash
# Deactivate first
deactivate
# Remove old venv
rm -r venv
# Create new
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Check Port Usage (Windows)
```bash
netstat -ano | findstr :5000
# Kill process using port 5000
taskkill /PID <PID> /F
```

### Check Port Usage (Mac/Linux)
```bash
lsof -i :5000
# Kill process
kill -9 <PID>
```

## Logging & Monitoring

### View Application Logs
```bash
tail -f logs/tourism_bot.log
```

### Clear Logs
```bash
rm logs/tourism_bot.log
```

### Check Disk Space
```bash
df -h
```

## Database Commands (if using)

### Initialize Database
```bash
python -m flask db init
python -m flask db migrate -m "Initial migration"
python -m flask db upgrade
```

## Useful Resources

### Python Debugging
```python
# In your code
import pdb; pdb.set_trace()  # Breakpoint

# Or use
import ipdb; ipdb.set_trace()
```

### Generate API Documentation
```bash
pip install pydoc-markdown
pydoc-markdown src/app.py > API.md
```

### Performance Profiling
```python
import cProfile
cProfile.run('main()')
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python -m src.app` | Run Flask app |
| `streamlit run streamlit_app.py` | Run Streamlit |
| `pip install -r requirements.txt` | Install deps |
| `python -m unittest discover` | Run tests |
| `git push origin main` | Push to GitHub |
| `vercel --prod` | Deploy to Vercel |
| `curl http://127.0.0.1:5000/api/health` | Test API |

## Advanced Commands

### Monitor Memory Usage
```bash
pip install memory-profiler
python -m memory_profiler src/app.py
```

### Async Testing
```bash
pip install pytest-asyncio
pytest --asyncio-mode=auto
```

### Load Testing
```bash
pip install locust
locust -f locustfile.py
```

## CI/CD Commands (GitHub Actions)

### Test Workflow
```yaml
name: Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m unittest discover
```

---

**Need Help?**
- Check [README.md](README.md) for detailed info
- See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help
- Review [FEATURES.md](FEATURES.md) for feature details
- Check [QUICKSTART.md](QUICKSTART.md) for quick setup

**Last Updated**: December 2025
