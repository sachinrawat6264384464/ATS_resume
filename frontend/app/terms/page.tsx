import Link from "next/link";
import { AlertCircle } from "lucide-react";

export default function TermsPage() {
  return (
    <div className="min-h-screen bg-slate-50/70 py-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        <div className="space-y-4 border-b border-emerald-100 pb-8">
          <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900">Terms of Service & Disclaimer</h1>
          <p className="text-slate-600 text-base">
            Guidelines and transparency statements for using ResumeIQ.
          </p>
        </div>

        <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl flex items-start gap-3 text-emerald-950 text-sm shadow-xs">
          <AlertCircle className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
          <div>
            <span className="font-bold">Important ATS Score Disclaimer:</span>
            <p className="mt-1 text-xs text-emerald-800 leading-relaxed">
              ResumeIQ calculates an explainable, calibrated heuristic match score based on NLP parsing, BM25 keyword relevance,
              and semantic cosine similarity. It does not guarantee employment or claim to replicate the exact internal scoring algorithms of proprietary ATS vendors (such as Workday, Taleo, Greenhouse, or Lever).
            </p>
          </div>
        </div>

        <div className="space-y-6 text-sm text-slate-600 leading-relaxed">
          <h2 className="text-lg font-bold text-slate-900">1. Acceptable Use</h2>
          <p>
            You agree to submit authentic resumes and job postings for personal career optimization. You may not upload malicious files,
            attempt denial-of-service attacks, or reverse-engineer the underlying service boundaries.
          </p>

          <h2 className="text-lg font-bold text-slate-900">2. No Guarantee of Employment</h2>
          <p>
            Hiring decisions rest entirely with employers. High scores on ResumeIQ reflect statistical alignment with stated job requirements,
            not an offer or guarantee of interview selection.
          </p>

          <h2 className="text-lg font-bold text-slate-900">3. Factual Integrity</h2>
          <p>
            ResumeIQ provides wording and formatting suggestions. Candidates remain solely responsible for the truthfulness and factual accuracy of their resumes.
            ResumeIQ explicitly instructs users never to fabricate qualifications or achievements.
          </p>
        </div>

        <div className="pt-6 border-t border-slate-200 flex justify-between items-center text-sm font-semibold">
          <Link href="/" className="text-emerald-700 hover:text-emerald-800 hover:underline">
            &larr; Back to Home
          </Link>
          <Link href="/analyze" className="text-emerald-700 hover:text-emerald-800 hover:underline">
            Start Analysis &rarr;
          </Link>
        </div>
      </div>
    </div>
  );
}
