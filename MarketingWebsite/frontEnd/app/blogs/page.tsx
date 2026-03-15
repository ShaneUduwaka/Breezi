import Navbar from "../components/Navbar";
import CTA from "../components/CTA";
import Footer from "../components/Footer";

// Extracted Components
import BlogHero from "../components/blog/BlogHero";
import FeaturedArticle from "../components/blog/FeaturedArticle";
import CategoryNav from "../components/blog/CategoryNav";
import BlogGrid from "../components/blog/BlogGrid";
import BlogSidebar from "../components/blog/BlogSidebar";
import NewsletterCapture from "../components/blog/NewsletterCapture";

export default function BlogPage() {
  return (
    <div className="min-h-screen bg-[#050509] text-white font-sans selection:bg-purple-500/30">
      <Navbar />

      <main className="relative pt-32 pb-16 px-6 lg:px-16 max-w-7xl mx-auto">
        <BlogHero />
        <FeaturedArticle />
        <CategoryNav />

        <div className="flex flex-col lg:flex-row gap-12">
            <BlogGrid />
            <BlogSidebar />
        </div>

        <NewsletterCapture />
      </main>

      <CTA />
      <Footer />
    </div>
  );
}