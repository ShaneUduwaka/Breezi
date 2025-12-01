import React from 'react';
import Link from 'next/link';

export default function Hero() {
  return (
    <section className="relative h-[90vh] flex items-center justify-center text-center overflow-hidden">
      {/* Background Gradient Effect */}
      <div
        className="absolute inset-0 z-0 opacity-40"
        style={{
          background: 'linear-gradient(135deg, #6B47ED 0%, #AD6FFB 50%, #4FA2EB 100%)',
          filter: 'blur(150px)', // Creates a soft, glowing effect
          transform: 'scale(1.5)' // Make sure the blur covers the edges
        }}
      ></div>
      {/* Content */}
      <div className="relative z-10 max-w-4xl mx-auto px-4">
        <p className="text-breezi-blue text-sm uppercase tracking-widest mb-4">
          New Updates v2 Out Now! {/* Example of a small announcement from your inspiration */}
        </p>
        <h1 className="text-white text-4xl md:text-6xl lg:text-7xl font-poppins font-bold leading-tight mb-6">
          Eliminate Staff Burnout. <br /> Deliver 24/7 Exceptional Service.
        </h1>
        <p className="text-gray-300 text-lg md:text-xl max-w-3xl mx-auto mb-10">
          Breezi is your advanced AI Call Agent, designed to handle high call volumes, provide
          consistent support, and free your human teams to focus on what matters most.
          Experience the future of customer interaction.
        </p>
        <div className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-6">
          <Link href="#request-demo">
            <button className="px-8 py-3 bg-gradient-hero text-white font-poppins font-semibold rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
              Request a Demo
            </button>
          </Link>
          <Link href="#how-it-works">
            <button className="px-8 py-3 border border-gray-500 text-gray-200 font-poppins font-semibold rounded-full hover:border-white hover:text-white transition-all duration-300">
              See How It Works
            </button>
          </Link>
        </div>
      </div>
    </section>
  );
}