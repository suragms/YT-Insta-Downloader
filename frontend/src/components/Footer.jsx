import React from 'react';

const Footer = () => {
    return (
        <footer className="w-full py-8 text-center text-slate-500 text-sm mt-auto border-t border-white/5 bg-black/20 backdrop-blur-sm">
            <div className="container mx-auto px-4">
                <p className="mb-2">© {new Date().getFullYear()} YTDownloader. Crafted for educational purposes.</p>
                <div className="flex justify-center gap-4 mt-4">
                    <a href="#" className="hover:text-white transition-colors">Privacy Policy</a>
                    <a href="#" className="hover:text-white transition-colors">Terms of Service</a>
                    <a href="#" className="hover:text-white transition-colors">Contact</a>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
