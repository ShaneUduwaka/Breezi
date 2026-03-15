export default function NewsletterCapture() {
  return (
    <section className="mt-24 mb-10 bg-gradient-to-r from-purple-900/30 via-[#100b20] to-[#050509] border border-purple-500/20 rounded-3xl p-10 md:p-16 text-center max-w-4xl mx-auto relative overflow-hidden">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-purple-500/10 blur-[100px] rounded-full pointer-events-none" />
        
        <div className="relative z-10">
            <h2 className="text-3xl font-bold mb-4">Stay ahead in AI Customer Support</h2>
            <p className="text-gray-400 mb-8 max-w-md mx-auto text-lg leading-relaxed">
                Get the latest insights on AI call centers, automation strategies, and industry trends directly to your inbox.
            </p>
            
            <form className="flex flex-col sm:flex-row gap-3 max-w-lg mx-auto w-full relative">
                <div className="absolute inset-0 bg-purple-500/20 blur-xl rounded-full -z-10" />
                <input 
                    type="email" 
                    placeholder="Enter your email address" 
                    className="flex-1 bg-[#050509]/80 border border-white/10 rounded-full px-6 py-4 text-white focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition shadow-inner"
                    required
                />
                <button 
                    type="submit"
                    className="bg-white text-black font-bold px-8 py-4 rounded-full hover:bg-gray-200 hover:scale-105 active:scale-95 transition-all whitespace-nowrap"
                >
                    Subscribe
                </button>
            </form>
            <div className="flex items-center justify-center gap-2 mt-6">
                <div className="flex -space-x-2">
                    <div className="w-6 h-6 rounded-full bg-gray-600 border border-[#100b20]" />
                    <div className="w-6 h-6 rounded-full bg-gray-500 border border-[#100b20]" />
                    <div className="w-6 h-6 rounded-full bg-gray-400 border border-[#100b20]" />
                </div>
                <p className="text-xs text-gray-500">Join <span className="text-gray-300">10,000+ support leaders</span> shaping the future.</p>
            </div>
        </div>
    </section>
  );
}