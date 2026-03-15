export default function CategoryNav() {
  const categories = ["All", "AI Agents", "Call Automation", "Customer Experience", "Case Studies", "Guides"];

  return (
    <section className="mb-10 flex overflow-x-auto pb-4 scrollbar-hide border-b border-white/10">
      <div className="flex gap-2 mx-auto md:mx-0">
          {categories.map((cat, i) => (
              <button 
                  key={cat} 
                  className={`px-5 py-2 rounded-full whitespace-nowrap text-sm font-medium transition duration-300 ${
                      i === 0 
                      ? "bg-purple-600 text-white" 
                      : "bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white border border-white/5"
                  }`}
              >
                  {cat}
              </button>
          ))}
      </div>
    </section>
  );
}
