export const fetchVideoInfo = async (url) => {
    return new Promise((resolve, reject) => {
        // Simulate network delay
        setTimeout(() => {
            // Basic validation simulation
            if (!url.includes('youtube.com') && !url.includes('youtu.be')) {
                reject(new Error('Please enter a valid YouTube URL'));
                return;
            }

            // Mock success response
            resolve({
                title: "Rick Astley - Never Gonna Give You Up (Official Music Video)",
                thumbnail: "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
                duration: "3:32",
                author: "Rick Astley",
                viewCount: "1,234,567,890",
                downloadUrl: "https://filesamples.com/samples/video/mp4/sample_720x480.mp4", // Real sample video for demo
                formats: [
                    { quality: "1080p", type: "mp4", size: "128MB" },
                    { quality: "720p", type: "mp4", size: "67MB" },
                    { quality: "Audio", type: "mp3", size: "5MB" }
                ]
            });
        }, 1500);
    });
};
