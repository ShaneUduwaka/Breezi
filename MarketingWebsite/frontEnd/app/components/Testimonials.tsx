"use client";

import { motion } from "framer-motion";
import { FaQuoteLeft } from "react-icons/fa";

const testimonials = [
  {
    id: 1,
    quote: "Breezi transformed our customer service. We went from missing 30% of calls to answering 100% instantly.",
    author: "Sarah Jenkins",
    role: "Operations Director, TechFlow",
    image: "https://i.pravatar.cc/150?u=a042581f4e29026024d",
  },
  {
    id: 2,
    quote: "The Sinhala language support is incredible. It sounds completely natural and our local customers love it.",
    author: "Ruwan Perera",
    role: "CEO, LankaLogistics",
    image: "https://i.pravatar.cc/150?u=a042581f4e29026704d",
  },
  {
    id: 3,
    quote: "Setup was surprisingly easy. We were live in an afternoon and saw ROI within the first week.",
    author: "Michael Chang",
    role: "Founder, UrbanEats",
    image: "https://i.pravatar.cc/150?u=a04258114e29026302d",
  },
];

export default function Testimonials() {
  return (
    <section className="py-24 bg-[#050509] relative">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
            Trusted by <span className="text-blue-400">Industry Leaders</span>
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((item, index) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1, duration: 0.5 }}
              className="bg-white/5 border border-white/10 p-8 rounded-2xl relative hover:bg-white/10 transition-colors"
            >
              <FaQuoteLeft className="text-3xl text-purple-500/30 absolute top-6 right-6" />
              <p className="text-gray-300 text-lg mb-8 relative z-10">"{item.quote}"</p>
              <div className="flex items-center gap-4">
                <img 
                  src={item.image} 
                  alt={item.author} 
                  className="w-12 h-12 rounded-full border-2 border-purple-500/20"
                />
                <div>
                  <h4 className="text-white font-medium">{item.author}</h4>
                  <p className="text-sm text-gray-500">{item.role}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
