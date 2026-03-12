import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

// Refactored Sections
import AboutHero from '../components/about/AboutHero';
import AboutMission from '../components/about/AboutMission';
import AboutCoreValues from '../components/about/AboutCoreValues';

export const metadata = {
  title: 'About Us | Breezi AI',
  description: 'Learn about Breezi AI, our mission, core values, and the story behind our advanced AI call agents.',
};

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-[#050509] text-white font-sans selection:bg-purple-500/30 flex flex-col">
      <Navbar />

      <main className="flex-1 pt-32 pb-20 px-6 sm:px-8 lg:px-12 w-full max-w-7xl mx-auto space-y-32">
        <AboutHero />
        <AboutMission />
        <AboutCoreValues />
      </main>

      <Footer />
    </div>
  );
}
