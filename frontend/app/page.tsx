"use client";

import Link from "next/link";
import { useState } from "react";
import {
  FileText,
  Briefcase,
  Cpu,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  Sparkles,
  Layers,
  Search,
  Scale,
  Code2,
  FileSearch,
  ChevronDown,
  BarChart3,
  Clock,
  HelpCircle,
  Award,
  Zap,
} from "lucide-react";

export default function LandingPage() {
  const [activeFaq, setActiveFaq] = useState<number | null>(null);

  const toggleFaq = (index: number) => {
    setActiveFaq(activeFaq === index ? null : index);
  };

  return (
    <div className="flex flex-col min-h-screen bg-white">
      {/* HERO SECTION WITH ENHANCED HIGH-DEFINITION GRID BOXES */}
      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-50/50 via-white to-white pt-20 pb-28 border-b border-emerald-100">
        {/* Crisp Geometric Grid Boxes Background Layer */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#cbd5e1_1px,transparent_1px),linear-gradient(to_bottom,#cbd5e1_1px,transparent_1px)] bg-[size:44px_44px] [mask-image:radial-gradient(ellipse_80%_65%_at_50%_25%,#000_70%,transparent_100%)] opacity-60 pointer-events-none" />

        {/* Ambient Emerald Radial Glow */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-[520px] bg-[radial-gradient(ellipse_60%_50%_at_50%_10%,rgba(16,185,129,0.14),transparent_80%)] pointer-events-none" />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto space-y-6">
            {/* Pill Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white border border-emerald-200/90 text-emerald-800 text-xs font-semibold tracking-wide shadow-sm">
              <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
              <span>100% Deterministic ATS Intelligence &middot; No Signup Required</span>
            </div>

            {/* Headline */}
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight leading-[1.14]">
              Real ATS Resume Analysis.{" "}
              <span className="bg-gradient-to-r from-emerald-700 via-teal-600 to-emerald-600 bg-clip-text text-transparent">
                Explainable, Evidence-Backed.
              </span>
            </h1>

            {/* Subtitle */}
            <p className="text-lg sm:text-xl text-slate-600 leading-relaxed font-normal max-w-2xl mx-auto">
              Stop guessing why your resume gets rejected. ResumeIQ parses your resume and target job description using
              local semantic embeddings, BM25 keyword ranking, and deterministic NLP algorithms.
            </p>

            {/* CTA Group */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
              <Link
                href="/analyze"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-4 rounded-xl text-base font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-xl shadow-emerald-600/25 active:scale-[0.98] transition-all"
              >
                <span>Analyze My Resume Now</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
              <Link
                href="#how-it-works"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl text-base font-semibold text-slate-700 bg-white hover:bg-emerald-50/60 border border-slate-300 shadow-sm transition-all"
              >
                <span>How Scoring Works</span>
              </Link>
            </div>

            {/* Micro Feature Indicators */}
            <div className="pt-6 flex flex-wrap items-center justify-center gap-6 text-xs font-medium text-slate-600">
              <div className="flex items-center gap-1.5 bg-white/80 px-3 py-1 rounded-full border border-slate-200/80 shadow-xs">
                <ShieldCheck className="w-4 h-4 text-emerald-600" />
                <span>Zero Storage / Auto-purge</span>
              </div>
              <div className="flex items-center gap-1.5 bg-white/80 px-3 py-1 rounded-full border border-slate-200/80 shadow-xs">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>No API Key Required</span>
              </div>
              <div className="flex items-center gap-1.5 bg-white/80 px-3 py-1 rounded-full border border-slate-200/80 shadow-xs">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>PDF & DOCX Support</span>
              </div>
              <div className="flex items-center gap-1.5 bg-white/80 px-3 py-1 rounded-full border border-slate-200/80 shadow-xs">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>Calibrated Explainable Scores</span>
              </div>
            </div>
          </div>

          {/* Interactive ATS Teaser Preview Card */}
          <div className="mt-14 max-w-4xl mx-auto rounded-3xl bg-white/95 backdrop-blur-md border border-emerald-200/80 shadow-2xl shadow-emerald-950/5 p-6 sm:p-8 overflow-hidden">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-slate-100">
              <div>
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
                  <span className="text-xs uppercase font-bold tracking-wider text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200/60">
                    Live ATS Engine Preview
                  </span>
                </div>
                <h3 className="text-lg font-bold text-slate-900 mt-2">Senior Full Stack Engineer &mdash; Analysis Demo</h3>
              </div>
              <div className="flex items-center gap-3">
                <div className="text-right">
                  <span className="text-xs text-slate-400 font-medium">ATS Match Score</span>
                  <p className="text-3xl font-black text-emerald-700">84 <span className="text-xs text-slate-400 font-normal">/ 100</span></p>
                </div>
                <span className="px-3 py-1.5 text-xs font-bold rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200">
                  Strong Match
                </span>
              </div>
            </div>

            {/* Score Breakdown Bar */}
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 py-6 border-b border-slate-100">
              <div className="p-3 bg-emerald-50/50 rounded-xl border border-emerald-100">
                <span className="text-[11px] font-semibold text-slate-600 block">Keywords (40%)</span>
                <span className="text-lg font-bold text-slate-900">88%</span>
                <div className="w-full bg-slate-200 rounded-full h-1.5 mt-1.5">
                  <div className="bg-emerald-600 h-1.5 rounded-full" style={{ width: "88%" }} />
                </div>
              </div>
              <div className="p-3 bg-emerald-50/50 rounded-xl border border-emerald-100">
                <span className="text-[11px] font-semibold text-slate-600 block">Semantic (25%)</span>
                <span className="text-lg font-bold text-slate-900">85%</span>
                <div className="w-full bg-slate-200 rounded-full h-1.5 mt-1.5">
                  <div className="bg-emerald-500 h-1.5 rounded-full" style={{ width: "85%" }} />
                </div>
              </div>
              <div className="p-3 bg-emerald-50/50 rounded-xl border border-emerald-100">
                <span className="text-[11px] font-semibold text-slate-600 block">Experience (20%)</span>
                <span className="text-lg font-bold text-slate-900">80%</span>
                <div className="w-full bg-slate-200 rounded-full h-1.5 mt-1.5">
                  <div className="bg-teal-600 h-1.5 rounded-full" style={{ width: "80%" }} />
                </div>
              </div>
              <div className="p-3 bg-emerald-50/50 rounded-xl border border-emerald-100">
                <span className="text-[11px] font-semibold text-slate-600 block">Projects (10%)</span>
                <span className="text-lg font-bold text-slate-900">90%</span>
                <div className="w-full bg-slate-200 rounded-full h-1.5 mt-1.5">
                  <div className="bg-emerald-700 h-1.5 rounded-full" style={{ width: "90%" }} />
                </div>
              </div>
              <div className="p-3 bg-emerald-50/50 rounded-xl border border-emerald-100 col-span-2 sm:col-span-1">
                <span className="text-[11px] font-semibold text-slate-600 block">Education (5%)</span>
                <span className="text-lg font-bold text-slate-900">100%</span>
                <div className="w-full bg-slate-200 rounded-full h-1.5 mt-1.5">
                  <div className="bg-teal-700 h-1.5 rounded-full" style={{ width: "100%" }} />
                </div>
              </div>
            </div>

            {/* Evidence Preview Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-6">
              {/* Matched Skills */}
              <div className="space-y-2">
                <span className="text-xs font-bold text-emerald-800 uppercase tracking-wider flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  Verified Skills With Evidence (14)
                </span>
                <div className="flex flex-wrap gap-1.5 text-xs">
                  <span className="px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200 font-medium">
                    Python (In Work Experience)
                  </span>
                  <span className="px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200 font-medium">
                    FastAPI (In 2 Projects)
                  </span>
                  <span className="px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200 font-medium">
                    PostgreSQL / pgvector (Demonstrated)
                  </span>
                  <span className="px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200 font-medium">
                    Docker & CI/CD
                  </span>
                </div>
              </div>

              {/* Missing Mandatory Skills */}
              <div className="space-y-2">
                <span className="text-xs font-bold text-rose-700 uppercase tracking-wider flex items-center gap-1.5">
                  <AlertTriangle className="w-4 h-4 text-rose-600" />
                  Missing Critical Requirements (2)
                </span>
                <div className="flex flex-wrap gap-1.5 text-xs">
                  <span className="px-2.5 py-1 rounded-md bg-rose-50 text-rose-800 border border-rose-200 font-medium">
                    Kubernetes (Mandatory in JD)
                  </span>
                  <span className="px-2.5 py-1 rounded-md bg-rose-50 text-rose-800 border border-rose-200 font-medium">
                    Kafka / Event Streaming
                  </span>
                </div>
              </div>
            </div>

            {/* Bottom Card CTA */}
            <div className="mt-6 pt-5 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
              <span className="text-slate-500 font-medium">
                Want to see where your resume matches and where the critical gaps are?
              </span>
              <Link
                href="/analyze"
                className="inline-flex items-center gap-1.5 font-bold text-emerald-700 hover:text-emerald-800 hover:underline"
              >
                <span>Upload Your Resume &rarr;</span>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* HOW RESUMEIQ WORKS */}
      <section id="how-it-works" className="py-20 bg-white border-b border-slate-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-16 space-y-3">
            <span className="text-xs uppercase font-bold tracking-wider text-emerald-800 bg-emerald-50 px-3.5 py-1.5 rounded-full border border-emerald-200">
              The Agentic Workflow
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900">How ResumeIQ Analyzes Your Resume</h2>
            <p className="text-slate-600">
              A 4-stage pipeline orchestrated by custom LangGraph agents running deterministic Python algorithms.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Stage 1 */}
            <div className="p-6 rounded-2xl bg-white border border-emerald-100/90 shadow-sm space-y-4 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center justify-center font-bold text-lg">
                1
              </div>
              <h3 className="text-lg font-bold text-slate-900">Upload & Extraction</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                PyMuPDF and python-docx parse untrusted PDF and DOCX files. Spans, dates, bullet points, and section boundaries are rigorously extracted.
              </p>
              <div className="text-xs font-semibold text-emerald-700 flex items-center gap-1">
                <span>Resume Parser Agent</span>
              </div>
            </div>

            {/* Stage 2 */}
            <div className="p-6 rounded-2xl bg-white border border-emerald-100/90 shadow-sm space-y-4 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center justify-center font-bold text-lg">
                2
              </div>
              <h3 className="text-lg font-bold text-slate-900">JD Decomposition</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Separates required vs preferred skills, years of experience, degree prerequisites, and technical stacks with taxonomy-grounded rules.
              </p>
              <div className="text-xs font-semibold text-emerald-700 flex items-center gap-1">
                <span>JD Analyzer Agent</span>
              </div>
            </div>

            {/* Stage 3 */}
            <div className="p-6 rounded-2xl bg-white border border-emerald-100/90 shadow-sm space-y-4 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center justify-center font-bold text-lg">
                3
              </div>
              <h3 className="text-lg font-bold text-slate-900">Hybrid Match Engine</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Applies exact keyword matching with alias resolution, BM25 section relevance, and local BGE-small semantic embeddings without hallucination.
              </p>
              <div className="text-xs font-semibold text-emerald-700 flex items-center gap-1">
                <span>Matching & Skill Intelligence Agents</span>
              </div>
            </div>

            {/* Stage 4 */}
            <div className="p-6 rounded-2xl bg-white border border-emerald-100/90 shadow-sm space-y-4 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center justify-center font-bold text-lg">
                4
              </div>
              <h3 className="text-lg font-bold text-slate-900">Explainable Scoring & Audit</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Generates a calibrated score breakdown with evidence citations, highlighted mandatory gaps, and actionable bullet improvements.
              </p>
              <div className="text-xs font-semibold text-emerald-700 flex items-center gap-1">
                <span>Scoring & Validation Agents</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* WHY RESUMEIQ VS LEGACY ATS CHECKERS */}
      <section id="scoring" className="py-20 bg-slate-50/60 border-b border-slate-200/60">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
            <span className="text-xs uppercase font-bold tracking-wider text-emerald-800 bg-emerald-50 px-3.5 py-1.5 rounded-full border border-emerald-200">
              ATS Truth & Transparency
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900">
              Why Keyword Stuffing & Blind LLMs Fail
            </h2>
            <p className="text-slate-600 leading-relaxed">
              Most resume tools are either naive regex searchers or erratic LLM wrappers that make up scores on every reload.
              Here is how ResumeIQ builds authentic, explainable ATS intelligence.
            </p>
          </div>

          {/* Comparison Table */}
          <div className="max-w-4xl mx-auto bg-white rounded-2xl border border-emerald-100 shadow-sm overflow-hidden">
            <div className="grid grid-cols-3 bg-emerald-50/60 p-4 border-b border-emerald-100 text-xs font-bold text-slate-700 uppercase tracking-wider">
              <div>Criterion</div>
              <div className="text-slate-400">Legacy Checkers / LLM Wrappers</div>
              <div className="text-emerald-800">ResumeIQ Architecture</div>
            </div>

            <div className="divide-y divide-slate-100 text-sm">
              <div className="grid grid-cols-3 p-4 items-center gap-2">
                <span className="font-semibold text-slate-900">Score Consistency</span>
                <span className="text-slate-500 text-xs">Varies on every run; hallucinated percentages</span>
                <span className="text-emerald-800 font-semibold text-xs flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  100% Deterministic formula
                </span>
              </div>

              <div className="grid grid-cols-3 p-4 items-center gap-2">
                <span className="font-semibold text-slate-900">Skill Aliases</span>
                <span className="text-slate-500 text-xs">Fails on &ldquo;React&rdquo; vs &ldquo;React.js&rdquo; or substring bugs</span>
                <span className="text-emerald-800 font-semibold text-xs flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  Curated canonical taxonomy
                </span>
              </div>

              <div className="grid grid-cols-3 p-4 items-center gap-2">
                <span className="font-semibold text-slate-900">Evidence Proof</span>
                <span className="text-slate-500 text-xs">Treats listed buzzwords identical to real experience</span>
                <span className="text-emerald-800 font-semibold text-xs flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  Differentiates bullet evidence vs mere skill lists
                </span>
              </div>

              <div className="grid grid-cols-3 p-4 items-center gap-2">
                <span className="font-semibold text-slate-900">Mandatory Gaps</span>
                <span className="text-slate-500 text-xs">Hides critical requirements inside a high generic score</span>
                <span className="text-emerald-800 font-semibold text-xs flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  Highlights critical gaps separately
                </span>
              </div>

              <div className="grid grid-cols-3 p-4 items-center gap-2">
                <span className="font-semibold text-slate-900">Privacy & Signup</span>
                <span className="text-slate-500 text-xs">Forces signup, harvests email, keeps resume forever</span>
                <span className="text-emerald-800 font-semibold text-xs flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  No login, zero tracking, auto-purge
                </span>
              </div>
            </div>
          </div>

          {/* Formula Callout */}
          <div className="mt-12 max-w-4xl mx-auto p-6 rounded-2xl bg-white border border-emerald-200 shadow-sm space-y-3">
            <div className="flex items-center gap-2 text-emerald-800 text-xs uppercase tracking-wider font-bold">
              <Scale className="w-4 h-4 text-emerald-600" />
              <span>Transparent Scoring Formula</span>
            </div>
            <p className="font-mono text-sm sm:text-base text-emerald-950 font-semibold">
              ATS Score = (Keyword &times; 0.40) + (Semantic &times; 0.25) + (Experience &times; 0.20) + (Project &times; 0.10) + (Education &times; 0.05)
            </p>
            <p className="text-xs text-slate-500 leading-relaxed">
              Every score component is independently calculated and visible. We never claim to replicate any corporate proprietary ATS black box.
            </p>
          </div>
        </div>
      </section>

      {/* CORE FEATURES GRID */}
      <section id="features" className="py-20 bg-white border-b border-slate-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-16 space-y-3">
            <span className="text-xs uppercase font-bold tracking-wider text-emerald-800 bg-emerald-50 px-3.5 py-1.5 rounded-full border border-emerald-200">
              Engineered For Accuracy
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900">Full-Spectrum ATS Capabilities</h2>
            <p className="text-slate-600">
              Built with battle-tested open-source NLP and IR algorithms designed for genuine resume optimization.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 rounded-2xl bg-white border border-emerald-100 shadow-sm space-y-3 hover:border-emerald-300 transition-all">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center justify-center">
                <Search className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-slate-900 text-lg">BM25 Section Relevance</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Leverages industry-standard Okapi BM25 to rank relevant experience descriptions and technical projects against JD requirements.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-emerald-100 shadow-sm space-y-3 hover:border-emerald-300 transition-all">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center justify-center">
                <Cpu className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-slate-900 text-lg">Local BGE-Small Embeddings</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Computes cosine similarity over dense vector spaces locally on your CPU. No external cloud dependencies or API keys required.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-emerald-100 shadow-sm space-y-3 hover:border-emerald-300 transition-all">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center justify-center">
                <Clock className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-slate-900 text-lg">Non-Overlapping Experience</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Smart chronological date parsing prevents concurrent roles and internships from being counted twice, ensuring true tenure analysis.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-emerald-100 shadow-sm space-y-3 hover:border-emerald-300 transition-all">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center justify-center">
                <FileSearch className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-slate-900 text-lg">Evidence Span Citations</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Every matched and missing skill points directly to the exact resume section or snippet where proof was discovered or missed.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-emerald-100 shadow-sm space-y-3 hover:border-emerald-300 transition-all">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center justify-center">
                <Zap className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-slate-900 text-lg">Improvement Workspace</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Side-by-side action-verb and quantitative metric suggestions that preserve your authentic career facts without hallucinating credentials.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-emerald-100 shadow-sm space-y-3 hover:border-emerald-300 transition-all">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center justify-center">
                <Award className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-slate-900 text-lg">Audit-Ready PDF Export</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Download a clean, structured PDF report complete with score breakdown, skill matrices, and actionable fixes for your review.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ SECTION */}
      <section className="py-20 bg-slate-50/60 border-b border-slate-200/60">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12 space-y-3">
            <span className="text-xs uppercase font-bold tracking-wider text-emerald-800 bg-emerald-50 px-3.5 py-1.5 rounded-full border border-emerald-200">
              Common Inquiries
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900">Frequently Asked Questions</h2>
            <p className="text-slate-600">Everything you need to know about ResumeIQ and ATS matching.</p>
          </div>

          <div className="space-y-4">
            {[
              {
                q: "Do I need to create an account or provide payment information?",
                a: "No. ResumeIQ has zero user registration, no login, no paywalls, and no subscription traps. All core features are open access to help job seekers freely.",
              },
              {
                q: "How does ResumeIQ prevent fake AI hallucinations?",
                a: "The core ATS matching engine is built on deterministic Python algorithms, spaCy NLP, custom skill taxonomy, and local BGE-small embeddings. We never use generative models to guess your score.",
              },
              {
                q: "What formats can I upload?",
                a: "ResumeIQ supports standard PDF and Microsoft Word (DOCX) files. You can also paste or edit your target job description directly in the browser.",
              },
              {
                q: "Is this score the exact score used by Taleo, Workday, or Greenhouse?",
                a: "No. Every corporate ATS is proprietary and employers configure unique filters. ResumeIQ calculates an objective, calibrated heuristic score to give you the highest statistical chance of clearing ATS filters.",
              },
              {
                q: "What happens to my uploaded resume?",
                a: "Your file is processed in isolated temporary memory and automatically expirable storage (24-hour retention). It is never sold, shared, or used to train third-party AI models.",
              },
            ].map((faq, index) => (
              <div
                key={index}
                className="bg-white rounded-xl border border-emerald-100 shadow-sm overflow-hidden"
              >
                <button
                  onClick={() => toggleFaq(index)}
                  className="w-full px-6 py-4 text-left flex items-center justify-between text-base font-semibold text-slate-800 hover:text-emerald-700 transition-colors"
                >
                  <span>{faq.q}</span>
                  <ChevronDown
                    className={`w-4 h-4 text-slate-400 transition-transform ${
                      activeFaq === index ? "rotate-180 text-emerald-600" : ""
                    }`}
                  />
                </button>
                {activeFaq === index && (
                  <div className="px-6 pb-5 pt-1 text-sm text-slate-600 leading-relaxed border-t border-slate-100">
                    {faq.a}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FINAL CTA BANNER */}
      <section className="py-20 bg-gradient-to-r from-emerald-800 via-emerald-700 to-teal-800 text-white">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
            Ready to Optimize Your Resume For ATS Filters?
          </h2>
          <p className="text-lg text-emerald-100 max-w-2xl mx-auto leading-relaxed">
            Upload your resume and target job description now to receive an instant, evidence-backed breakdown.
          </p>
          <div className="pt-2">
            <Link
              href="/analyze"
              className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl text-base font-bold text-emerald-900 bg-white hover:bg-emerald-50 shadow-xl active:scale-[0.98] transition-all"
            >
              <span>Analyze My Resume Now</span>
              <ArrowRight className="w-5 h-5 text-emerald-700" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
