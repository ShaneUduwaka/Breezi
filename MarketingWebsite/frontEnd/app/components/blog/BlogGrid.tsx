"use client";

import { useState, useEffect } from "react";
import { FaClock } from "react-icons/fa";

// Define the shape of our blog post for TypeScript
interface BlogPost {
  id: number;
  title: string;
  summary: string;
  category: string;
  readTime: string;
  author: string;
  date: string;
  image: string;
}

export default function BlogGrid() {
  const [blogPosts, setBlogPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchBlogs = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/blogs");
        if (!response.ok) throw new Error("Failed to fetch");
        const data = await response.json();
        setBlogPosts(data);
      } catch (err) {
        console.error("Error loading blogs:", err);
        setError(true);
      } finally {
        setLoading(false);
      }
    };

    fetchBlogs();
  }, []);

  // Show a clean loading state while fetching
  if (loading) {
    return (
      <div className="lg:w-2/3 flex items-center justify-center py-24">
        <div className="text-gray-400 animate-pulse text-lg">Loading the latest insights...</div>
      </div>
    );
  }

  // Show an error state if the backend is down
  if (error) {
    return (
      <div className="lg:w-2/3 flex items-center justify-center py-24 border border-red-500/20 rounded-2xl bg-red-500/5">
        <div className="text-red-400 text-center">
          <p className="font-bold">Unable to reach the Breezi Engine.</p>
          <p className="text-sm opacity-70">Make sure your FastAPI server is running on port 8000.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="lg:w-2/3">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {blogPosts.map((post) => (
          <div 
            key={post.id} 
            className="group cursor-pointer flex flex-col rounded-2xl border border-transparent hover:border-white/10 hover:bg-white/5 transition-all p-4 -m-4"
          >
            <div className="w-full h-48 rounded-xl overflow-hidden mb-5 relative bg-gradient-to-br from-gray-800 to-gray-900 border border-white/5">
              <img 
                src={post.image} 
                className="w-full h-full object-cover transform group-hover:scale-105 transition duration-500 opacity-80 group-hover:opacity-100"
                alt={post.title}
              />
            </div>
            
            <div className="flex items-center gap-3 mb-3">
              <span className="text-xs font-semibold text-purple-400 uppercase tracking-wider">{post.category}</span>
              <span className="text-xs text-gray-500 flex items-center gap-1">
                <FaClock className="text-gray-600"/> {post.readTime}
              </span>
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