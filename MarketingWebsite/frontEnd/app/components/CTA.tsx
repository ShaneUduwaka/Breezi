"use client";

import { motion } from "framer-motion";
import Link from "next/link";

export default function CTA() {
  return (
    <section className="py-24 bg-[#050509] relative overflow-hidden">
      {/* Background Glow */}
      <div className="absolute inset-0 bg-linear-to-b from-transparent to-blue-900/20 pointer-events-none" />

      <div className="max-w-5xl mx-auto px-6 relative z-10 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="bg-linear-to-r from-purple-900/50 to-blue-900/50 border border-white/10 rounded-3xl p-12 md:p-20 backdrop-blur-md"
        >
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
            Ready to Transform Your Customer Experience?
          </h2>
          <p className="text-gray-300 text-lg md:text-xl max-w-2xl mx-auto mb-10">
            Join hundreds of businesses using Breezi to automate calls, save
            costs, and delight customers 24/7.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/contact" className="w-full sm:w-auto">
              <button className="w-full px-8 py-4 bg-white text-black font-bold rounded-full hover:bg-gray-200 transition-colors shadow-[0_0_20px_rgba(255,255,255,0.3)]">
                Get Started
              </button>
            </Link>
            <button className="w-full sm:w-auto px-8 py-4 bg-transparent border border-white/30 text-white font-medium rounded-full hover:bg-white/10 transition-colors">
              Demo
            </button>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
