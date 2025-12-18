import Link from 'next/link';
import ContactForm from '../components/ContactForm';
import { FaCheckCircle } from 'react-icons/fa';

export default function Contact() {
  return (
    <div className="min-h-screen flex flex-col lg:flex-row font-sans selection:bg-purple-500/30 relative">
      
      {/* Left Panel - Value Prop (Dark) */}
      <div className="lg:w-1/2 bg-[#050509] p-8 md:p-16 flex flex-col relative overflow-hidden text-white">
        
        {/* Logo Centered in Left Panel */}
        <Link href="/" className="absolute top-8 left-1/2 -translate-x-1/2 z-50 text-white">
            <h1 className="text-xl font-bold tracking-tight">
              Breezi
            </h1>
        </Link>
        
        <div className="relative z-10 flex-1 flex flex-col justify-center max-w-lg">
          <h2 className="text-4xl md:text-5xl font-bold mb-6 tracking-tight leading-tight">
            Talk to our sales team
          </h2>
          
          <p className="text-lg text-gray-400 mb-12 leading-relaxed">
            Need help with a large-scale deployment? We can design a custom plan for your business.
          </p>

          <div className="space-y-6">
            <div className="flex items-center gap-4">
              <FaCheckCircle className="text-white text-xl shrink-0" />
              <span className="text-lg font-medium">Custom volume pricing & discounts</span>
            </div>

            <div className="flex items-center gap-4">
              <FaCheckCircle className="text-white text-xl shrink-0" />
              <span className="text-lg font-medium">Enterprise-grade security & SLAs</span>
            </div>

            <div className="flex items-center gap-4">
              <FaCheckCircle className="text-white text-xl shrink-0" />
              <span className="text-lg font-medium">Dedicated success manager</span>
            </div>

            <div className="flex items-center gap-4">
              <FaCheckCircle className="text-white text-xl shrink-0" />
              <span className="text-lg font-medium">Priority 24/7 support access</span>
            </div>
          </div>
        </div>

        {/* Decorative subtle element at bottom instead of logos */}
        <div className="relative z-10 text-sm text-gray-600 mt-12 md:mt-0">
            © 2024 Breezi AI Inc.
        </div>
      </div>

      {/* Right Panel - Form (White) */}
      <div className="lg:w-1/2 bg-white flex items-center justify-center p-8 md:p-24">
        <div className="w-full max-w-md">
            <div className="mb-10 text-center md:text-left">
                <h3 className="text-3xl font-bold text-gray-900 mb-2">Get in touch</h3>
                <p className="text-gray-500">Fill out the form and we'll be in touch shortly.</p>
            </div>
            <ContactForm />
        </div>
      </div>

    </div>
  );
}
