# YT-Insta-Downloader

A full-stack application for downloading videos from YouTube and Instagram.

## Features

- Download videos from YouTube
- Download videos from Instagram
- Responsive web interface
- Built with React and Node.js

## Tech Stack

- **Frontend**: React, Vite, Tailwind CSS
- **Backend**: Python Flask
- **Deployment**: Docker, Render

## Project Structure

- `frontend/` - React application with components for UI
- `backend/` - Python Flask server

## Setup Instructions

### Frontend

1. Navigate to the frontend directory: `cd frontend`
- Install dependencies: `npm install`
- Start the development server: `npm run dev`

### Backend

1. Navigate to the backend directory: `cd backend`
- Install dependencies: `pip install -r requirements.txt`
- Run the server: `python app.py`

## Deployment (Render + Firebase)

### Backend on Render

1. Connect your repo; Render will use `render.yaml` and build from `backend/` with the Dockerfile.
2. **PORT** is set automatically by Render; the app binds to it (no extra config).
3. Optional: add **YOUTUBE_COOKIES_BASE64** in Render Dashboard → Environment if you need cookies for restricted videos.
4. After deploy, copy your backend URL (e.g. `https://yt-downloader-backend-xxxx.onrender.com`).

### Frontend on Firebase

1. Set the backend URL in **`frontend/.env.production`**:
   ```bash
   VITE_API_URL=https://YOUR-RENDER-SERVICE-URL.onrender.com
   ```
2. Build and deploy:
   ```bash
   cd frontend
   npm run build
   firebase deploy
   ```
3. The built app uses `VITE_API_URL` from `.env.production`; do not use `.env.local` for production builds.

### Common post-host issues

| Issue | Fix |
|-------|-----|
| "Cannot connect to server" | Render free tier sleeps after ~15 min; first request can take 30–60s to wake. Show a “Waking up…” message and retry. |
| CORS errors | Backend allows all origins; if you restrict later, add your Firebase URL (e.g. `https://your-app.web.app`) to CORS. |
| Download/thumbnail links broken | Backend uses `request.host_url` so links point to your Render URL; ensure the backend is deployed and reachable. |
| Wrong API URL in production | Run `npm run build` from `frontend/` so Vite uses `.env.production`; avoid building with `.env.local` (localhost). |

### Firebase deploy: "Failed to make request" or timeout

If `firebase deploy` fails with **Failed to make request to firebasehosting.googleapis.com** or **An unexpected error**:

1. **Re-authenticate** (fixes expired or invalid login):
   ```bash
   firebase login --reauth
   ```
   Complete the browser sign-in, then run `firebase deploy` again.

2. **Enable Firebase Hosting API** (if you get 403 or "resource not accessible"):
   - Open [Google Cloud Console](https://console.cloud.google.com/) → select project **yt-insta-downloader**.
   - APIs & Services → **Enable APIs and Services** → search **Firebase Hosting API** → Enable.

3. **Network / firewall**: Ensure your network allows HTTPS to `firebasehosting.googleapis.com` and `googleapis.com`. Disable VPN or try another network if needed.

4. **Deploy only hosting** (sometimes more reliable):
   ```bash
   cd frontend
   npm run build
   firebase deploy --only hosting
   ```

## Author

surag