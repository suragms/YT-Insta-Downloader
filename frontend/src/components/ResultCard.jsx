import React from 'react';

const ResultCard = ({ result, onDownload }) => {
    if (!result) return null;

    return (
        <div className="w-full max-w-3xl mx-auto mt-8 bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl overflow-hidden shadow-2xl animate-fade-in">
            <div className="p-6 md:p-8 flex flex-col md:flex-row gap-6">
                {/* Thumbnail */}
                <div className="w-full md:w-1/3 relative group overflow-hidden rounded-lg">
                    <img
                        src={result.thumbnail}
                        alt={result.title}
                        className="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-500"
                    />
                    <div className="absolute bottom-2 right-2 bg-black/80 px-2 py-1 rounded text-xs text-white font-medium">
                        {result.duration}
                    </div>
                    <div className="absolute inset-0 bg-black/20 group-hover:bg-black/0 transition-colors"></div>
                </div>

                {/* Info */}
                <div className="flex-1 flex flex-col justify-between">
                    <div>
                        <h2 className="text-xl md:text-2xl font-bold text-white mb-2 line-clamp-2 leading-tight">
                            {result.title}
                        </h2>
                        <div className="flex items-center gap-3 text-sm text-gray-400 mb-4">
                            <span>{result.author}</span>
                            <span>•</span>
                            <span>{result.viewCount || '1.2M'} views</span>
                        </div>
                    </div>

                    <div className="flex flex-col gap-3">
                        {/* Format Selection (Mock) */}
                        <div className="grid grid-cols-2 gap-3 mb-2">
                            {result.formats?.map((fmt, idx) => (
                                <button
                                    key={idx}
                                    className="px-3 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/5 text-sm text-gray-300 flex justify-between items-center transition-colors"
                                >
                                    <span className="font-semibold">{fmt.quality}</span>
                                    <span className="text-xs opacity-70">{fmt.size}</span>
                                </button>
                            )) || (
                                    <div className="text-gray-500 text-sm">No formats available</div>
                                )}
                        </div>

                        <a
                            href={result.downloadUrl}
                            target="_blank"
                            download
                            className="w-full py-3 bg-red-600 hover:bg-red-700 text-white font-bold rounded-xl flex items-center justify-center gap-2 transition-all shadow-lg shadow-red-600/30 hover:shadow-red-600/50 transform hover:-translate-y-0.5"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
                            </svg>
                            Download Now
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ResultCard;
