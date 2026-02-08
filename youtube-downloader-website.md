# 🎬 YouTube Downloader Website (React + Backend) – Full Requirements

## ⚠️ Legal Disclaimer

This project is for **educational full-stack development purposes only**.

* Downloading copyrighted YouTube videos may violate YouTube Terms of Service.
* Use only for personal/educational/demo use.
* Do not use for piracy or illegal distribution.

---

# 📌 Project Overview

A modern **YouTube video & audio downloader web app** built using:

* ⚛️ React (Frontend)
* 🐍 Python Flask (Backend API)
* 📦 yt-dlp (media extraction)
* 🎨 Modern responsive UI
* 📱 Mobile friendly design

Users can:

* Paste YouTube link
* Choose MP4 or MP3
* Fetch video info
* Download instantly

---

# 🏗️ Tech Stack

## Frontend (React)

* React.js (Vite recommended)
* Axios / Fetch API
* Tailwind CSS or custom CSS
* Responsive UI

## Backend

* Python
* Flask
* yt-dlp
* FFmpeg (required for mp3)

## Deployment

* Frontend: Netlify / Vercel
* Backend: Render / Railway

---

# 📁 Project Structure

```
yt-downloader-react/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── Downloader.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   └── Loader.jsx
│   │   │
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   │
│   └── package.json
│
└── README.md
```

---

# ⚙️ Backend Requirements (Flask)

## requirements.txt

```
Flask
flask-cors
yt-dlp
gunicorn
```

Install:

```bash
pip install -r requirements.txt
```

---

## Backend Features

* Accept YouTube URL
* Extract video info
* Return title + thumbnail
* Return download link
* Convert to MP3 (optional)
* Handle errors
* CORS enabled for React

---

## Backend API Endpoints

### 1. Health check

```
GET /
```

Response:

```
Server running
```

### 2. Download API

```
POST /download
```

Body:

```json
{
  "url": "youtube link",
  "format": "mp4 or mp3"
}
```

Response:

```json
{
  "title": "Video title",
  "thumbnail": "thumbnail link",
  "download_url": "direct file link"
}
```

---

# ⚛️ Frontend Requirements (React)

## Pages & Components

### 1. Navbar

* Logo
* Title
* Dark theme

### 2. Downloader Card

* Input field (YouTube URL)
* Format select (MP4/MP3)
* Download button
* Loading animation

### 3. Result Card

* Thumbnail preview
* Video title
* Download button

### 4. Error Handling

* Invalid URL message
* Server error message

---

# 🎨 UI Design Requirements

## Theme

* Dark modern UI
* YouTube red accent
* Glassmorphism card
* Gradient background

## Responsive

* Mobile friendly
* Tablet support
* Desktop optimized

---

# 🧠 React Functional Requirements

### Input validation

* Empty input check
* Valid YouTube link check

### Loading state

* Show spinner
* Disable button

### API connection

Use fetch or axios:

```
POST http://localhost:5000/download
```

### Result display

* Show thumbnail
* Show title
* Show download link

---

# 🛠️ Setup Instructions

## 1️⃣ Backend Setup

```
cd backend
pip install -r requirements.txt
python app.py
```

Runs:

```
http://localhost:5000
```

---

## 2️⃣ Frontend Setup

Create React app using Vite:

```
npm create vite@latest frontend
cd frontend
npm install
npm run dev
```

Runs:

```
http://localhost:5173
```

---

# 🔗 Connect React to Flask

Inside React fetch:

```
fetch("http://localhost:5000/download", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    url: videoUrl,
    format: selectedFormat
  })
})
```

---

# 🌍 Deployment Requirements

## Backend (Render)

* Upload backend to GitHub
* Deploy as web service
* Start command:

```
gunicorn app:app
```

## Frontend (Netlify)

* Upload React build

```
npm run build
```

* Deploy dist folder

---

# 🔒 Security Requirements

* Rate limiting
* Input validation
* Error handling
* Prevent spam requests

---

# 🚀 Advanced Features (Future Scope)

## Phase 2 Features

* Download history
* User login
* Dark/light mode
* Multiple quality options
* Playlist download
* Instagram downloader
* TikTok downloader

## Phase 3 (Pro SaaS)

* AdSense integration
* Premium fast download
* API access
* SEO blog
* Admin dashboard

---

# 💰 Monetization Ideas

* Google AdSense
* Affiliate links
* Premium plan
* AI tools integration

---

# 🏁 Conclusion

This project demonstrates:

* Full stack development
* React frontend
* Flask backend
* API integration
* Real world deployment
* Modern UI design

Perfect for:

* Portfolio project
* Resume
* Freelancing
* Startup idea

---

# 👨💻 Author

**Surag M S**
AI + Full Stack Developer

GitHub: [https://github.com/yourusername](https://github.com/yourusername)
Portfolio: [https://yourportfolio.com](https://yourportfolio.com)
