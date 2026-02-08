from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import yt_dlp
import requests
import urllib.parse

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

@app.route("/")
def home():
    return "YouTube Downloader API running"

import sys
import subprocess
import os

# Check for cookies in environment variable and write to file
# Check for cookies in environment variable and write to file
try:
    if os.environ.get("YOUTUBE_COOKIES"):
        with open("cookies.txt", "w", encoding="utf-8") as f:
            f.write(os.environ.get("YOUTUBE_COOKIES"))
        print("Successfully wrote cookies from env var.")
except Exception as e:
    print(f"Error writing cookies from env var: {e}")


@app.route("/stream_handler")
def stream_handler():
    url = request.args.get("url")
    title = request.args.get("title", "download")
    fmt = request.args.get("format", "mp4")

    if not url:
        return "Missing URL", 400

    try:
        # Detect platform
        is_instagram = "instagram.com" in url
        
        # Set content-disposition early for filename
        if fmt == "jpg":
            ext = "jpg"
            mime = "image/jpeg"
        elif fmt == "mp3":
            ext = "mp3"
            mime = "audio/mpeg"
        else:
            ext = "mp4"
            mime = "video/mp4"

        filename = f"{title}.{ext}" if title else f"media.{ext}"
        safe_filename = urllib.parse.quote(filename)

        if is_instagram and fmt == "jpg":
            # Direct image proxy using requests (more reliable than yt-dlp for static images)
            fake_browser_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            }
            req = requests.get(url, headers=fake_browser_headers, stream=True)
            
            # Use upstream headers but force attachment
            return Response(
                stream_with_context(req.iter_content(chunk_size=1024)),
                headers={
                    "Content-Disposition": f"attachment; filename*=UTF-8''{safe_filename}",
                    "Content-Type": req.headers.get("Content-Type", "image/jpeg"),
                }
            )

        # Build the yt-dlp command to stream to stdout
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "-o", "-", # Output to stdout
            "--quiet", "--no-warnings", 
            "--no-playlist",
            # Anti-blocking measures (Keep generic cache clear)
            "--rm-cache-dir",
            "--no-check-certificate",
            "--geo-bypass",
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        ]

        if os.path.exists("cookies.txt"):
            cmd.extend(["--cookies", "cookies.txt"])


        # INSTAGRAM SPECIFIC LOGIC
        if is_instagram:
            if fmt == "mp3":
                # Extract audio from Reel/Video
                cmd.extend(["-f", "bestaudio/best"])
            else:
                # Video (mp4)
                cmd.extend(["-f", "best"])
        
        # YOUTUBE SPECIFIC LOGIC
        else:
            # Enhanced anti-bot measures for YouTube
            cmd.extend([
                "--extractor-args", "youtube:player_client=android,ios;skip=webpage,configs",
                "--add-header", "Accept-Language:en-US,en;q=0.9",
            ])
            
            if fmt == "mp3":
                cmd.extend(["-f", "bestaudio/best"])
            else:
                # YouTube video - prefer pre-merged
                cmd.extend(["-f", "b[ext=mp4] / best[ext=mp4] / best"])
        
        cmd.append(url)

        # Start subprocess
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Generator to yield chunks of data
        def generate():
            try:
                # Check for immediate errors
                if proc.poll() is not None and proc.returncode != 0:
                     err = proc.stderr.read()
                     print(f"yt-dlp process failed early: {err.decode('utf-8', errors='ignore')}")
                     return

                while True:
                    chunk = proc.stdout.read(1024 * 64) 
                    if not chunk:
                        if proc.poll() is not None:
                            if proc.returncode != 0:
                                err = proc.stderr.read()
                                print(f"yt-dlp Error: {err.decode('utf-8', errors='ignore')}")
                            break
                    yield chunk
            except Exception as e:
                print(f"Stream generation error: {e}")
            finally:
                proc.stdout.close()
                proc.stderr.close()
                if proc.poll() is None:
                    proc.kill()

        return Response(
            generate(),
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{safe_filename}",
                "Content-Type": mime,
            }
        )
            
    except Exception as e:
        return f"Stream Error: {str(e)}", 500

