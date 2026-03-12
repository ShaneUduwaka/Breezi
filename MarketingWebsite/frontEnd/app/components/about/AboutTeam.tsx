import { FaLinkedin } from 'react-icons/fa';

export default function AboutTeam() {
  return (
    <section>
      <div className="text-center mb-16">
        <h2 className="text-3xl md:text-4xl font-semibold">Meet the Team</h2>
        <p className="text-gray-400 mt-4 text-lg max-w-2xl mx-auto">
          The builders behind Breezi. We combine deep expertise in artificial intelligence with a passion for human-centric design.
        </p>
      </div>

      {/* Team Grid: 3 on top, 2 centered on bottom on large screens */}
      <div className="flex flex-wrap justify-center gap-8 max-w-6xl mx-auto">
        <div className="w-full md:w-[calc(50%-1rem)] lg:w-[calc(33.333%-1.5rem)]">
          <TeamMemberCard
            name="Tevin Bandara"
            role="CEO & Co-Founder"
            bio="Former AI research lead with a vision to make enterprise-grade voice agents accessible to businesses of all sizes."
            linkedin="https://linkedin.com"
          />
        </div>
        <div className="w-full md:w-[calc(50%-1rem)] lg:w-[calc(33.333%-1.5rem)]">
          <TeamMemberCard
            name="Sanithya Mahavithange"
            role="CTO & Co-Founder"
            bio="Scaling infrastructure expert. Spent 10 years building high-availability real-time communication systems."
            linkedin="https://linkedin.com"
          />
        </div>
        <div className="w-full md:w-[calc(50%-1rem)] lg:w-[calc(33.333%-1.5rem)]">
          <TeamMemberCard
            name="Kaveetha Cooray"
            role="Head of Product"
            bio="Obsessed with user experience and conversational design. Ensures every Breezi interaction feels incredibly natural."
            linkedin="https://linkedin.com"
          />
        </div>
        <div className="w-full md:w-[calc(50%-1rem)] lg:w-[calc(33.333%-1.5rem)]">
          <TeamMemberCard
            name="Shane Uduwaka"
            role="VP of Sales"
            bio="Veteran sales leader passionate about showing enterprises the ROI of AI-driven voice solutions."
            linkedin="https://linkedin.com"
          />
        </div>
        <div className="w-full md:w-[calc(50%-1rem)] lg:w-[calc(33.333%-1.5rem)]">
          <TeamMemberCard
            name="Naveen Harry"
            role="Lead AI Engineer"
            bio="Specialist in low-latency LLMs and natural language processing. Makes our agents sound perfectly human."
            linkedin="https://linkedin.com"
          />
        </div>
      </div>
    </section>
  );
}

// Props component for team members
function TeamMemberCard({ name, role, bio, linkedin, imageUrl }: { name: string, role: string, bio: string, linkedin?: string, imageUrl?: string }) {
  return (
    <div className="bg-[#0A0A1F] border border-white/5 rounded-3xl p-6 hover:bg-[#10102E] hover:border-white/10 transition-all duration-300 flex flex-col items-center text-center group h-full">

      {/* Profile Image (Using a placeholder gradient if none provided) */}
      <div className="w-40 h-40 rounded-full mb-6 relative overflow-hidden bg-gradient-to-tr from-purple-800 to-indigo-900 border-2 border-purple-500/30 group-hover:border-purple-500/60 transition-colors">
        {imageUrl ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={imageUrl} alt={name} className="object-cover w-full h-full" />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-2xl font-bold text-white/50">
            {name.charAt(0)}
          </div>
        )}
      </div>

      <h3 className="text-xl font-bold text-white mb-1">{name}</h3>
      <p className="text-purple-400 font-medium text-sm mb-4">{role}</p>

      <p className="text-gray-400 text-sm leading-relaxed mb-6 flex-1">
        {bio}
      </p>

      {linkedin && (
        <a href={linkedin} target="_blank" rel="noopener noreferrer" className="text-gray-500 hover:text-white transition-colors mt-auto">
          <FaLinkedin size={24} />
        </a>
      )}
    </div>
  );
}