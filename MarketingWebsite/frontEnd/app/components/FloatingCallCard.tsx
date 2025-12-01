"use client";

import { motion } from "framer-motion";

export default function FloatingCallCard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4, duration: 0.6 }}
      className="absolute right-2 top-4 w-60 rounded-2xl border border-white/10 bg-white/5 p-4 text-xs text-white/80 backdrop-blur-xl shadow-[0_18px_60px_rgba(0,0,0,0.7)]"
    >
      <div className="flex items-center justify-between mb-2">
        <span className="text-[11px] text-white/60">Live Call</span>
        <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
      </div>
      <p className="text-sm font-medium mb-1">+94 77 321 7654</p>
      <p className="text-[11px] text-white/60 mb-3">New lead · Colombo · Sinhala</p>
      <div className="flex flex-wrap gap-2">
        <span className="rounded-full bg-emerald-400/15 px-2 py-1 text-[10px] text-emerald-300 border border-emerald-400/40">
          Lead Qualified
        </span>
        <span className="rounded-full bg-[#F75C03]/10 px-2 py-1 text-[10px] text-[#F75C03] border border-[#F75C03]/40">
          Appointment Booked
        </span>
      </div>
    </motion.div>
  );
}
