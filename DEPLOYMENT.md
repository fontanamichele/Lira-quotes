# 🚀 Deployment Guide

This guide covers multiple free hosting options for your Finance Data API.

## Option 1: Railway (Recommended) ⭐

Railway offers the best free tier with $5 monthly credit and easy GitHub integration.

### Steps:

1. **Sign up for Railway**:

   - Go to [railway.app](https://railway.app)
   - Sign up with your GitHub account

2. **Deploy from GitHub**:

   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `finance-data-api` repository
   - Railway will automatically detect it's a Python app

3. **Configure Environment**:

   - Railway will automatically use your `requirements.txt`
   - The `railway.json` file configures the deployment
   - No additional setup needed!

4. **Get Your URL**:
   - Railway will provide a URL like `https://your-app-name.up.railway.app`
   - Your API will be available at `https://your-app-name.up.railway.app/prices/current?tickers=AAPL`

### Railway Benefits:

- ✅ $5 free credit monthly
- ✅ Automatic deployments from GitHub
- ✅ No cold starts
- ✅ Built-in monitoring
- ✅ Easy custom domains

---

## Option 2: Render

Render offers 750 free hours per month with automatic deployments.

### Steps:

1. **Sign up for Render**:

   - Go to [render.com](https://render.com)
   - Sign up with your GitHub account

2. **Create Web Service**:

   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect Python

3. **Configure Service**:

   - **Name**: `finance-data-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Instance Type**: Free

4. **Deploy**:
   - Click "Create Web Service"
   - Render will build and deploy automatically

### Render Benefits:

- ✅ 750 free hours/month
- ✅ Automatic deployments
- ✅ Custom domains
- ⚠️ Sleeps after 15min inactivity (cold starts)

---

## Option 3: Fly.io

Fly.io offers 3 free shared-cpu VMs with global deployment.

### Steps:

1. **Install Fly CLI**:

   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex

   # macOS/Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Sign up and Login**:

   ```bash
   fly auth signup
   fly auth login
   ```

3. **Deploy**:

   ```bash
   fly launch
   # Follow the prompts
   fly deploy
   ```

4. **Get Your URL**:
   - Fly will provide a URL like `https://your-app-name.fly.dev`

### Fly.io Benefits:

- ✅ 3 free VMs
- ✅ Global deployment
- ✅ No cold starts
- ⚠️ More complex setup

---

## Option 4: Heroku (Paid but Cheap)

Heroku no longer has a free tier, but offers a $5/month basic plan.

### Steps:

1. **Install Heroku CLI**:

   - Download from [devcenter.heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login and Create App**:

   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Deploy**:

   ```bash
   git push heroku main
   ```

4. **Open Your App**:
   ```bash
   heroku open
   ```

---

## 🧪 Testing Your Deployed API

Once deployed, test your API with these endpoints:

```bash
# Test root endpoint
curl https://your-app-url.com/

# Test current prices
curl "https://your-app-url.com/prices/current?tickers=AAPL&currency=USD"

# Test historical prices
curl "https://your-app-url.com/prices/historical?tickers=AAPL&period=1mo"

# Test currency conversion
curl "https://your-app-url.com/prices/current?tickers=VWCE.AS&currency=USD"

# Test multiple assets
curl "https://your-app-url.com/prices/current?tickers=AAPL,TSLA,BTC-USD&currency=EUR"
```

## 🔧 Environment Variables

If you need to set environment variables:

### Railway:

- Go to your project → Variables tab
- Add variables like `PORT=8000`

### Render:

- Go to your service → Environment tab
- Add variables

### Fly.io:

```bash
fly secrets set PORT=8000
```

## 📊 Monitoring

### Railway:

- Built-in metrics and logs
- Automatic health checks

### Render:

- Service logs available in dashboard
- Uptime monitoring

### Fly.io:

```bash
fly logs
fly status
```

## 🚨 Troubleshooting

### Common Issues:

1. **Port Issues**:

   - Make sure your app binds to `0.0.0.0:8000`
   - Use `PORT` environment variable if needed

2. **Memory Issues**:

   - Some free tiers have memory limits
   - Consider optimizing your code

3. **Timeout Issues**:
   - Yahoo Finance requests might timeout
   - Add proper error handling

### Debug Commands:

```bash
# Check logs
railway logs
# or
fly logs
# or
heroku logs --tail
```

## 💡 Pro Tips

1. **Use Railway** for the best free experience
2. **Set up custom domains** for professional URLs
3. **Monitor usage** to stay within free limits
4. **Use caching** to reduce API calls
5. **Add health checks** for better monitoring

## 🎯 Recommended Setup

For the best free hosting experience:

1. **Primary**: Railway (reliable, good free tier)
2. **Backup**: Render (good alternative)
3. **Advanced**: Fly.io (if you need global deployment)

Choose Railway for simplicity and reliability! 🚀
