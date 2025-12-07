# 🚀 Deploy Backend to Vercel - Quick Guide

## Prerequisites

- GitHub account with code pushed
- Vercel account (free tier available)
- Environment variables ready

## Step 1: Push Code to GitHub

```bash
cd /Users/ammadkhan/coding/giaic-robotics-book-hackathon
git add .
git commit -m "Add Vercel deployment config"
git push origin main
```

## Step 2: Create Vercel Account

1. Go to https://vercel.com
2. Click "Sign up"
3. Choose "Continue with GitHub"
4. Authorize Vercel

## Step 3: Import Project

1. Click "Add New..." → "Project"
2. Select `humanoid-robotics-book` repository
3. Click "Import"

## Step 4: Configure Project

In the import screen:

**Framework Preset:** Other
**Root Directory:** `chatbot/backend`

## Step 5: Add Environment Variables

Click "Environment Variables" and add:

```
GEMINI_API_KEY          → Your Gemini API key
QDRANT_URL              → Your Qdrant cluster URL
QDRANT_API_KEY          → Your Qdrant API key
DATABASE_URL            → (Optional) Neon DB URL
APP_ENV                 → production
CORS_ORIGINS            → https://your-docusaurus-domain.com
GENERATION_MODEL        → gemini-2.5-flash
EMBEDDING_MODEL         → models/text-embedding-004
BOOK_DOCS_PATH          → ../../humanoid-robotics-book/docs
TOP_K_RESULTS           → 5
SIMILARITY_THRESHOLD    → 0.5
```

## Step 6: Deploy

Click "Deploy"

Wait 2-3 minutes for deployment to complete.

## Step 7: Get Your URL

After deployment, you'll see a URL like:
```
https://humanoid-robotics-chatbot.vercel.app
```

## Step 8: Test Backend

```bash
curl https://humanoid-robotics-chatbot.vercel.app/health
```

Should return:
```json
{
  "status": "healthy",
  "qdrant_connected": true,
  "database_connected": true,
  "timestamp": "..."
}
```

## Step 9: Index Documents

```bash
curl -X POST https://humanoid-robotics-chatbot.vercel.app/chat/index \
  -H "Content-Type: application/json" \
  -d '{"force_reindex": false}'
```

Wait 5-10 minutes for indexing.

## Step 10: Update Frontend

Edit: `humanoid-robotics-book/src/components/ChatbotWidget/ChatbotWidget.tsx`

Change line 64:
```typescript
// From:
const response = await fetch('http://localhost:8000/chat/query', {

// To:
const response = await fetch('https://humanoid-robotics-chatbot.vercel.app/chat/query', {
```

## ✅ Your Live URLs

- **Backend API:** `https://humanoid-robotics-chatbot.vercel.app`
- **API Docs:** `https://humanoid-robotics-chatbot.vercel.app/docs`
- **Health:** `https://humanoid-robotics-chatbot.vercel.app/health`

## ⚠️ Vercel Limitations & Solutions

### Issue: Long Request Timeout (>60 seconds)
Vercel has a 60-second timeout for serverless functions.

**Solution:** Indexing will timeout. Use Vercel for API only, NOT for indexing.

**Workaround:**
1. Index documents locally before deployment
2. Or index from a scheduled task
3. Or accept that indexing must be done separately

### Issue: Function Needs to be Long-Running
FastAPI works fine on Vercel for normal requests (< 60 seconds)

**For Document Indexing:**
```bash
# Index BEFORE you deploy
cd chatbot/backend
source venv/bin/activate
python -c "
from utils.document_loader import load_and_chunk_all
from services.qdrant_service import qdrant_service
from services.gemini_service import gemini_service

texts, metadatas = load_and_chunk_all()
qdrant_service.create_collection()
count = qdrant_service.add_documents(
    texts,
    [gemini_service.generate_embedding(t) for t in texts],
    metadatas
)
print(f'Indexed {count} documents')
"
```

Then deploy with already-indexed Qdrant.

## 🔄 Auto-Deployment

Vercel automatically redeploys when you push to GitHub:

```bash
git add .
git commit -m "Update chatbot"
git push origin main
# Vercel auto-deploys!
```

## 📊 Monitoring

View logs in Vercel dashboard:
1. Go to https://vercel.com/dashboard
2. Click your project
3. View "Deployments" and "Logs"

## 💡 Pro Tips

1. **Index before deploying** - Don't rely on post-deployment indexing
2. **Use environment variables** - Never hardcode secrets
3. **Monitor cold starts** - First request might be slow
4. **Keep dependencies minimal** - Faster deployments
5. **Test locally first** - Verify everything works locally

## 🆘 Troubleshooting

**Deployment fails?**
- Check build logs in Vercel dashboard
- Verify Python version is 3.11+
- Ensure all requirements are in requirements.txt

**CORS errors?**
- Add frontend domain to CORS_ORIGINS
- Redeploy

**502 Bad Gateway?**
- Check function logs
- Verify Qdrant is reachable
- Check API key validity

**Timeout on indexing?**
- Index locally before deployment
- Or index from command line after deployment fails

## 📝 Files Created

- `vercel.json` - Vercel configuration
- `Dockerfile` - Docker config (optional, for reference)
- `.dockerignore` - Docker ignore file (optional)

---

**Time: ~10 minutes** ⏱️

**Difficulty: Medium** (Vercel has 60s timeout limitation)

**Recommendation:** Consider Render.com or Railway for easier deployment with long-running processes.

---

## 🎯 Complete Deployment URL

```
https://humanoid-robotics-chatbot.vercel.app
```

Replace in ChatbotWidget.tsx and you're done! 🚀
