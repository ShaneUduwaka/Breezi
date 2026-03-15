import { FaArrowRight, FaBookOpen, FaPlayCircle, FaFileDownload } from "react-icons/fa";

export default function BlogSidebar() {
  const trendingArticles = [
    { title: "AI vs Human Call Centers: A Meta-Analysis", id: 1 },
    { title: "Cost Savings of AI Automation in Healthcare", id: 2 },
    { title: "RAG for Customer Support Bots Explained", id: 3 },
    { title: "Building Voice AI Systems: Best Practices", id: 4 }
  ];

  const knowledgeHub = [
    { title: "What is Conversational AI?", icon: <FaBookOpen className="text-purple-400" /> },
    { title: "How Speech Recognition Works", icon: <FaPlayCircle className="text-blue-400" /> },
    { title: "LLM vs Traditional Models", icon: <FaBookOpen className="text-pink-400" /> },
    { title: "Call Center Automation Stack", icon: <FaBookOpen className="text-indigo-400" /> },
  ];

  return (
    <div className="lg:w-1/3 flex flex-col gap-10">
      
      {/* TRENDING WIDGET */}
      <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
          <h3 className="text-lg font-bold mb-6 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" /> Trending Now
          </h3>
          <div className="flex flex-col gap-5">
              {trendingArticles.map((article, i) => (
                  <div key={article.id} className="flex gap-4 group cursor-pointer items-center">
                      <span className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-b from-gray-500 to-gray-800 group-hover:from-purple-400 group-hover:to-purple-600 transition-all opacity-50">
                        0{i+1}
                      </span>
                      <p className="text-sm font-medium text-gray-300 group-hover:text-white leading-tight">
                          {article.title}
                      </p>
                  </div>
              ))}
          </div>
      </div>

      {/* AI KNOWLEDGE HUB */}
      <div className="bg-gradient-to-b from-purple-900/20 to-transparent border border-purple-500/20 rounded-2xl p-6 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-purple-500/10 blur-2xl rounded-full" />
          <h3 className="text-lg font-bold mb-2">AI Knowledge Hub</h3>
          <p className="text-sm text-gray-400 mb-6">Master the fundamentals of conversational AI and voice agents.</p>
          
          <div className="flex flex-col gap-3 relative z-10">
              {knowledgeHub.map((item, i) => (
                  <div key={i} className="flex items-center justify-between p-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 cursor-pointer transition group">
                      <div className="flex items-center gap-3">
                          <div className="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center group-hover:scale-110 transition-transform">
                            {item.icon}
                          </div>
                          <span className="text-sm font-medium text-gray-200">{item.title}</span>
                      </div>
                      <FaArrowRight className="text-xs text-gray-600 group-hover:text-purple-400 transition-colors group-hover:translate-x-1" />
                  </div>
              ))}
          </div>
      </div>

      {/* EDUCATIONAL RESOURCES */}
      <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
          <h3 className="text-lg font-bold mb-6">Resources & Guides</h3>
          <div className="flex flex-col gap-4">
              <div className="group cursor-pointer border border-white/10 rounded-xl p-4 hover:border-blue-500/50 hover:bg-blue-500/5 transition relative overflow-hidden">
                  <div className="relative z-10">
                      <div className="flex justify-between items-start mb-2">
                          <span className="text-[10px] font-bold text-blue-400 uppercase tracking-widest bg-blue-500/10 px-2 py-1 rounded">Whitepaper</span>
                          <FaFileDownload className="text-gray-500 group-hover:text-blue-400 transition" />
                      </div>
                      <h4 className="text-sm font-semibold mb-1 text-gray-200 group-hover:text-white mt-3">AI Call Center Implementation Guide</h4>
                      <p className="text-xs text-gray-500 mt-2 flex items-center gap-2">
                        <span>PDF</span> • <span>4.2 MB</span>
                      </p>
                  </div>
              </div>

              <div className="group cursor-pointer border border-white/10 rounded-xl p-4 hover:border-pink-500/50 hover:bg-pink-500/5 transition relative overflow-hidden">
                  <div className="relative z-10">
                      <div className="flex justify-between items-start mb-2">
                          <span className="text-[10px] font-bold text-pink-400 uppercase tracking-widest bg-pink-500/10 px-2 py-1 rounded">Playbook</span>
                          <FaArrowRight className="text-gray-500 group-hover:text-pink-400 transition" />
                      </div>
                      <h4 className="text-sm font-semibold mb-1 text-gray-200 group-hover:text-white mt-3">Customer Support Automation</h4>
                      <p className="text-xs text-gray-500 mt-2">Interactive Web Experience</p>
                  </div>
              </div>
          </div>
      </div>
    </div>
  );
}