# Quick Start Guide

## 5-Minute Setup

### 1. Prerequisites
- Python 3.8+
- Mistral AI API key (free at https://console.mistral.ai)

### 2. Setup
```bash
# Clone/navigate to project
cd "path/to/VSCode tourism Bot"

# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure
```bash
# Create .env file
echo "MISTRAL_API_KEY=your_key_here" > .env
```

### 4. Run (Choose One)

**Flask Version**:
```bash
python -m src.app
# Open: http://127.0.0.1:5000
```

**Streamlit Version**:
```bash
streamlit run streamlit_app.py
# Opens automatically at http://localhost:8501
```

## 🎮 Try These Commands

### Voice Demo
1. Click 🎤 Voice button
2. Say: "Tell me about Paris"
3. Listen to response

### Weather Demo
- "What's the weather in Tokyo?"
- "Is it hot in Dubai?"
- "Tell me about Singapore's climate"

### Flight Demo
- "Show flights to Bali"
- "Find flights from NYC to London"
- "Cheap flights to Thailand"

### Attractions Demo
- "What attractions in Barcelona?"
- "Top things to see in Rome"
- "Must visit places in Cairo"

## 📱 Streamlit Version (Easier)

1. Run: `streamlit run streamlit_app.py`
2. Opens in browser automatically
3. Type or use microphone 🎤
4. See weather, flights, attractions in columns

## 🌐 Deploy (2 Options)

### Option A: Streamlit Cloud (Easiest)
```bash
# 1. Push to GitHub
git push origin main

# 2. Go to https://share.streamlit.io
# 3. Click "New app"
# 4. Select your repo
# 5. App is live in 2 minutes!
```

### Option B: Vercel (Best Performance)
```bash
# 1. npm install -g vercel
# 2. vercel --prod
# 3. Set env vars in dashboard
# 4. App is live!
```

## 📚 Documentation

- **Features**: See [FEATURES.md](FEATURES.md)
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **APIs**: See [README.md](README.md)

## 🆘 Troubleshooting

**Voice not working?**
- Use Chrome, Firefox, or Safari (latest versions)
- Allow microphone access

**App won't start?**
- Check API key in .env
- Verify Python 3.8+
- Try: `pip install --upgrade -r requirements.txt`

**Deploy issues?**
- See [DEPLOYMENT.md](DEPLOYMENT.md)

## 🚀 Next Steps

1. ✅ Get it running locally
2. ✅ Try voice and weather features
3. ✅ Deploy to Streamlit Cloud
4. ✅ Share with friends!

**That's it! You're ready to use Tourism Bot! 🌍**

---

For more detailed setup, see [README.md](README.md)
