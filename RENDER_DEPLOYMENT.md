# 🚀 Render.com Deployment Guide

Complete step-by-step guide to deploy your FastAPI chatbot backend to Render.com

## Prerequisites

- GitHub account with your repository pushed
- Render.com account (free tier available)
- Environment variables ready from `.env` file

## Step 1: Push Code to GitHub

Make sure all your code is pushed to GitHub:

```bash
cd /Users/ammadkhan/coding/giaic-robotics-book-hackathon
git add .
git commit -m "Add chatbot backend for production deployment"
git push origin main
```

## Step 2: Create Render.com Account

1. Go to https://render.com
2. Click "Sign up"
3. Choose "Sign up with GitHub"
4. Authorize Render to access your GitHub repositories

## Step 3: Create New Web Service

1. Click the **New +** button in the top-right
2. Select **Web Service**
3. Choose your `humanoid-robotics-book` repository
4. Click **Connect**

## Step 4: Configure Service

Fill in the following details:

### Basic Configuration
```
Name: humanoid-robotics-chatbot
Runtime: Python 3
Region: Choose closest to you (e.g., Oregon, Frankfurt)
Branch: main
Root Directory: chatbot/backend
```

### Build & Start Commands
```
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port 8000
```

### Plan
- Select **Free** tier (sufficient for hackathon)

## Step 5: Add Environment Variables

After clicking "Create Web Service", you'll be taken to the dashboard.

Go to **Environment** section and add each variable:

```
GEMINI_API_KEY=your_actual_gemini_key
QDRANT_URL=https://your-qdrant-url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=postgresql://your-neon-db-url
APP_ENV=production
CORS_ORIGINS=https://your-docusaurus-domain.com
GENERATION_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=models/text-embedding-004
BOOK_DOCS_PATH=../../humanoid-robotics-book/docs
TOP_K_RESULTS=5
SIMILARITY_THRESHOLD=0.5
```

### Getting Your Values

**GEMINI_API_KEY:**
- Go to https://aistudio.google.com/app/apikey
- Copy your API key

**QDRANT_URL & QDRANT_API_KEY:**
- Go to https://cloud.qdrant.io
- Log in to your account
- Copy cluster URL and API key

**DATABASE_URL (optional):**
- Go to https://neon.tech
- Copy your connection string

**CORS_ORIGINS:**
- Replace with your actual Docusaurus domain
- Format: `https://yourdomain.com`

## Step 6: Deploy

1. After adding environment variables, click **Deploy**
2. Watch the logs for build progress
3. Wait 3-5 minutes for deployment to complete
4. Once live, you'll see a URL like: `https://humanoid-robotics-chatbot.onrender.com`

## Step 7: Test Your Deployment

Test the health endpoint:

```bash
curl https://humanoid-robotics-chatbot.onrender.com/health
```

You should get:
```json
{
  "status": "healthy",
  "qdrant_connected": true,
  "database_connected": true,
  "timestamp": "2025-12-07T..."
}
```

## Step 8: Index Documents on Production

Once deployed, index your documents:

```bash
curl -X POST https://humanoid-robotics-chatbot.onrender.com/chat/index \
  -H "Content-Type: application/json" \
  -d '{"force_reindex": false}'
```

This will take 5-10 minutes. Check logs to verify completion.

## Step 9: Update Frontend

Edit your frontend to use the production backend URL.

**File:** `humanoid-robotics-book/src/components/ChatbotWidget/ChatbotWidget.tsx`

Change line ~64:
```typescript
// From:
const response = await fetch('http://localhost:8000/chat/query', {

// To:
const response = await fetch('https://humanoid-robotics-chatbot.onrender.com/chat/query', {
```

Or use environment variable approach:

```typescript
const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
const response = await fetch(`${backendUrl}/chat/query`, {
```

Then set in Docusaurus build:
```bash
REACT_APP_BACKEND_URL=https://humanoid-robotics-chatbot.onrender.com npm run build
```

## Step 10: Update CORS Origins

If you get CORS errors, update your backend environment variable:

1. Go to Render dashboard
2. Select your service
3. Go to **Environment**
4. Edit **CORS_ORIGINS** to include your Docusaurus domain:
```
https://your-docusaurus-site.com,https://www.your-docusaurus-site.com
```
5. Click **Save**
6. Service will auto-redeploy

## 🎯 Your Live URLs

**Backend API:** `https://humanoid-robotics-chatbot.onrender.com`

**API Documentation:** `https://humanoid-robotics-chatbot.onrender.com/docs`

**Health Check:** `https://humanoid-robotics-chatbot.onrender.com/health`

## 📊 Monitoring & Logs

View your service logs in Render dashboard:

1. Go to https://dashboard.render.com
2. Click on your service
3. View **Logs** tab for real-time updates

## 🔄 Automatic Redeployment

Render automatically redeploys when you push to GitHub:

1. Push changes to `main` branch
2. Render automatically builds and deploys
3. No manual action needed!

## ⚠️ Troubleshooting

### Service won't start
- Check **Build Logs** tab for errors
- Verify all environment variables are set
- Check Python version (should be 3.11)

### 502 Bad Gateway
- Backend crashed, check **Logs** tab
- Verify Qdrant is reachable
- Check API key validity

### CORS errors
- Add frontend domain to CORS_ORIGINS
- Format: `https://yourdomain.com`

### Slow responses
- Ensure documents are indexed
- Check Qdrant connection
- Verify Gemini API is working

### Free tier running out
- Render free tier services spin down after 15 minutes of inactivity
- Upgrade to paid plan for always-on service

## 💡 Pro Tips

1. **Monitor Build Time:** Free tier has limits; optimize dependencies
2. **Use Environment Variables:** Never commit secrets
3. **Enable Auto-Deploy:** Set in GitHub integration
4. **Scale When Needed:** Upgrade to paid plan for more resources
5. **Keep Backups:** Regularly backup your Qdrant data

## 🚀 Next Steps

1. ✅ Deploy backend
2. ✅ Update frontend URLs
3. ✅ Deploy frontend to Vercel/Netlify
4. ✅ Test end-to-end
5. ✅ Submit to hackathon!

---

**Questions?** Check Render docs: https://render.com/docs

**Need help?** Review the logs in Render dashboard!
