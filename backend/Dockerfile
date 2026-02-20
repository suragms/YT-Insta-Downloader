# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# ffmpeg is required for yt-dlp to merge video/audio
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    nodejs \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Render sets PORT; default 5000 for local
ENV PORT=5000
EXPOSE 5000

# Run gunicorn (must bind to $PORT on Render)
# Workers: 1 (for streaming stability), Threads: 8 (for concurrency)
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --workers 1 --threads 8 --timeout 0 app:app"]
