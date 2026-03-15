import { FaSearch } from "react-icons/fa";

export default function BlogHero() {
  return (
    <section className="text-center max-w-3xl mx-auto mb-16 relative">
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-purple-900/20 blur-[120px] rounded-full -z-10 pointer-events-none" />
      
      <h1 className="text-4xl md:text-6xl font-bold tracking-tight leading-tight mb-6">
        Insights on AI Call Centers & Customer Experience
      </h1>
      <p className="text-lg md:text-xl text-gray-400 mb-10">
        Learn how businesses are using AI agents, voice automation, and analytics to transform customer support.
      </p>

      <div className="relative max-w-lg mx-auto mb-6">
        <input 
          type="text" 
          placeholder="Search articles, guides, and case studies..." 
          className="w-full bg-white/5 border border-white/10 rounded-full py-4 pl-12 pr-6 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500/50 transition-colors"
        />
        <FaSearch className="absolute left-5 top-1/2 -translate-y-1/2 text-gray-500" />
      </div>

      <div className="flex flex-wrap justify-center gap-2">
        <span className="text-sm text-gray-400 flex items-center mr-2">Popular:</span>
        {["AI Agents", "Call Automation", "LLM", "ROI"].map((tag) => (
          <span key={tag} className="text-xs font-medium text-purple-300 bg-purple-900/30 border border-purple-500/20 px-3 py-1 rounded-full cursor-pointer hover:bg-purple-800/40 transition">
            {tag}
          </span>
        ))}
      </div>
    </section>
  );
}
