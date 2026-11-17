"use client";

import Link from "next/link";
import { Cpu, ShieldCheck } from "lucide-react";

export default function Footer() {
  return (
    <footer className="border-t border-emerald-100 bg-white text-slate-600 text-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
          {/* Brand info */}
          <div className="md:col-span-2 space-y-4">
            <Link href="/" className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white">
                <Cpu className="w-4 h-4" />
              </div>
              <span className="font-bold text-lg text-slate-900 tracking-tight">
                Resume<span className="text-emerald-600">IQ</span>
              </span>
            </Link>
            <p className="text-slate-600 max-w-md leading-relaxed text-sm">
              An open-access, deterministic ATS Resume Intelligence platform. Powered by custom Python agents,
              local semantic embeddings, BM25 keyword ranking, and explainable scoring models.
            </p>
            <div className="flex items-center gap-2 text-xs text-emerald-800 bg-emerald-50 border border-emerald-200 rounded-lg px-3 py-1.5 w-fit font-medium">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span>Zero-Storage Privacy: Resumes are processed anonymously and purged automatically.</span>
            </div>
          </div>

          {/* Product links */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-900">Platform</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/analyze" className="hover:text-emerald-700 transition-colors font-medium">
                  Resume & JD Upload
                </Link>
              </li>
              <li>
                <Link href="/#how-it-works" className="hover:text-emerald-700 transition-colors font-medium">
                  How ATS Scoring Works
                </Link>
              </li>
              <li>
                <Link href="/#scoring" className="hover:text-emerald-700 transition-colors font-medium">
                  Formula & Heuristic Weights
                </Link>
              </li>
              <li>
                <Link href="/#features" className="hover:text-emerald-700 transition-colors font-medium">
                  Agentic Architecture
                </Link>
              </li>
            </ul>
          </div>

          {/* Legal and Support */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-900">Trust & Transparency</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/privacy" className="hover:text-emerald-700 transition-colors font-medium">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="/terms" className="hover:text-emerald-700 transition-colors font-medium">
                  Terms of Service
                </Link>
              </li>
              <li>
                <Link href="/faq" className="hover:text-emerald-700 transition-colors font-medium">
                  Frequently Asked Questions
                </Link>
              </li>
              <li>
                <a
                  href="https://github.com/sachinrawat6264384464/ATS_resume"
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-emerald-700 transition-colors font-medium"
                >
                  GitHub Repository
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Disclaimer & Bottom Bar */}
        <div className="pt-8 border-t border-slate-100 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <p>
            &copy; 2026 ResumeIQ. Built with deterministic NLP algorithms & semantic AI.
            <span className="block mt-1 text-slate-400">
              Disclaimer: ResumeIQ provides calibrated heuristic matching scores and recommendations; it does not represent any specific proprietary corporate ATS.
            </span>
          </p>
          <div className="flex items-center gap-1 text-emerald-700 font-medium">
            <span>Open Source & Public Access</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
