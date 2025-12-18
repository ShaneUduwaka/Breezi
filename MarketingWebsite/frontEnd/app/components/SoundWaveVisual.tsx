"use client";

import { motion } from "framer-motion";

export default function SoundWaveVisual() {
  return (
    <div className="absolute inset-0 flex items-center justify-center">
      <div className="relative w-full max-w-md h-40">
        {/* main wave */}
        <motion.div
          aria-hidden
          initial={{ x: -30 }}
          animate={{ x: 30 }}
          transition={{ duration: 10, repeat: Infinity, repeatType: "reverse" }}
          className="absolute inset-x-[-10%] top-1/2 h-12 -translate-y-1/2 rounded-full bg-linear-to-r from-purple-500 via-teal-300 to-purple-500 opacity-60 blur-sm"
        />
        {/* secondary wave */}
        <motion.div
          aria-hidden
          initial={{ x: 30 }}
          animate={{ x: -30 }}
          transition={{ duration: 14, repeat: Infinity, repeatType: "reverse" }}
          className="absolute inset-x-[-15%] top-1/2 h-8 -translate-y-1/2 rounded-full bg-linear-to-r from-purple-400 via-blue-400 to-purple-400 opacity-40 blur-md rotate-2"
        />
        {/* subtle reflection */}
        <div className="absolute inset-x-0 top-[55%] h-10 bg-linear-to-t from-purple-500/30 via-transparent to-transparent blur-lg opacity-30" />
      </div>
    </div>
  );
}
