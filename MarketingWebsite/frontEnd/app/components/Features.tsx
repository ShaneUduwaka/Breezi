"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { FaHeadset, FaChartLine, FaGlobe, FaStar } from 'react-icons/fa';

export default function Features() {
  return (
    <section id="features" className="py-24 bg-[#050509] relative">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6 leading-tight">
            Transform Your <span className="text-blue-400">Customer Experience</span>
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto text-lg">
            Powerful features designed to help you scale your support without scaling your headcount.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <FeatureCard
            icon={<FaHeadset />}
            title="24/7 Support"
            description="Never miss a call. Breezi ensures your customers receive instant, intelligent support around the clock."
            delay={0}
          />
          <FeatureCard
            icon={<FaChartLine />}
            title="High Volume"
            description="Scale effortlessly. Manage countless concurrent conversations without wait times."
            delay={0.1}
          />
          <FeatureCard
            icon={<FaGlobe />}
            title="Multilingual"
            description="Connect globally. Support multiple languages, including Sinhala, for personalized interactions."
            delay={0.2}
          />
          <FeatureCard
            icon={<FaStar />}
            title="Personalized"
            description="Beyond scripts. Leverage context to deliver tailored responses that make customers feel valued."
            delay={0.3}
          />
        </div>
      </div>
    </section>
  );
}

function FeatureCard({ icon, title, description, delay }: { icon: React.ReactNode; title: string; description: string; delay: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay, duration: 0.5 }}
      className="bg-white/5 p-8 rounded-2xl border border-white/10 hover:border-blue-500/50 hover:bg-white/10 transition-all duration-300 group"
    >
      <div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center text-2xl text-blue-400 mb-6 group-hover:scale-110 transition-transform duration-300">
        {icon}
      </div>
      <h3 className="text-white text-xl font-semibold mb-3">{title}</h3>
      <p className="text-gray-400 text-sm leading-relaxed">{description}</p>
    </motion.div>
  );
}