@app.route("/thumbnail_proxy")
def thumbnail_proxy():
    url = request.args.get("url")
    if not url:
        return "Missing URL", 400
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }
        req = requests.get(url, headers=headers, stream=True)
        return Response(
            stream_with_context(req.iter_content(chunk_size=1024)),
            content_type=req.headers.get("Content-Type", "image/jpeg")
        )
    except Exception as e:
        return f"Thumbnail Error: {str(e)}", 500

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")
    format_type = data.get("format")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Detect platform
        is_instagram = "instagram.com" in url

        # We just extract metadata here, we don't need the direct URL anymore
        # because the stream_handler will handle the download.
        # But we still extract info to show the title/thumbnail to the user.
        
        ydl_opts = {
            "quiet": True,
            "noplaylist": True,
            "ignoreerrors": True, # Don't crash on "No video" error
        }

        if os.path.exists("cookies.txt"):
            ydl_opts["cookiefile"] = "cookies.txt"

        
        # Add YouTube-specific anti-bot measures
        if not is_instagram:
            ydl_opts["extractor_args"] = {
                "youtube": {
                    "player_client": ["android", "ios"],
                    "skip": ["webpage", "configs"],
                }
            }
            ydl_opts["geo_bypass"] = True
            ydl_opts["nocheckcertificate"] = True

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Fallback/Primary for Instagram Photos using Instaloader
            if is_instagram and (not info or not info.get("url")):
                 print("yt-dlp failed, switching to Instaloader...")
                 try:
                     import instaloader
                     
                     # Create instance
                     L = instaloader.Instaloader(
                         download_pictures=False,
                         download_videos=False, 
                         download_video_thumbnails=False,
                         download_geotags=False,
                         download_comments=False,
                         save_metadata=False,
                         compress_json=False
                     )
                     
                     # Extract shortcode from URL
                     # https://www.instagram.com/p/SHORTCODE/
                     import re
                     match = re.search(r'/(p|reel)/([^/?#&]+)', url)
                     if match:
                         shortcode = match.group(2)
                         print(f"Instaloader processing shortcode: {shortcode}")
                         
                         post = instaloader.Post.from_shortcode(L.context, shortcode)
                         
                         final_image_url = post.url
                         title = "Instagram Photo"
                         
                         # Try to get caption as title
                         if post.caption:
                             title = post.caption[:30] + "..."
                             
                         print(f"Instaloader Success! Found URL: {final_image_url}")

                         # Construct response manually
                         safe_title = urllib.parse.quote(title)
                         safe_url = urllib.parse.quote(final_image_url)
                         safe_thumb = urllib.parse.quote(final_image_url)
                         
                         local_download_url = f"{request.host_url}stream_handler?url={safe_url}&title={safe_title}&format=jpg"
                         local_thumbnail_url = f"{request.host_url}thumbnail_proxy?url={safe_thumb}"
                         
                         return jsonify({
                            "title": title,
                            "thumbnail": local_thumbnail_url,
                            "download_url": local_download_url,
                            "duration": 0,
                            "author": post.owner_username
                         })
                     else:
                         return jsonify({"error": "Could not parse Instagram shortcode."}), 400

                 except Exception as exc:
                     print(f"Instaloader exception: {exc}")
                     return jsonify({"error": f"Instaloader failed: {str(exc)}"}), 500

            if not info:
                 return jsonify({"error": "Failed to fetch info"}), 500

            # Create a link to our OWN stream handler
            safe_title = urllib.parse.quote(info.get("title", "video"))
            safe_url = urllib.parse.quote(url) # Pass the Original YouTube URL
            safe_thumb = urllib.parse.quote(info.get("thumbnail", ""))
            
            local_download_url = f"{request.host_url}stream_handler?url={safe_url}&title={safe_title}&format={format_type}"
            local_thumbnail_url = f"{request.host_url}thumbnail_proxy?url={safe_thumb}"

            return jsonify({
                "title": info.get("title"),
                "thumbnail": local_thumbnail_url, # Use PROXY thumbnail
                "download_url": local_download_url,
                "duration": info.get("duration"),
                "author": info.get("uploader")
            })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
