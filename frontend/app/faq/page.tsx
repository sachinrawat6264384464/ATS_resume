import Link from "next/link";
import { HelpCircle } from "lucide-react";

export default function FaqPage() {
  const faqs = [
    {
      q: "What makes ResumeIQ different from ordinary resume checkers?",
      a: "Most online resume checkers simply search for keywords using naive substring matching, which triggers false matches (e.g. matching 'Java' inside 'JavaScript'). ResumeIQ normalizes skills via a canonical taxonomy, resolves technical aliases, runs BM25 contextual relevance, uses local BGE-small embeddings, and calculates non-overlapping employment tenure.",
    },
    {
      q: "Why is there no login or user registration?",
      a: "We believe privacy and accessibility come first. Job seekers should not have to create accounts, remember passwords, or surrender their email addresses just to check if their resume meets a job description.",
    },
    {
      q: "How is the ATS Match Score calculated?",
      a: "The score is calculated via an explainable, versioned formula: (Keyword Match × 40%) + (Semantic Relevance × 25%) + (Experience Match × 20%) + (Project Relevance × 10%) + (Education Match × 5%). Each component is displayed individually along with evidence citations.",
    },
    {
      q: "What happens if a job has mandatory requirements I lack?",
      a: "ResumeIQ separates mandatory prerequisites from preferred nice-to-haves. Even if your overall score is high, missing mandatory skills will be visibly highlighted so you know exactly what recruiters will flag.",
    },
    {
      q: "Does ResumeIQ use OpenAI or external cloud LLMs?",
      a: "No! The core ATS intelligence engine runs completely locally using deterministic Python algorithms, spaCy NLP, fastembed BGE embeddings, and LangGraph agent orchestration. If Ollama is optionally configured, it can assist with bullet rewrites, but is never required.",
    },
  ];

  return (
    <div className="min-h-screen bg-slate-50/70 py-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        <div className="space-y-4 border-b border-emerald-100 pb-8">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold shadow-xs">
            <HelpCircle className="w-4 h-4 text-emerald-600" />
            <span>Knowledge Base</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900">Frequently Asked Questions</h1>
          <p className="text-slate-600 text-base">
            Detailed answers on ATS mechanics, privacy, and our agentic matching engine.
          </p>
        </div>

        <div className="space-y-4">
          {faqs.map((faq, i) => (
            <div key={i} className="p-6 bg-white rounded-2xl border border-emerald-100 shadow-sm space-y-2">
              <h3 className="font-bold text-slate-900 text-base">{faq.q}</h3>
              <p className="text-sm text-slate-600 leading-relaxed">{faq.a}</p>
            </div>
          ))}
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
