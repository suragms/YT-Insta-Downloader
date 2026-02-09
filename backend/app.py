from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import yt_dlp
import requests
import urllib.parse
import sys
import subprocess
import os
import tempfile
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

# Global variable to store the path to the cookie file
COOKIE_FILE_PATH = None

@app.route("/")
def home():
    return "YouTube Downloader API running"

@app.route("/debug")
def debug():
    try:
        # Check Cookies
        cookie_status = "Not Found"
        if COOKIE_FILE_PATH and os.path.exists(COOKIE_FILE_PATH):
            cookie_size = os.path.getsize(COOKIE_FILE_PATH)
            cookie_status = f"Found (Size: {cookie_size} bytes)"
        elif os.path.exists("cookies.txt"):
            cookie_size = os.path.getsize("cookies.txt")
            cookie_status = f"Found local cookies.txt (Size: {cookie_size} bytes)"

        # Check Versions
        try:
            yt_version = subprocess.check_output([sys.executable, "-m", "yt_dlp", "--version"]).decode().strip()
        except: yt_version = "Error"
        
        try:
            node_version = subprocess.check_output(["node", "--version"]).decode().strip()
        except: node_version = "Not Found"

        # Check IP
        try:
            server_ip = subprocess.check_output(["curl", "-s", "ifconfig.me"]).decode().strip()
        except: server_ip = "Unknown"

        return jsonify({
            "cookies": cookie_status,
            "yt_dlp_version": yt_version,
            "node_version": node_version,
            "server_ip": server_ip,
            "env_cookie_var_present": bool(os.environ.get("YOUTUBE_COOKIES"))
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def setup_cookies():
    """
    Writes cookies from the environment variable to a temporary file.
    Returns the path to the temporary file or None if no cookies are present.
    """
    global COOKIE_FILE_PATH
    cookie_content = os.environ.get("YOUTUBE_COOKIES")
    
    if cookie_content:
        try:
            # Create a temporary file that persists until explicitly deleted (or OS cleans up)
            # We use delete=False so we can close it and pass the path to yt-dlp
            tf = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt', encoding='utf-8')
            tf.write(cookie_content)
            tf.close()
            COOKIE_FILE_PATH = tf.name
            logger.info(f"Successfully wrote cookies to temporary file: {COOKIE_FILE_PATH}")
            return COOKIE_FILE_PATH
        except Exception as e:
            logger.error(f"Error writing cookies to temp file: {e}")
            return None
    else:
        logger.info("No YOUTUBE_COOKIES environment variable found.")
        return None

# Initialize cookies on startup
setup_cookies()

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

        if COOKIE_FILE_PATH and os.path.exists(COOKIE_FILE_PATH):
            cmd.extend(["--cookies", COOKIE_FILE_PATH])
        elif os.path.exists("cookies.txt"): # Fallback to local file if exists
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
                "--extractor-args", "youtube:skip=webpage,configs",
                "--add-header", "Accept-Language:en-US,en;q=0.9",
            ])
            
            if fmt == "mp3":
                cmd.extend(["-f", "bestaudio/best"])
            else:
                # YouTube video - prefer pre-merged
                cmd.extend(["-f", "b[ext=mp4] / best[ext=mp4] / best"])
        
        cmd.append(url)

        # Start subprocess
        logger.info(f"Stream command: {cmd}")
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
                     error_msg = err.decode('utf-8', errors='ignore')
                     logger.error(f"yt-dlp stream process failed early: {error_msg}")
                     return

                while True:
                    chunk = proc.stdout.read(1024 * 64) 
                    if not chunk:
                        if proc.poll() is not None:
                            if proc.returncode != 0:
                                err = proc.stderr.read()
                                error_msg = err.decode('utf-8', errors='ignore')
                                logger.error(f"yt-dlp Stream Error: {error_msg}")
                            break
                    yield chunk
            except Exception as e:
                logger.error(f"Stream generation exception: {e}")
                logger.error(traceback.format_exc())
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
        logger.error(f"Stream Handle Exception: {e}")
        logger.error(traceback.format_exc())
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
        logger.error(f"Thumbnail Proxy Error: {e}")
        return f"Thumbnail Error: {str(e)}", 500

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")
    format_type = data.get("format")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    logger.info(f"Received download request for URL: {url}")

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

        if COOKIE_FILE_PATH and os.path.exists(COOKIE_FILE_PATH):
            ydl_opts["cookiefile"] = COOKIE_FILE_PATH
            logger.info("Using cookies from temp file.")
        elif os.path.exists("cookies.txt"):
            ydl_opts["cookiefile"] = "cookies.txt"
            logger.info("Using cookies from local file.")
        else:
            logger.warning("No cookies found for yt-dlp.")

        
        # Add YouTube-specific anti-bot measures
        if not is_instagram:
            ydl_opts["extractor_args"] = {
                "youtube": {
                    "skip": ["webpage", "configs"],
                }
            }
            ydl_opts["geo_bypass"] = True
            ydl_opts["nocheckcertificate"] = True

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
            except Exception as e:
                logger.error(f"yt-dlp extraction failed: {e}")
                logger.error(traceback.format_exc())
                # Re-raise to catch in outer block or handle specific errors here
                raise e
            
            # Fallback/Primary for Instagram Photos using Instaloader
            if is_instagram and (not info or not info.get("url")):
                 logger.info("yt-dlp failed, switching to Instaloader...")
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
                         logger.info(f"Instaloader processing shortcode: {shortcode}")
                         
                         post = instaloader.Post.from_shortcode(L.context, shortcode)
                         
                         final_image_url = post.url
                         title = "Instagram Photo"
                         
                         # Try to get caption as title
                         if post.caption:
                             title = post.caption[:30] + "..."
                             
                         logger.info(f"Instaloader Success! Found URL: {final_image_url}")

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
                     logger.error(f"Instaloader exception: {exc}")
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
        logger.error(f"General Download Error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": f"Server Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
