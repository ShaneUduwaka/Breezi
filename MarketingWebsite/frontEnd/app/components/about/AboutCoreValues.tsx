import { FaRocket, FaHandshake, FaHeart, FaLightbulb } from 'react-icons/fa';

export default function AboutCoreValues() {
  return (
    <section>
      <div className="text-center mb-16">
        <h2 className="text-3xl md:text-4xl font-semibold">Core Values</h2>
        <p className="text-gray-400 mt-4 text-lg">The principles that guide our technology and our team.</p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
        <ValueCard
          icon={<FaLightbulb />}
          title="Innovation"
          description="We constantly push the boundaries of conversational AI to create seamless, natural interactions."
        />
        <ValueCard
          icon={<FaHandshake />}
          title="Reliability"
          description="Enterprise-grade stability you can trust. No sick days, no dropped calls, always online."
        />
        <ValueCard
          icon={<FaHeart />}
          title="Empathy in AI"
          description="Technology should understand context and tone. Our agents are designed to handle calls with care."
        />
        <ValueCard
          icon={<FaRocket />}
          title="Scalability"
          description="Built to handle massive surges in call volume instantly without breaking a sweat."
        />
      </div>
    </section>
  );
}

// Props component for values
function ValueCard({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) {
  return (
    <div className="bg-[#0A0A1F] border border-white/5 rounded-3xl p-8 hover:bg-[#10102E] hover:border-white/10 transition-all duration-300 group">
      <div className="text-purple-400 text-3xl mb-6 bg-purple-500/10 w-16 h-16 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300 group-hover:bg-purple-500/20 group-hover:text-purple-300">
        {icon}
      </div>
      <h3 className="text-xl font-bold mb-3">{title}</h3>
      <p className="text-gray-400 leading-relaxed text-sm lg:text-base">
        {description}
      </p>
    </div>
  );
}
