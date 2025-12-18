"use client";

import { motion } from "framer-motion";
import {
  FaHamburger,
  FaLandmark,
  FaUniversity,
  FaHospital,
  FaBuilding,
} from "react-icons/fa";

export default function Industries() {
  const industries = [
    {
      name: "Food Franchises",
      icon: <FaHamburger />,
      description:
        "Automate orders and reservations with voice AI that handles peak hours effortlessly.",
      image:
        "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80",
      className: "md:col-span-2",
    },
    {
      name: "Healthcare",
      icon: <FaHospital />,
      description:
        "Schedule appointments and triage patient calls with HIPAA-compliant AI agents.",
      image:
        "https://images.unsplash.com/photo-1538108149393-fbbd81895907?auto=format&fit=crop&w=800&q=80",
      className: "md:col-span-1",
    },
    {
      name: "Government",
      icon: <FaLandmark />,
      description:
        "Provide 24/7 citizen support and streamline public inquiry handling.",
      image: "/frontEnd/public/images/samuel-schroth-hyPt63Df3Dw-unsplash.jpg",
      className: "md:col-span-1",
    },
    {
      name: "Banks",
      icon: <FaUniversity />,
      description:
        "Secure, authenticated voice banking for balance checks and transfers.",
      image: "/images/samuel-schroth-hyPt63Df3Dw-unsplash.jpg",
      className: "md:col-span-1",
    },
    {
      name: "Real Estate",
      icon: <FaBuilding />,
      description:
        "Qualify leads and schedule property viewings automatically.",
      image:
        "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=800&q=80",
      className: "md:col-span-1",
    },
  ];

  return (
    <section className="py-24 bg-[#050509] relative" id="industries">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
            Built for{" "}
            <span className="text-blue-400">High-Trust Industries</span>
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto text-lg">
            Empowering sectors where accuracy, security, and reliability are
            non-negotiable.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {industries.map((industry, index) => (
            <motion.div
              key={industry.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1, duration: 0.5 }}
              className={`relative overflow-hidden rounded-3xl border border-white/10 group h-80 ${industry.className}`}
            >
              {/* Background Image */}
              <div
                className="absolute inset-0 bg-cover bg-center transition-transform duration-700 group-hover:scale-110"
                style={{ backgroundImage: `url(${industry.image})` }}
              />

              {/* Gradient Overlay */}
              <div className="absolute inset-0 bg-linear-to-t from-black/90 via-black/50 to-transparent opacity-80 group-hover:opacity-90 transition-opacity duration-300" />

              {/* Content */}
              <div className="relative z-10 h-full flex flex-col justify-end p-8">
                <div className="w-12 h-12 bg-white/10 backdrop-blur-md rounded-xl flex items-center justify-center text-xl text-white mb-4 group-hover:bg-blue-500/20 group-hover:text-blue-400 transition-colors duration-300">
                  {industry.icon}
                </div>
                <h3 className="text-2xl font-bold text-white mb-2">
                  {industry.name}
                </h3>
                <p className="text-gray-300 text-sm leading-relaxed opacity-0 transform translate-y-4 group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-300 delay-75">
                  {industry.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
