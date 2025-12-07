# Streamlit Cloud Deployment Guide - Tourism Bot

## Complete Step-by-Step Deployment

### Prerequisites
- GitHub account (free at github.com)
- Streamlit Cloud account (free at share.streamlit.io)
- Your Mistral AI API key

---

## Step 1: Initialize Git Repository

```bash
cd "c:\Users\dell\Desktop\JLT VScode\VSCode tourism Bot"

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Tourism Bot - AI Travel Assistant with voice and real-time APIs"
```

---

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create repository named `tourism-bot`
3. **DO NOT** initialize with README (we have one)
4. Click "Create repository"

---

## Step 3: Push Code to GitHub

```bash
# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/tourism-bot.git

# Rename branch to main (if needed)
git branch -M main

# Push code
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## Step 4: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "New app"
3. Fill in the form:
   - **GitHub account**: Your username
   - **Repository**: tourism-bot
   - **Branch**: main
   - **Main file path**: streamlit_app.py
4. Click "Deploy"

Streamlit will install dependencies and deploy your app!

---

## Step 5: Add Secrets (API Key)

1. Your app will appear with URL: `https://your-username-tourism-bot.streamlit.app`
2. Click the three dots (⋯) → "Manage app"
3. Go to "Settings" tab
4. Click "Secrets"
5. Add:
```
MISTRAL_API_KEY = kie6zGu4WPSsJsIym49wncywfQPSMvjP
```
6. Save and wait for auto-restart

---

## Step 6: Done! 🎉

Your app is now live at:
```
https://your-username-tourism-bot.streamlit.app
```

Test it:
- Try voice input (🎤 button)
- Ask about weather
- Search for flights
- Share the link!

---

## Troubleshooting

### App won't deploy
- Check `streamlit_app.py` exists in root
- Verify all packages are in `requirements.txt`
- Check logs in Streamlit Cloud dashboard

### API key not working
- Make sure secret is named exactly: `MISTRAL_API_KEY`
- Restart app after adding secret
- Value should be: `kie6zGu4WPSsJsIym49wncywfQPSMvjP`

### App crashes after deploy
- Check cloud logs for errors
- Verify Python 3.8+
- Make sure all imports work

---

## Update Your App

When you make changes:
```bash
git add .
git commit -m "Update features"
git push origin main
```

Streamlit automatically redeploys!

---

## Share Your App

Your live URL:
```
https://your-username-tourism-bot.streamlit.app
```

Share this with friends!

---

**Need Help?** Check DEPLOYMENT.md for more details.
