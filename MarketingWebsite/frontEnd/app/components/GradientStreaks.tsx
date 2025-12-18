"use client";

import { motion } from "framer-motion";

export default function GradientStreaks() {
  return (
    <>
      {/* Top streak */}
      <motion.div
        aria-hidden
        initial={{ x: -100 }}
        animate={{ x: 100 }}
        transition={{ duration: 18, repeat: Infinity, repeatType: "reverse" }}
        className="pointer-events-none absolute -top-40 left-0 h-72 w-full bg-linear-to-r from-purple-500/0 via-purple-500/40 to-teal-300/0 blur-3xl"
      />
      {/* Bottom streak */}
      <motion.div
        aria-hidden
        initial={{ x: 100 }}
        animate={{ x: -100 }}
        transition={{ duration: 22, repeat: Infinity, repeatType: "reverse" }}
        className="pointer-events-none absolute -bottom-32 right-[-10%] h-64 w-[70%] bg-linear-to-r from-teal-400/0 via-teal-400/40 to-purple-500/0 blur-3xl"
      />
    </>
  );
}
