"use client";

import { motion } from "framer-motion";
import { FaCheck } from "react-icons/fa";

const plans = [
  {
    name: "Starter",
    price: "$49",
    period: "/mo",
    description: "Perfect for small businesses just getting started.",
    features: [
      "1 AI Voice Agent",
      "500 Minutes/month",
      "Standard English Voice",
      "Email Support",
      "Basic Analytics"
    ],
    cta: "Start Free Trial",
    popular: false,
  },
  {
    name: "Pro",
    price: "$149",
    period: "/mo",
    description: "For growing teams that need more power and flexibility.",
    features: [
      "3 AI Voice Agents",
      "2,000 Minutes/month",
      "Multilingual (Sinhala & English)",
      "Priority Support",
      "Advanced Analytics",
      "CRM Integration"
    ],
    cta: "Get Started",
    popular: true,
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "",
    description: "Full-scale solutions for large organizations.",
    features: [
      "Unlimited Agents",
      "Unlimited Minutes",
      "Custom Voice Cloning",
      "Dedicated Account Manager",
      "On-premise Deployment",
      "SLA Guarantee"
    ],
    cta: "Contact Sales",
    popular: false,
  },
];

export default function Pricing() {
  return (
    <section id="pricing" className="py-24 bg-[#050509] relative">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
            Simple, Transparent <span className="text-purple-400">Pricing</span>
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Choose the plan that fits your business needs. No hidden fees.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-center">
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1, duration: 0.5 }}
              className={`relative p-8 rounded-2xl border ${
                plan.popular 
                  ? "bg-white/10 border-purple-500 shadow-[0_0_30px_rgba(168,85,247,0.15)]" 
                  : "bg-white/5 border-white/10"
              } backdrop-blur-sm flex flex-col h-full`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-purple-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">
                  Most Popular
                </div>
              )}

              <div className="mb-8">
                <h3 className="text-xl font-semibold text-white mb-2">{plan.name}</h3>
                <div className="flex items-baseline gap-1">
                  <span className="text-4xl font-bold text-white">{plan.price}</span>
                  <span className="text-gray-400">{plan.period}</span>
                </div>
                <p className="text-gray-400 text-sm mt-4">{plan.description}</p>
              </div>

              <ul className="space-y-4 mb-8 flex-1">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start gap-3 text-gray-300 text-sm">
                    <FaCheck className="text-green-400 mt-1 shrink-0" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>

              <button 
                className={`w-full py-3 rounded-lg font-medium transition-all duration-300 ${
                  plan.popular
                    ? "bg-purple-600 hover:bg-purple-700 text-white shadow-lg shadow-purple-600/25"
                    : "bg-white/10 hover:bg-white/20 text-white"
                }`}
              >
                {plan.cta}
              </button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
