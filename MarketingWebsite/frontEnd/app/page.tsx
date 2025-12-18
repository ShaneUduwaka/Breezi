import Hero from './components/Hero';
import Navbar from './components/Navbar';
import Features from './components/Features';
import HowItWorks from './components/HowItWorks';
import Industries from './components/Industries';
import Pricing from './components/Pricing';
import FAQ from './components/FAQ';
import CTA from './components/CTA';
import Footer from './components/Footer';

export default function Home() {
  return (
    <div className="min-h-screen bg-[#050509] text-white font-sans selection:bg-purple-500/30">
      <Navbar />
      <main className="relative overflow-hidden">
        <Hero />
        <Features />
        <HowItWorks />
        <Industries />
        <Pricing />
        <FAQ />
        <CTA />
      </main>
      <Footer />
    </div>
  );
}