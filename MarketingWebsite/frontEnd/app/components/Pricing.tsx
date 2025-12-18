"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  FaRobot,
  FaInfinity,
  FaMicrophone,
  FaHandshake,
  FaChartBar,
  FaShieldAlt,
} from "react-icons/fa";

export default function Pricing() {
  return (
    <section
      id="pricing"
      className="py-24 bg-[#050509] relative border-t border-white/5"
    >
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-6">
          <div className="max-w-2xl">
            <h2 className="text-3xl md:text-5xl font-bold text-white mb-6 tracking-tight">
              One Simple,{" "}
              <span className="text-purple-400">All-Inclusive Plan</span>
            </h2>
            <p className="text-gray-400 text-lg leading-relaxed">
              Experience the full power of Breezi without limits. We've
              simplified our pricing to give you everything you need to scale.
            </p>
          </div>
          <div>
            <Link href="/contact">
              <button className="px-6 py-3 bg-white text-black font-semibold rounded-full hover:bg-gray-200 transition-colors duration-300">
                Get Started
              </button>
            </Link>
          </div>
        </div>

        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={{
            visible: { transition: { staggerChildren: 0.1 } },
          }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5"
        >
          {/* Feature 1 */}
          <motion.div
            variants={{
              hidden: { opacity: 0, y: 20 },
              visible: { opacity: 1, y: 0 },
            }}
            className="group p-6 rounded-2xl bg-white/2 border border-white/5 hover:border-white/10 transition-colors duration-300"
          >
            <div className="w-12 h-12 rounded-xl bg-purple-500/10 flex items-center justify-center mb-5 group-hover:bg-purple-500/20 transition-colors">
              <FaRobot className="text-purple-400 text-xl" />
            </div>
            <h3 className="text-lg font-bold text-white mb-2">
              Unlimited Agents
            </h3>
            <p className="text-gray-400 text-sm leading-relaxed">
              Deploy as many AI voice agents as you need to handle simultaneous
              calls without any concurrent limits.
            </p>
          </motion.div>

          {/* Feature 2 */}
          <motion.div
            variants={{
              hidden: { opacity: 0, y: 20 },
              visible: { opacity: 1, y: 0 },
            }}
            className="group p-6 rounded-2xl bg-white/2 border border-white/5 hover:border-white/10 transition-colors duration-300"
          >
            <div className="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center mb-5 group-hover:bg-blue-500/20 transition-colors">
              <FaInfinity className="text-blue-400 text-xl" />
            </div>
            <h3 className="text-lg font-bold text-white mb-2">
              Unlimited Minutes
            </h3>
            <p className="text-gray-400 text-sm leading-relaxed">
              No metering or overage fees. Talk as much as your business
              requires with a flat, predictable rate.
            </p>
          </motion.div>

          {/* Feature 3 */}
          <motion.div
            variants={{
              hidden: { opacity: 0, y: 20 },
              visible: { opacity: 1, y: 0 },
            }}
            className="group p-6 rounded-2xl bg-white/2 border border-white/5 hover:border-white/10 transition-colors duration-300"
          >
            <div className="w-12 h-12 rounded-xl bg-green-500/10 flex items-center justify-center mb-5 group-hover:bg-green-500/20 transition-colors">
              <FaMicrophone className="text-green-400 text-xl" />
            </div>
            <h3 className="text-lg font-bold text-white mb-2">
              Custom Voice Cloning
            </h3>
            <p className="text-gray-400 text-sm leading-relaxed">
              Clone your own voice or create a unique brand persona that
              represents your company perfectly.
            </p>
          </motion.div>

          {/* Feature 4 */}
          <motion.div
            variants={{
              hidden: { opacity: 0, y: 20 },
              visible: { opacity: 1, y: 0 },
            }}
            className="group p-6 rounded-2xl bg-white/2 border border-white/5 hover:border-white/10 transition-colors duration-300"
          >
            <div className="w-12 h-12 rounded-xl bg-orange-500/10 flex items-center justify-center mb-5 group-hover:bg-orange-500/20 transition-colors">
              <FaHandshake className="text-orange-400 text-xl" />
            </div>
            <h3 className="text-lg font-bold text-white mb-2">
              CRM Integration
            </h3>
            <p className="text-gray-400 text-sm leading-relaxed">
              Seamlessly syncs with Salesforce, HubSpot, and Zoho to keep your
              customer records always up to date.
            </p>
          </motion.div>

          {/* Feature 5 */}
          <motion.div
            variants={{
              hidden: { opacity: 0, y: 20 },
              visible: { opacity: 1, y: 0 },
            }}
            className="group p-6 rounded-2xl bg-white/2 border border-white/5 hover:border-white/10 transition-colors duration-300"
          >
            <div className="w-12 h-12 rounded-xl bg-pink-500/10 flex items-center justify-center mb-5 group-hover:bg-pink-500/20 transition-colors">
              <FaChartBar className="text-pink-400 text-xl" />
            </div>
            <h3 className="text-lg font-bold text-white mb-2">
              Real-time Insights
            </h3>
            <p className="text-gray-400 text-sm leading-relaxed">
              Get deep insights into call sentiment, resolution rates, and agent
              performance with our dashboard.
            </p>
          </motion.div>

          {/* Feature 6 */}
          <motion.div
            variants={{
              hidden: { opacity: 0, y: 20 },
              visible: { opacity: 1, y: 0 },
            }}
            className="group p-6 rounded-2xl bg-white/2 border border-white/5 hover:border-white/10 transition-colors duration-300"
          >
            <div className="w-12 h-12 rounded-xl bg-teal-500/10 flex items-center justify-center mb-5 group-hover:bg-teal-500/20 transition-colors">
              <FaShieldAlt className="text-teal-400 text-xl" />
            </div>
            <h3 className="text-lg font-bold text-white mb-2">
              99.9% Uptime SLA
            </h3>
            <p className="text-gray-400 text-sm leading-relaxed">
              Enterprise-grade reliability with financially backed service level
              agreements for peace of mind.
            </p>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
