export default function AboutMission() {
  return (
    <section className="relative">
      {/* Subtle background glow */}
      <div className="absolute inset-0 bg-purple-900/10 blur-[100px] rounded-full -z-10 w-3/4 mx-auto hidden md:block" />
      
      <div className="bg-[#0A0A1F]/80 border border-white/5 rounded-3xl p-10 md:p-16 text-center shadow-max backdrop-blur-sm">
        <h2 className="text-3xl md:text-4xl font-semibold mb-6">Our Mission</h2>
        <p className="text-lg md:text-xl text-gray-300 leading-relaxed max-w-3xl mx-auto">
          At Breezi AI, our goal is to <strong>unburden your staff and elevate your service</strong>. 
          We believe that routine queries shouldn't consume valuable human hours. By deploying advanced AI Voice Agents, 
          we empower businesses to provide instant, scalable, and empathetic support 24/7—allowing human teams to focus on 
          complex problem-solving and meaningful relationship building.
        </p>
      </div>
    </section>
  );
}
