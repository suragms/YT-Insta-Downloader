import React from 'react';

const Navbar = () => {
    return (
        <nav className="w-full p-6 flex justify-between items-center backdrop-blur-md bg-black/20 border-b border-white/5 fixed top-0 z-50 transition-all duration-300">
            <div className="flex items-center gap-3 group cursor-pointer">
                <div className="w-10 h-10 bg-gradient-to-br from-red-600 to-red-800 rounded-xl flex items-center justify-center shadow-lg shadow-red-500/20 group-hover:scale-105 transition-transform duration-300">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z" />
                    </svg>
                </div>
                <h1 className="text-2xl font-bold tracking-tight text-white group-hover:text-red-500 transition-colors">
                    YT<span className="text-red-500 group-hover:text-white transition-colors">Downloader</span>
                </h1>
            </div>

            <div className="hidden md:flex items-center gap-6">
                <a href="#" className="text-gray-300 hover:text-white transition-colors text-sm font-medium">How to use</a>
                <a href="#" className="text-gray-300 hover:text-white transition-colors text-sm font-medium">Features</a>
                <button className="px-5 py-2 bg-white/10 hover:bg-white/20 text-white rounded-full text-sm font-medium transition-all border border-white/5 hover:border-white/10">
                    Get Started
                </button>
            </div>
        </nav>
    );
};

export default Navbar;
