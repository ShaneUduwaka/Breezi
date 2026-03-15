export default function AboutRoadmap() {
  return (
    <section className="relative mt-32">
      <div className="text-center mb-16">
        <h2 className="text-3xl md:text-4xl font-semibold">Our Roadmap</h2>
        <p className="text-gray-400 mt-4 text-lg max-w-2xl mx-auto">
          We're building the future of customer interaction step by step. Here is where we are heading.
        </p>
      </div>

      <div className="max-w-4xl mx-auto relative">
        {/* Vertical Line */}
        <div className="absolute left-4 md:left-1/2 top-4 bottom-4 w-px bg-gradient-to-b from-purple-500/50 via-purple-500/20 to-transparent -translate-x-1/2" />

        <div className="space-y-12">
          <TimelineItem 
            date="May 2026"
            title="MVP Deployment: Food Franchises"
            description="Launching our core AI voice agent tailored for high-volume food franchises to handle orders, reservations, and FAQs."
            align="left"
          />
          <TimelineItem 
            date="Mid 2026"
            title="Multilingual Support Expansion"
            description="Rolling out broad language support, including native Tamil comprehension and speaking, to serve diverse demographics seamlessly."
            align="right"
          />
          <TimelineItem 
            date="Early 2027"
            title="Healthcare Integration"
            description="Expanding our models to handle HIPAA-compliant patient scheduling, basic triage, and appointment reminders."
            align="left"
          />
          <TimelineItem 
            date="Late 2027"
            title="Banking & Real Estate Sectors"
            description="Deploying specialized agents capable of property inquiries, basic financial support routing, and secure authentication flows."
            align="right"
          />
        </div>
      </div>
    </section>
  );
}

// Props component for timeline
function TimelineItem({ date, title, description, align }: { date: string, title: string, description: string, align: 'left' | 'right' }) {
  const isLeft = align === 'left';
  
  return (
    <div className={`relative flex items-center justify-between md:justify-normal w-full ${isLeft ? 'md:flex-row-reverse' : ''}`}>
      
      {/* Date Marker (Mobile) */}
      <div className="md:hidden absolute left-4 w-4 h-4 rounded-full bg-purple-500 border-[3px] border-[#050509] -translate-x-[7px] z-10 shadow-[0_0_15px_rgba(168,85,247,0.5)]" />

      {/* spacer for alternate layout on desktop */}
      <div className={`hidden md:block w-5/12 ${isLeft ? 'text-left pl-8' : 'text-right pr-8'}`}>
          <div className="text-purple-400 font-bold text-xl tracking-wider">{date}</div>
      </div>

      {/* Center dot for desktop */}
      <div className="hidden md:flex z-10 relative flex-col items-center justify-center w-2/12">
        <div className="w-5 h-5 rounded-full bg-purple-500 border-[4px] border-[#0A0A1F] shadow-[0_0_15px_rgba(168,85,247,0.5)] relative z-10" />
      </div>

      {/* Content Card */}
      <div className={`w-full pl-12 md:pl-0 md:w-5/12 ${isLeft ? 'md:pr-8 text-left md:text-right' : 'md:pl-8 text-left'}`}>
        <div className="bg-[#0A0A1F] border border-white/5 p-6 rounded-3xl hover:border-purple-500/30 transition-colors shadow-lg">
          {/* Mobile date */}
          <div className="md:hidden text-purple-400 font-bold text-sm tracking-wider mb-2">{date}</div>
          
          <h3 className="text-xl font-bold text-white mb-2">{title}</h3>
          <p className="text-gray-400 text-sm md:text-base leading-relaxed">
            {description}
          </p>
        </div>
      </div>
    </div>
  );
}