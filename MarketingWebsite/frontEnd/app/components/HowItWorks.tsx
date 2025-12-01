"use client";

import { motion } from "framer-motion";
import { FaNetworkWired, FaCogs, FaRocket } from "react-icons/fa";

const steps = [
  {
    id: 1,
    title: "Connect",
    description: "Integrate Breezi with your existing phone system in minutes. No hardware required.",
    icon: <FaNetworkWired />,
  },
  {
    id: 2,
    title: "Configure",
    description: "Upload your knowledge base and customize your agent's voice, tone, and language.",
    icon: <FaCogs />,
  },
  {
    id: 3,
    title: "Deploy",
    description: "Go live instantly. Watch as Breezi handles calls, books appointments, and delights customers.",
    icon: <FaRocket />,
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="py-24 bg-[#050509] relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full max-w-7xl pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-purple-600/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-64 h-64 bg-blue-600/10 rounded-full blur-3xl" />
      </div>

      <div className="max-w-6xl mx-auto px-6 relative z-10">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
            Up and Running in <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400">Minutes</span>
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto text-lg">
            We've simplified the complex. Get enterprise-grade AI voice agents without the enterprise-grade headache.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps.map((step, index) => (
            <motion.div
              key={step.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.2, duration: 0.5 }}
              className="relative group"
            >
              <div className="absolute inset-0 bg-gradient-to-b from-white/5 to-transparent rounded-2xl -z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <div className="bg-white/5 border border-white/10 p-8 rounded-2xl h-full backdrop-blur-sm hover:border-white/20 transition-colors">
                <div className="w-16 h-16 bg-gradient-to-br from-purple-500/20 to-blue-500/20 rounded-xl flex items-center justify-center text-3xl text-white mb-6 group-hover:scale-110 transition-transform duration-300">
                  {step.icon}
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">{step.title}</h3>
                <p className="text-gray-400 leading-relaxed">{step.description}</p>
              </div>
              
              {/* Connector Line (Desktop only) */}
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-1/2 -right-4 w-8 h-[2px] bg-gradient-to-r from-white/20 to-transparent transform -translate-y-1/2 z-0" />
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
