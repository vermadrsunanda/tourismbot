# Deployment Guide

This guide covers deployment of Tourism Bot to Streamlit Cloud and Vercel.

## Prerequisites

- GitHub account
- Streamlit Cloud account (free)
- Vercel account (free)
- Mistral AI API key

## Option 1: Deploy to Streamlit Cloud (Recommended)

### Steps:

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/tourism-bot.git
   git push -u origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit https://share.streamlit.io
   - Click "New app"
   - Select your GitHub repository
   - Choose the main branch
   - Set main file path to `streamlit_app.py`

3. **Configure Secrets**
   - In Streamlit Cloud dashboard, go to your app settings
   - Add secrets under "Advanced settings" > "Secrets"
   - Add: `MISTRAL_API_KEY=your_api_key_here`

4. **Deploy**
   - Click "Deploy"
   - Your app will be live at `https://your-username-tourism-bot.streamlit.app`

## Option 2: Deploy Flask to Vercel

### Steps:

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Create Vercel Python runtime**
   Create `api/index.py`:
   ```python
   from src.app import app as flask_app
   
   def handler(request):
       return flask_app(request)
   ```

3. **Login to Vercel**
   ```bash
   vercel login
   ```

4. **Deploy**
   ```bash
   vercel --prod
   ```

5. **Set Environment Variables**
   - In Vercel dashboard: Settings > Environment Variables
   - Add: `MISTRAL_API_KEY=your_api_key_here`
   - Add: `FLASK_ENV=production`

6. **Access your app**
   - Your app will be live at `https://your-project.vercel.app`

## Option 3: Deploy to Railway

### Steps:

1. **Push to GitHub** (same as Streamlit)

2. **Go to Railway.app**
   - Connect your GitHub repository
   - Railway will auto-detect it's a Python app

3. **Configure variables**
   - Set `MISTRAL_API_KEY` in Railway dashboard
   - Set `FLASK_ENV=production`

4. **Deploy**
   - Railway auto-deploys on every push

## Environment Variables

Required for all deployments:
- `MISTRAL_API_KEY`: Your Mistral AI API key

Optional:
- `OPENWEATHER_API_KEY`: For real OpenWeatherMap data (free tier available)
- `FLIGHT_API_KEY`: For real flight data (paid API)
- `FLASK_ENV`: Set to "production" for production

## Monitoring

### Streamlit Cloud
- Logs visible in Streamlit Cloud dashboard
- Real-time monitoring
- Free tier suitable for low-traffic apps

### Vercel
- Access logs: `vercel logs`
- Monitoring dashboard available
- Generous free tier (100 GB/month)

### Railway
- Built-in monitoring and logs
- Free tier: $5 credit/month

## Scaling

### Streamlit Cloud
- Free tier limited to 1 GB RAM
- Pro tier available for production apps

### Vercel
- Auto-scaling serverless functions
- Generous free tier: 100 GB bandwidth/month

### Railway
- Auto-scaling available
- Pay-per-use pricing

## Performance Tips

1. **Cache API calls** - Use Streamlit's `@st.cache_data` for weather/flight data
2. **Optimize images** - Use WebP format
3. **Minimize bundle size** - Only include necessary dependencies
4. **Use CDN** - Vercel automatically uses Edge Network

## Troubleshooting

### Streamlit Cloud Issues

**App not deploying**
- Check `streamlit_app.py` exists in repo root
- Verify all dependencies are in `requirements.txt`
- Check logs in Streamlit Cloud dashboard

**API key not loading**
- Ensure secret is named exactly `MISTRAL_API_KEY`
- Restart the app after adding secrets

### Vercel Issues

**504 Gateway Timeout**
- Increase maxDuration in `vercel.json`
- Optimize API calls
- Use caching

**Module not found**
- All dependencies must be in `requirements.txt`
- Rebuild: `vercel --prod --force`

## Cost Estimation

### Streamlit Cloud
- Free tier: $0/month
- Pro tier: $10/month

### Vercel
- Free tier: $0/month (generous limits)
- Pro: $20/month for additional features

### Railway
- Free tier: $5 credit/month (~4-8 hours typical usage)
- Pay-per-use: ~$0.50/hour

## Domain Setup

### Streamlit Cloud
- Free `.streamlit.app` subdomain
- Custom domain: $10/month with Pro plan

### Vercel
- Free `.vercel.app` subdomain
- Custom domain: Free (bring your own)

### Railway
- Free `.railway.app` subdomain
- Custom domain: Free (bring your own)

## Continuous Deployment

All platforms support automatic deployment on git push:
1. Connect your GitHub repository
2. Choose deployment branch (usually `main`)
3. Automatic deployments on every push

## Security Best Practices

1. **Never commit API keys** - Use `.env` locally, secrets in cloud
2. **Use HTTPS only** - All platforms provide HTTPS by default
3. **Validate inputs** - Already implemented in the app
4. **Rate limiting** - Implement in production
5. **Monitor logs** - Check for unusual activity

## Next Steps

1. Choose your preferred platform
2. Push code to GitHub
3. Connect repository to deployment platform
4. Add environment variables
5. Deploy and test
6. Monitor performance

For more details:
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)
- [Vercel Python Docs](https://vercel.com/docs/concepts/functions/serverless-functions/python)
- [Railway Docs](https://docs.railway.app)
