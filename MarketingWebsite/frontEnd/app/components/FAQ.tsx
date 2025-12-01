"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FaPlus, FaMinus } from "react-icons/fa";

const faqs = [
  {
    question: "Do I need to change my phone number?",
    answer: "No. You can forward calls from your existing number to Breezi, or we can provide you with a new number. The choice is yours.",
  },
  {
    question: "How does the Sinhala voice support work?",
    answer: "Our AI models are trained on thousands of hours of native Sinhala speech, allowing them to understand dialects, slang, and context with near-human accuracy.",
  },
  {
    question: "Can I customize the agent's responses?",
    answer: "Absolutely. You can upload your own knowledge base, scripts, and guidelines. The AI will strictly adhere to your instructions while maintaining a natural conversation flow.",
  },
  {
    question: "What happens if the AI can't answer a question?",
    answer: "If the AI encounters a complex query it can't resolve, it will gracefully transfer the call to a human agent or take a message and notify your team immediately.",
  },
  {
    question: "Is my data secure?",
    answer: "Yes. We adhere to strict enterprise-grade security standards. All calls are encrypted, and we do not use your data to train public models without your explicit consent.",
  },
];

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section className="py-24 bg-[#050509]">
      <div className="max-w-3xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
            Frequently Asked <span className="text-blue-400">Questions</span>
          </h2>
        </div>

        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <div
              key={index}
              className="border border-white/10 rounded-lg bg-white/5 overflow-hidden"
            >
              <button
                onClick={() => setOpenIndex(openIndex === index ? null : index)}
                className="w-full px-6 py-4 flex items-center justify-between text-left text-white hover:bg-white/5 transition-colors"
              >
                <span className="font-medium text-lg pr-8">{faq.question}</span>
                <span className="text-blue-400 shrink-0">
                  {openIndex === index ? <FaMinus /> : <FaPlus />}
                </span>
              </button>
              <AnimatePresence>
                {openIndex === index && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <div className="px-6 pb-6 pt-2 text-gray-400 leading-relaxed border-t border-white/5">
                      {faq.answer}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
