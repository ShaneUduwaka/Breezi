"use client";

import React from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import SoundWaveVisual from "./SoundWaveVisual";

export default function Hero() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.8,
        ease: "easeOut" as any,
      },
    },
  };

  return (
    <section className="relative h-[90vh] flex items-center justify-center text-center overflow-hidden bg-[#020205]">
      {/* Moving Grid Background */}
      <div
        className="absolute inset-0 z-0 opacity-[0.05] pointer-events-none"
        style={{
          backgroundImage: `linear-gradient(to right, #4f46e5 1px, transparent 1px), linear-gradient(to bottom, #4f46e5 1px, transparent 1px)`,
          backgroundSize: "60px 60px",
          maskImage: "radial-gradient(circle, black, transparent 80%)",
        }}
      >
        <motion.div
          animate={{
            x: [0, -60],
            y: [0, -60],
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: "linear",
          }}
          className="absolute -inset-full z-0"
          style={{
            backgroundImage: `inherit`,
            backgroundSize: "inherit",
          }}
        />
      </div>

      {/* Dynamic Background Blobs */}
      <div className="absolute inset-0 z-1 pointer-events-none overflow-hidden">
        <motion.div
          animate={{
            scale: [1, 1.1, 1],
            x: [0, 30, 0],
            y: [0, 20, 0],
          }}
          transition={{
            duration: 15,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="absolute top-[-20%] left-[-10%] w-[70%] h-[70%] rounded-full bg-purple-600/10 blur-[130px]"
        />
        <motion.div
          animate={{
            scale: [1.1, 1, 1.1],
            x: [0, -30, 0],
            y: [0, -15, 0],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="absolute bottom-[-20%] right-[-10%] w-[60%] h-[60%] rounded-full bg-blue-600/10 blur-[130px]"
        />
      </div>

      {/* Floating Particles Field */}
      <div className="absolute inset-0 z-2 pointer-events-none">
        {[...Array(50)].map((_, i) => (
          <motion.div
            key={i}
            initial={{
              x: Math.random() * 100 + "%",
              y: Math.random() * 100 + "%",
              opacity: Math.random() * 0.5 + 0.1,
              scale: Math.random() * 0.5 + 0.5,
            }}
            animate={{
              y: [0, -40, 0],
              x: [0, Math.random() * 20 - 10, 0],
              opacity: [0.1, 0.4, 0.1],
            }}
            transition={{
              duration: Math.random() * 10 + 10,
              repeat: Infinity,
              ease: "easeInOut",
              delay: Math.random() * 5,
            }}
            className="absolute w-1 h-1 bg-white rounded-full blur-[1px]"
            style={{
              left: Math.random() * 100 + "%",
              top: Math.random() * 100 + "%",
            }}
          />
        ))}
      </div>

      {/* Visual Effects (SoundWave) */}
      <motion.div
        animate={{
          y: [-5, 5, -5],
          opacity: [0.3, 0.5, 0.3],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute inset-0 z-10 pointer-events-none opacity-40"
      >
        <SoundWaveVisual />
      </motion.div>

      {/* Content */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        className="relative z-10 max-w-4xl mx-auto px-4"
      >
        <motion.p
          variants={itemVariants}
          className="text-breezi-blue text-sm uppercase tracking-widest mb-4"
        ></motion.p>
        <motion.h1
          variants={itemVariants}
          className="text-white text-4xl md:text-6xl lg:text-7xl font-poppins font-bold leading-tight mb-6"
        >
          Eliminate Staff Burnout. <br /> Deliver 24/7 Exceptional Service.
        </motion.h1>
        <motion.p
          variants={itemVariants}
          className="text-gray-300 text-lg md:text-xl max-w-3xl mx-auto mb-10 leading-relaxed"
        >
          Breezi is your advanced AI Call Agent, designed to handle high call
          volumes, provide consistent support, and free your human teams to
          focus on what matters most.
        </motion.p>
        <motion.div
          variants={itemVariants}
          className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-6"
        >
          <Link href="#">
            <button className="px-8 py-3 bg-gradient-hero text-white font-poppins font-semibold rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
              Demo
            </button>
          </Link>
          <Link href="#how-it-works">
            <button className="px-8 py-3 border border-gray-500 text-gray-200 font-poppins font-semibold rounded-full hover:border-white hover:text-white transition-all duration-300">
              See How It Works
            </button>
          </Link>
        </motion.div>
      </motion.div>
    </section>
  );
}
