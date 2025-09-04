# TrialMatch AI - Deployment Guide

## 🚀 Quick Deployment to Streamlit Cloud

### Prerequisites
- GitHub account with your project repository
- Streamlit Cloud account (free at share.streamlit.io)

### Step 1: Prepare Repository
Ensure your repo has these files in the root:
- `streamlit_app.py` ✅
- `requirements.txt` ✅
- All data files in `data/` directory ✅

### Step 2: Deploy to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**

2. **Click "New app"**

3. **Connect your GitHub repository:**
   - Repository: `your-username/trialmatch-ai-pro`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

4. **Click "Deploy!"**

Your app will be live at: `https://your-username-trialmatch-ai-pro-streamlit-app-xxxxx.streamlit.app/`

### Step 3: Configure Secrets (If Using PDF Features)

1. **In Streamlit Cloud, go to your app settings**
2. **Add to Secrets:**
```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "your-openai-api-key-here"
```

## 🛠 Local Development Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/your-username/trialmatch-ai-pro.git
cd trialmatch-ai-pro
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv trialmatch-env

# Activate it
# On Windows:
trialmatch-env\Scripts\activate
# On Mac/Linux:
source trialmatch-env/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Locally
```bash
streamlit run streamlit_app.py
```

App will open at `http://localhost:8501`

## 🔧 Environment Variables

### Required for PDF Features
```bash
# Create .env file in project root
OPENAI_API_KEY=your-openai-api-key
```

### Optional Configuration
```bash
# Data directory (default: "data")
DATA_DIR=data

# Log level (default: INFO)
LOG_LEVEL=INFO
```

## 📁 Project Structure Requirements

Ensure your deployment has this structure:
```
trialmatch-ai-pro/
├── streamlit_app.py          # Main app (REQUIRED)
├── requirements.txt          # Dependencies (REQUIRED)
├── README.md                # Documentation
├── .gitignore               # Git ignore file
├── src/                     # Source code
│   ├── __init__.py
│   ├── matching/
│   │   ├── __init__.py
│   │   └── engine.py        # Core matching logic
│   ├── data/
│   │   ├── __init__.py
│   │   └── loader.py        # Data loading
│   └── utils/
│       ├── __init__.py
│       └── pdf_parser.py    # PDF processing
├── data/                    # Data files (REQUIRED)
│   ├── sample_patients.csv
│   └── trials/
│       ├── egfr.json
│       ├── pd-l1.json
│       ├── kras_g12c.json
│       ├── combo.json
│       └── early_stage.json
├── tests/                   # Unit tests
├── docs/                    # Documentation
└── assets/                  # Screenshots, etc.
```

## 🚨 Common Deployment Issues & Solutions

### Issue 1: "Module not found" Error
**Solution:** Ensure all `__init__.py` files exist in directories:
```bash
touch src/__init__.py
touch src/matching/__init__.py
touch src/data/__init__.py
touch src/utils/__init__.py
```

### Issue 2: Data Files Not Loading
**Symptoms:** "File not found" errors
**Solution:** 
- Ensure `data/` directory is committed to git
- Check file paths in `src/data/loader.py`
- Verify CSV/JSON files are valid

### Issue 3: PDF Features Not Working
**Symptoms:** OpenAI API errors
**Solution:**
- Add `OPENAI_API_KEY` to Streamlit secrets
- Ensure API key has credits
- Check if PDF upload size exceeds limits

### Issue 4: Slow Loading
**Solutions:**
- Use `@st.cache_data` decorators (already implemented)
- Optimize data file sizes
- Consider pagination for large datasets

## 📊 Performance Monitoring

### Built-in Streamlit Metrics
- App usage stats in Streamlit Cloud dashboard
- Error logs and performance metrics

### Custom Logging
Check logs for:
```python
logger.info("Data loaded successfully") 
logger.error("Matching failed: {error}")
```

## 🔄 Update Deployment

### Auto-Deploy (Recommended)
Streamlit Cloud auto-deploys on git push:
```bash
git add .
git commit -m "Update: added new features"
git push origin main
```

### Manual Reboot
In Streamlit Cloud dashboard:
1. Go to your app
2. Click "⋮" menu
3. Select "Reboot"

## 🔒 Security Considerations

### Data Privacy
- No personal patient data stored permanently
- All processing happens in memory
- Sessions are isolated

### API Keys
- Never commit API keys to git
- Use Streamlit secrets or environment variables
- Rotate keys regularly

### Access Control
- Streamlit Cloud apps are public by default
- For private deployment, consider Streamlit for Teams

## 🐳 Docker Deployment (Advanced)

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py"]
```

### Build and Run
```bash
docker build -t trialmatch-ai .
docker run -p 8501:8501 trialmatch-ai
```

## 🆘 Troubleshooting

### Debug Mode
Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Data Loading
```python
from src.data.loader import DataLoader
loader = DataLoader()
patients = loader.load_patients()
print(f"Loaded {len(patients)} patients")
```

### Validate Installation
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Test imports
python -c "from src.matching.engine import TrialMatchEngine"
```

## 📞 Support

**Issues with deployment?**
1. Check Streamlit Cloud logs
2. Verify all files are in git repository
3. Test locally first
4. Check GitHub Issues for common problems

**Performance issues?**
1. Monitor resource usage in dashboard
2. Optimize data loading with caching
3. Consider reducing dataset size for testing