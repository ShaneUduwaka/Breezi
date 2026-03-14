"use client";

import { useState } from "react";
import { FaPaperPlane, FaUser, FaEnvelope, FaBuilding, FaCommentAlt, FaSpinner, FaCheck } from "react-icons/fa";

export default function ContactForm() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    company: "",
    message: ""
  });
  const [status, setStatus] = useState<"idle" | "loading" | "success">("idle");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Native validation handles the checks before this event fires
    setStatus("loading");

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));

    setStatus("successs");
    setFormData({ name: "", email: "", company: "", message: "" });

    // Reset status after delay
    setTimeout(() => {
      setStatus("idle");
    }, 3000);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 w-full max-w-md mx-auto">
      <div className="space-y-5">
        {/* Name */}
        <div className="space-y-1.5">
          <label className="text-xs font-bold text-gray-900 uppercase tracking-wider ml-1">Full Name</label>
          <div className="relative">
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:border-black focus:ring-1 focus:ring-black transition-all duration-200"
            />
          </div>
        </div>

        {/* Email */}
        <div className="space-y-1.5">
          <label className="text-xs font-bold text-gray-900 uppercase tracking-wider ml-1">Business Email</label>
          <div className="relative">
            <input
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:border-black focus:ring-1 focus:ring-black transition-all duration-200"
            />
          </div>
        </div>

        {/* Company */}
        <div className="space-y-1.5">
          <label className="text-xs font-bold text-gray-900 uppercase tracking-wider ml-1">Company</label>
          <div className="relative">
            <input
              type="text"
              value={formData.company}
              onChange={(e) => setFormData({ ...formData, company: e.target.value })}
              className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:border-black focus:ring-1 focus:ring-black transition-all duration-200"
            />
          </div>
        </div>

        {/* Message */}
        <div className="space-y-1.5">
          <label className="text-xs font-bold text-gray-900 uppercase tracking-wider ml-1">Message</label>
          <div className="relative">
            <textarea
              rows={4}
              required
              value={formData.message}
              onChange={(e) => setFormData({ ...formData, message: e.target.value })}
              className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:border-black focus:ring-1 focus:ring-black transition-all duration-200 resize-none"
            />
          </div>
        </div>
      </div>

      <button
        type="submit"
        disabled={status !== "idle"}
        className={`w-full py-4 font-bold rounded-full shadow-lg flex items-center justify-center gap-2 uppercase tracking-wide text-sm transition-all duration-200 
          bg-black text-white
          ${status === "success" ? "cursor-default" : "hover:opacity-75 hover:-translate-y-0.5 disabled:opacity-80 disabled:cursor-wait"}
        `}
      >
        {status === "success" ? "Sent" : "Send Message"}
      </button>
    </form>
  );
}
