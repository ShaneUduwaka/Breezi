import { FaCalendarAlt, FaClock, FaArrowRight } from "react-icons/fa";

export default function FeaturedArticle() {
  const featuredArticle = {
    title: "How AI Voice Agents Reduced Call Center Costs by 63%",
    summary: "Discover how implementing conversational AI routing dramatically lowered operational overhead without sacrificing customer satisfaction ratings.",
    category: "Case Studies",
    readTime: "8 min read",
    author: "Elena Rodriguez",
    date: "March 12, 2026",
    image: "https://images.unsplash.com/photo-1596524430615-b46475ddff6e?q=80&w=2070&auto=format&fit=crop", 
  };

  return (
    <section className="mb-20">
      <div className="group relative rounded-3xl overflow-hidden border border-white/10 bg-white/5 flex flex-col md:flex-row hover:border-purple-500/30 transition-all cursor-pointer">
        <div className="w-full md:w-1/2 h-64 md:h-auto relative overflow-hidden">
            <div className="absolute inset-0 bg-blue-900/20 z-10 transition-opacity group-hover:opacity-0" />
            <div className="w-full h-full bg-gradient-to-br from-purple-900/40 to-[#050509] absolute inset-0 -z-10" />
            <img 
                src={featuredArticle.image} 
                alt={featuredArticle.title} 
                className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-700"
            />
        </div>
        <div className="w-full md:w-1/2 p-8 md:p-12 flex flex-col justify-center">
          <div className="flex items-center gap-3 mb-6">
            <span className="bg-purple-600 text-white text-xs font-bold px-3 py-1 rounded-full">Featured</span>
            <span className="text-sm text-purple-400 font-medium">{featuredArticle.category}</span>
          </div>
          <h2 className="text-3xl md:text-4xl font-bold mb-4 group-hover:text-purple-300 transition-colors leading-tight">
            {featuredArticle.title}
          </h2>
          <p className="text-gray-400 mb-8 leading-relaxed text-lg">
            {featuredArticle.summary}
          </p>
          
          <div className="flex items-center justify-between mt-auto pt-6 border-t border-white/10">
            <div className="flex flex-col">
              <span className="text-sm font-medium">{featuredArticle.author}</span>
              <span className="text-xs text-gray-500 flex items-center gap-2">
                <FaCalendarAlt /> {featuredArticle.date} • <FaClock /> {featuredArticle.readTime}
              </span>
            </div>
            <div className="h-10 w-10 rounded-full bg-white/10 flex items-center justify-center group-hover:bg-purple-600 transition-colors">
              <FaArrowRight className="text-white" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
