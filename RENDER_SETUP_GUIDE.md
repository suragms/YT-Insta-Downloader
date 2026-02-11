# Render Backend Setup Guide

## 🚨 Current Issue
Your backend at `https://yt-downloader-backend-j4vn.onrender.com` is not responding because:
1. The service might not be deployed correctly
2. Environment variables are not configured
3. The service might be sleeping (free tier)

## ✅ Step-by-Step Fix

### Step 1: Access Render Dashboard
1. Go to: https://dashboard.render.com
2. Log in with your account
3. Find your service: `yt-downloader-backend`

### Step 2: Check Service Status
Look for the service status:
- 🟢 **Live** = Service is running
- 🟡 **Building** = Service is deploying
- 🔴 **Failed** = Deployment failed (check logs)
- ⚪ **Suspended** = Service is sleeping

### Step 3: Configure Environment Variables
1. Click on your `yt-downloader-backend` service
2. Go to **Environment** tab on the left
3. Add/Update these environment variables:

#### Required Environment Variables:

**PORT** (Render sets this automatically, but verify it exists)
- Key: `PORT`
- Value: Leave empty (Render auto-assigns)

**YOUTUBE_COOKIES** (Critical for YouTube downloads)
- Key: `YOUTUBE_COOKIES`
- Value: Copy the ENTIRE contents of `backend/cookies.txt`
  
To get the cookies content:
```bash
# In your project directory
cd backend
type cookies.txt
```

Copy ALL the text from cookies.txt and paste it as the value for YOUTUBE_COOKIES.

### Step 4: Trigger Manual Deploy
After setting environment variables:
1. Go to **Manual Deploy** section
2. Click **"Deploy latest commit"** or **"Clear build cache & deploy"**
3. Wait for deployment to complete (5-10 minutes)

### Step 5: Check Deployment Logs
1. Click on **Logs** tab
2. Look for these success messages:
   ```
   Successfully wrote cookies to temporary file
   Running on http://0.0.0.0:10000
   ```
3. If you see errors, note them down

### Step 6: Test the Backend
Once deployed, test these URLs in your browser:

1. **Health Check**: 
   ```
   https://yt-downloader-backend-j4vn.onrender.com/
   ```
   Should return: "YouTube Downloader API running"

2. **Debug Info**:
   ```
   https://yt-downloader-backend-j4vn.onrender.com/debug
   ```
   Should return JSON with cookies status

## 🔧 Common Issues & Solutions

### Issue 1: "Service Unavailable" or Timeout
**Solution**: Free tier services sleep after 15 minutes. First request takes 30-60 seconds to wake up.
- Just wait and refresh
- Or upgrade to paid plan ($7/month) for always-on service

### Issue 2: "No cookies found"
**Solution**: YOUTUBE_COOKIES environment variable not set correctly
- Make sure you copied the ENTIRE cookies.txt content
- No extra spaces or line breaks
- Save and redeploy

### Issue 3: Build fails
**Solution**: Check logs for specific error
- Common: Missing dependencies in requirements.txt
- Common: Dockerfile syntax error
- Try "Clear build cache & deploy"

### Issue 4: "Sign-in required" errors when downloading
**Solution**: Cookies expired or invalid
- Export fresh cookies from your browser
- Update cookies.txt
- Update YOUTUBE_COOKIES in Render
- Redeploy

## 📱 Alternative: Deploy Backend Elsewhere

If Render continues to have issues, consider these alternatives:

### Option A: Railway.app
- Similar to Render
- Better free tier reliability
- Easier setup

### Option B: Fly.io
- Good free tier
- Fast deployment
- Global edge network

### Option C: Self-host on VPS
- DigitalOcean ($4/month)
- Linode ($5/month)
- Vultr ($2.50/month)
- Full control, always on

## 🎯 Quick Checklist

Before asking for help, verify:
- [ ] Render service shows "Live" status
- [ ] Environment variable YOUTUBE_COOKIES is set
- [ ] Deployment logs show no errors
- [ ] Health check URL returns "YouTube Downloader API running"
- [ ] Debug URL shows cookies found
- [ ] Waited 60 seconds for service to wake up (if it was sleeping)

## 📞 Need More Help?

If still not working:
1. Screenshot the Render logs
2. Screenshot the environment variables page
3. Test the /debug endpoint and share the response
4. Check if the service is on free tier and sleeping

---

**Last Updated**: 2026-02-11
**Backend URL**: https://yt-downloader-backend-j4vn.onrender.com
**Frontend URL**: https://yt-insta-downloader.web.app
