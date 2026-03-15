"use client";

import Link from "next/link";
import { useState, useEffect } from "react";

const navLinks = [
  { label: "Features", href: "/#features" },
  { label: "How it Works", href: "/#how-it-works" },
  { label: "Plan", href: "/#pricing" },
  { label: "About Us", href: "/about" },
  { label: "Blog", href: "/blogs" },
  { label: "Contact", href: "/contact" },
];

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 inset-x-0 z-50 flex justify-center transition-all duration-300 ${
        scrolled ? "py-2" : "py-4"
      }`}
    >
      <nav
        className={`w-[92%] max-w-5xl rounded-full border border-white/10 bg-white/5 px-6 py-3 backdrop-blur-xl flex items-center justify-between transition-all duration-300 ${
          scrolled ? "bg-[#050509]/80 shadow-lg shadow-purple-500/10" : ""
        }`}
      >
        {/* LOGO */}
        <Link href="/" className="font-bold text-xl tracking-tight text-white">
          Breezi
        </Link>

        {/* LINKS */}
        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-white/70">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="hover:text-white transition-colors"
            >
              {link.label}
            </Link>
          ))}
        </div>

        {/* ACTIONS */}
        <div className="flex items-center gap-4">
          {/**/}
          <Link href="/contact">
            <button className="bg-white text-black text-sm font-bold px-5 py-2 rounded-full hover:bg-gray-200 transition-colors">
              Get Started
            </button>
          </Link>
        </div>
      </nav>
    </header>
  );
}
