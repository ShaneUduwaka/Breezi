import { FaClock } from "react-icons/fa";

export default function BlogGrid() {
  const blogPosts = [
    {
      title: "How AI Call Routing Works",
      summary: "AI routing systems analyze intent, sentiment, and customer history to send calls to the right agent. Learn the architecture behind it.",
      category: "AI Technology",
      readTime: "5 min read",
      author: "David Chen",
      date: "March 10, 2026",
      image: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?q=80&w=2070&auto=format&fit=crop"
    },
    {
      title: "7 Metrics Every Contact Center Should Track",
      summary: "From First Contact Resolution (FCR) to Average Handle Time (AHT) - what really matters in the AI era.",
      category: "Customer Experience",
      readTime: "6 min read",
      author: "Sarah Kim",
      date: "March 5, 2026",
      image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070&auto=format&fit=crop"
    },
    {
      title: "Voice AI Implementation Guide",
      summary: "A step-by-step framework to rolling out voice AI across your organization without disrupting current workflows.",
      category: "Guides",
      readTime: "12 min read",
      author: "Michael Torres",
      date: "Feb 28, 2026",
      image: "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?q=80&w=2070&auto=format&fit=crop"
    },
    {
      title: "LLM vs Traditional Chatbots",
      summary: "Why rigid decision-tree chatbots are dying, and how generative AI is taking over semantic understanding.",
      category: "AI Technology",
      readTime: "7 min read",
      author: "Dr. Avery Smith",
      date: "Feb 20, 2026",
      image: "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=1965&auto=format&fit=crop"
    },
    {
      title: "Scaling Customer Support with AI",
      summary: "How fast-growing startups are maintaining support quality while their user base 10x's.",
      category: "Case Studies",
      readTime: "4 min read",
      author: "Jessica Wong",
      date: "Feb 15, 2026",
      image: "https://images.unsplash.com/photo-1573164713988-8665fc963095?q=80&w=2069&auto=format&fit=crop"
    },
    {
      title: "Speech Recognition Fundamentals",
      summary: "A primer on how modern ASR (Automated Speech Recognition) engines process accents, noise, and context.",
      category: "Guides",
      readTime: "9 min read",
      author: "James Peterson",
      date: "Feb 10, 2026",
      image: "https://images.unsplash.com/photo-1589254065878-42c9da997008?q=80&w=2070&auto=format&fit=crop"
    }
  ];

  return (
    <div className="lg:w-2/3">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {blogPosts.map((post, idx) => (
              <div key={idx} className="group cursor-pointer flex flex-col rounded-2xl border border-transparent hover:border-white/10 hover:bg-white/5 transition-all p-4 -m-4">
                  <div className="w-full h-48 rounded-xl overflow-hidden mb-5 relative bg-gradient-to-br from-gray-800 to-gray-900 border border-white/5">
                      <img 
                          src={post.image} 
                          className="w-full h-full object-cover transform group-hover:scale-105 transition duration-500 opacity-80 group-hover:opacity-100"
                          alt={post.title}
                      />
                  </div>
                  <div className="flex items-center gap-3 mb-3">
                      <span className="text-xs font-semibold text-purple-400 uppercase tracking-wider">{post.category}</span>
                      <span className="text-xs text-gray-500 flex items-center gap-1"><FaClock className="text-gray-600"/> {post.readTime}</span>
                  </div>
                  <h3 className="text-xl font-bold mb-3 leading-snug group-hover:text-purple-300 transition-colors line-clamp-2">
                      {post.title}
                  </h3>
                  <p className="text-gray-400 text-sm mb-6 line-clamp-2">
                      {post.summary}
                  </p>
                  
                  <div className="flex items-center justify-between mt-auto">
                    <div className="flex items-center gap-2">
                        <div className="w-6 h-6 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 flex-shrink-0" />
                        <span className="text-xs font-medium text-gray-300">{post.author}</span>
                    </div>
                    <span className="text-xs text-gray-500">{post.date}</span>
                  </div>
              </div>
          ))}
      </div>

      <div className="mt-12 flex justify-center">
          <button className="px-6 py-3 rounded-full border border-white/20 text-sm font-medium hover:bg-white/10 transition">
              Load More Articles
          </button>
      </div>
    </div>
  );
}