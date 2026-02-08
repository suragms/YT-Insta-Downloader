import React, { useState } from 'react';
import { fetchVideoInfo } from '../utils/mockApi';
import ResultCard from './ResultCard';

const Downloader = () => {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [result, setResult] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!url.trim()) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const data = await fetchVideoInfo(url);
            setResult(data);
        } catch (err) {
            setError(err.message || 'Failed to fetch video. Please check the URL.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="w-full max-w-4xl mx-auto px-4 z-10 relative">
            <div className="text-center mb-10">
                <h2 className="text-4xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400 mb-4 animate-slide-up">
                    Download YouTube Videos
                </h2>
                <p className="text-lg text-gray-400 max-w-2xl mx-auto animate-slide-up animation-delay-100">
                    Convert and download YouTube videos in MP4, MP3, and more qualities instantly.
                </p>
            </div>

            <div className="bg-white/5 backdrop-blur-xl border border-white/10 p-2 rounded-2xl shadow-2xl animate-slide-up animation-delay-200">
                <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-2">
                    <input
                        type="text"
                        className="flex-1 bg-transparent border-none text-white placeholder-gray-500 px-6 py-4 text-lg focus:ring-0 rounded-xl outline-none"
                        placeholder="Paste YouTube link here..."
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                    />
                    <button
                        type="submit"
                        disabled={loading}
                        className="bg-red-600 hover:bg-red-700 disabled:bg-red-800 text-white font-bold py-4 px-8 rounded-xl transition-all flex items-center justify-center gap-2 min-w-[160px]"
                    >
                        {loading ? (
                            <>
                                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                <span>Processing</span>
                            </>
                        ) : (
                            'Start'
                        )}
                    </button>
                </form>
            </div>

            {error && (
                <div className="mt-6 p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-200 text-center animate-fade-in">
                    {error}
                </div>
            )}

            {result && <ResultCard result={result} />}
        </div>
    );
};

export default Downloader;
