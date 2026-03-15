import Link from 'next/link';

export default function AboutStory() {
  return (
    <section className="grid lg:grid-cols-2 gap-16 items-center">
      <div className="order-2 lg:order-1 relative h-64 md:h-96 rounded-3xl overflow-hidden bg-gradient-to-br from-[#10102E] to-[#0A0A1F] border border-white/10 flex items-center justify-center group">
        {/* Abstract Visual Representation */}
        <div className="absolute w-full h-full opacity-30 mix-blend-screen bg-[url('/soundwave-bg.svg')] bg-cover bg-center transition-transform duration-700 group-hover:scale-105" />
        <div className="w-32 h-32 rounded-full border border-purple-500/30 flex items-center justify-center animate-pulse shadow-[0_0_50px_rgba(168,85,247,0.2)]">
          <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-purple-600 to-blue-500 opacity-80 blur-md" />
        </div>
      </div>

      <div className="order-1 lg:order-2 space-y-6">
        <h2 className="text-3xl md:text-4xl font-semibold">Why We Built Breezi</h2>
        <div className="space-y-4 text-gray-300 text-lg leading-relaxed">
          <p>
            We saw a recurring problem across industries: overwhelmed support teams, long hold times, and frustrated customers. Traditional IVR systems (press 1 for sales, 2 for support) were impersonal and clunky.
          </p>
          <p>
            We envisioned a future where calling a business feels exactly like talking to your smartest, most helpful team member—instantly available.
          </p>
          <p>
            Breezi was built to bridge the gap between artificial efficiency and human-like interaction. By combining cutting-edge LLMs with low-latency voice models, we created an agent that doesn't just listen, but understands and resolves.
          </p>
        </div>
        <div className="pt-6">
          <Link href="/contact" className="inline-block bg-white text-black font-semibold px-8 py-3 rounded-full hover:bg-gray-200 transition-colors shadow-[0_0_20px_rgba(255,255,255,0.3)]">
            Let's Talk
          </Link>
        </div>
      </div>
    </section>
  );
}