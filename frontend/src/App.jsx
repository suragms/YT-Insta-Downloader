import { useState } from "react";

export default function App() {
    const [url, setUrl] = useState("");
    const [format, setFormat] = useState("mp4");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [loadingMessage, setLoadingMessage] = useState("");
    const [connectionError, setConnectionError] = useState(null);

    const handleDownload = async () => {
        if (!url) return alert("Paste URL");

        setLoading(true);
        setResult(null);
        setConnectionError(null);
        setLoadingMessage("Connecting to server...");

        try {
            const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:5000";

            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 90000); // 90s for Render free tier wake-up

            // Update message after 3 seconds if still loading
            const messageTimeout = setTimeout(() => {
                setLoadingMessage("Server is waking up (this may take 30-60s on free tier)...");
            }, 3000);

            const res = await fetch(`${apiUrl}/download`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url, format }),
                signal: controller.signal
            });

            clearTimeout(timeoutId);
            clearTimeout(messageTimeout);
            setLoadingMessage("Processing your request...");

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.error || "Server error");
            }

            setResult(data);
        } catch (err) {
            if (err.name === 'AbortError') {
                setConnectionError("Request timed out. The server may be waking up (Render free tier). Wait ~1 minute, then click Download again.");
            } else if (err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
                setConnectionError("Cannot connect — backend may be sleeping (Render free tier takes 30–60s to wake). Wait ~1 minute, then click Download again.");
            } else {
                setConnectionError(err.message);
            }
        }

        setLoading(false);
        setLoadingMessage("");
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-zinc-900 text-white font-sans p-4">

            <h1 className="text-4xl font-bold mb-8 text-transparent bg-clip-text bg-gradient-to-r from-red-500 to-purple-600 flex items-center gap-2">
                <span>🎬</span> YT & Insta Downloader
            </h1>

            <div className="w-full max-w-md bg-zinc-800 p-6 rounded-2xl shadow-xl border border-zinc-700">
                <input
                    placeholder="Paste YouTube or Instagram link..."
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    className="w-full p-4 bg-zinc-900 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-purple-500 transition-colors"
                />

                <select
                    value={format}
                    onChange={(e) => setFormat(e.target.value)}
                    className="w-full mt-4 p-3 bg-zinc-900 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-purple-500 cursor-pointer"
                >
                    <option value="mp4">Video (MP4)</option>
                    <option value="mp3">Audio (MP3)</option>
                    <option value="jpg">Photo (JPG) - Instagram Only</option>
                </select>

                <button
                    onClick={handleDownload}
                    disabled={loading}
                    className="w-full mt-6 py-3 bg-red-600 hover:bg-red-700 disabled:bg-red-800 text-white font-bold rounded-lg transition-all flex justify-center items-center gap-2"
                >
                    {loading ? loadingMessage || "Processing..." : "Download Now"}
                </button>

                {connectionError && (
                    <p className="mt-4 p-3 bg-amber-500/20 border border-amber-500/50 rounded-lg text-amber-200 text-sm">
                        {connectionError}
                    </p>
                )}
            </div>

            {result && (
                <div className="mt-8 text-center animate-fade-in max-w-lg w-full bg-zinc-800 p-6 rounded-2xl border border-zinc-700">
                    <img src={result.thumbnail} className="w-full rounded-lg shadow-lg mb-4" alt="Thumbnail" />
                    <h3 className="text-xl font-bold mb-2 line-clamp-2">{result.title}</h3>
                    <p className="text-zinc-400 text-sm mb-4">{result.author}</p>

                    <a href={result.download_url} target="_blank" rel="noopener noreferrer">
                        <button className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg transition-colors shadow-lg shadow-green-900/20">
                            Click to Save File
                        </button>
                    </a>
                </div>
            )}

        </div>
    );
}
