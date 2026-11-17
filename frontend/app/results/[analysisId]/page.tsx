"use client";

import React, { useEffect, useState, Suspense } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  FileText,
  Download,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Briefcase,
  GraduationCap,
  ArrowRight,
  ShieldCheck,
  ChevronRight,
  Layers,
  HelpCircle,
  ExternalLink,
  Edit3,
  Loader2,
} from "lucide-react";
import { analysisApi, AnalysisReport } from "@/services/api";
import ScoreGauge from "@/components/results/ScoreGauge";
import CategoryBreakdownChart from "@/components/charts/CategoryBreakdownChart";
import SkillGapChart from "@/components/charts/SkillGapChart";

function ResultsContent() {
  const params = useParams();
  const analysisId = (params?.analysisId as string) || "";

  const [report, setReport] = useState<AnalysisReport | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedFilter, setSelectedFilter] = useState<"all" | "mandatory" | "matched" | "related">("all");

  useEffect(() => {
    if (!analysisId) return;

    async function loadReport() {
      try {
        const data = await analysisApi.getReport(analysisId);
        setReport(data);
      } catch (err: any) {
        setError(err.response?.data?.detail || "Failed to load ATS analysis report.");
      } finally {
        setIsLoading(false);
      }
    }
    loadReport();
  }, [analysisId]);

  const handleDownloadPdf = () => {
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000/api/v1";
    window.open(`${backendUrl}/reports/${analysisId}/pdf`, "_blank");
  };

  if (isLoading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center space-y-4">
        <Loader2 className="w-10 h-10 animate-spin text-blue-600" />
        <p className="text-sm font-semibold text-slate-600">Loading your ATS Audit Report...</p>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="max-w-xl mx-auto px-4 py-20 text-center space-y-4">
        <AlertTriangle className="w-12 h-12 text-rose-600 mx-auto" />
        <h2 className="text-xl font-bold text-slate-800">Could Not Load Report</h2>
        <p className="text-sm text-slate-600">{error || "Report not found."}</p>
        <Link
          href="/analyze"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-blue-600 text-white text-xs font-bold"
        >
          Return to Analyzer
        </Link>
      </div>
    );
  }

  const { scores, matched_skills, missing_skills, missing_mandatory, related_skills, experience_analysis } = report;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Top Action Header */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-0.5 rounded-md border border-blue-200">
              ATS Audit Report
            </span>
            <span className="text-xs text-slate-400 font-mono">ID: {analysisId.slice(0, 8)}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            {report.candidate_name || "Candidate"} &mdash; {report.job_title || "Target Role"}
          </h1>
          <p className="text-xs text-slate-500">
            Evaluated by ResumeIQ v1.0.0 &bull; Deterministic NLP, BM25 & Local BGE-small Embeddings
          </p>
        </div>

        {/* Buttons */}
        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={handleDownloadPdf}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold text-slate-700 bg-white hover:bg-slate-50 border border-slate-300 shadow-sm transition-all"
          >
            <Download className="w-4 h-4 text-slate-600" />
            <span>Download PDF Report</span>
          </button>

          <Link
            href={`/improve/${analysisId}`}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 shadow-md shadow-blue-500/20 active:scale-[0.98] transition-all"
          >
            <Edit3 className="w-4 h-4" />
            <span>Open Improvement Workspace</span>
          </Link>
        </div>
      </div>

      {/* Critical Mandatory Gaps Banner if any */}
      {missing_mandatory && missing_mandatory.length > 0 && (
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-2xl flex items-start gap-3.5 text-rose-900 shadow-sm">
          <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
          <div className="space-y-1 flex-1">
            <div className="flex items-center justify-between">
              <h4 className="text-sm font-bold">
                Critical Mandatory Prerequisite Gap ({missing_mandatory.length} Missing)
              </h4>
              <span className="text-[11px] font-semibold text-rose-700 bg-rose-100 px-2 py-0.5 rounded">
                High Rejection Risk
              </span>
            </div>
            <p className="text-xs text-rose-800 leading-relaxed">
              Recruiter screening algorithms specifically require the following skills as mandatory prerequisites.
              Even with a high overall score, lacking these may trigger an immediate rejection:
            </p>
            <div className="flex flex-wrap gap-1.5 pt-1">
              {missing_mandatory.map((skill, i) => (
                <span
                  key={i}
                  className="px-2.5 py-1 rounded-md bg-white border border-rose-300 text-rose-800 text-xs font-bold shadow-xs"
                >
                  &times; {skill}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Grid: Score Gauge + Category Breakdown Bar Chart + Skill Gap Pie */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
        {/* Score Gauge Card */}
        <div className="lg:col-span-4 bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
              <h3 className="font-bold text-slate-800 text-sm">Overall ATS Score</h3>
              <span className="text-[10px] text-slate-400 font-mono">Calibrated Heuristic</span>
            </div>
            <ScoreGauge score={scores.overall} rating={scores.rating || "Evaluated"} />
          </div>

          <div className="mt-6 pt-4 border-t border-slate-100 text-center">
            <p className="text-xs text-slate-500 leading-relaxed">
              Calculated using transparent formula: (Keyword &times; 40%) + (Semantic &times; 25%) + (Experience &times; 20%) + (Projects &times; 10%) + (Education &times; 5%).
            </p>
          </div>
        </div>

        {/* Category Breakdown Bar Chart */}
        <div className="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-2">
            <h3 className="font-bold text-slate-800 text-sm">Component Score Breakdown</h3>
            <span className="text-[11px] font-semibold text-blue-600">Target: 75%+</span>
          </div>
          <CategoryBreakdownChart scores={scores} />
        </div>

        {/* Skill Gap Pie Chart */}
        <div className="lg:col-span-3 bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-2">
            <h3 className="font-bold text-slate-800 text-sm">Skill Gap Matrix</h3>
            <span className="text-[11px] font-semibold text-slate-500">Distribution</span>
          </div>
          <SkillGapChart
            matchedCount={matched_skills.length}
            relatedCount={related_skills.length}
            missingCount={missing_skills.length}
          />
        </div>
      </div>

      {/* Experience & Tenure Non-Overlapping Verification */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <Clock className="w-5 h-5 text-indigo-600" />
            <h3 className="font-bold text-slate-800 text-base">Chronological Experience Verification</h3>
          </div>
          <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-indigo-50 text-indigo-700 border border-indigo-200">
            Deduplicated Tenure
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200/80">
            <span className="text-slate-500 block text-[11px]">Candidate Verified Tenure</span>
            <span className="text-lg font-bold text-slate-900 mt-0.5 block">
              {experience_analysis.candidate_years || 0} Years ({experience_analysis.tenure_details?.total_months || 0} Months)
            </span>
          </div>

          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200/80">
            <span className="text-slate-500 block text-[11px]">Job Description Prerequisite</span>
            <span className="text-lg font-bold text-slate-900 mt-0.5 block">
              {experience_analysis.required_years || 0} Years Required
            </span>
          </div>

          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200/80">
            <span className="text-slate-500 block text-[11px]">Overlapping Dates Deducted</span>
            <span className="text-lg font-bold text-emerald-700 mt-0.5 block">
              {experience_analysis.tenure_details?.overlap_months_deducted || 0} Months Deducted
            </span>
          </div>
        </div>

        {experience_analysis.tenure_details?.has_overlaps && (
          <p className="text-xs text-slate-500">
            &bull; Notice: ResumeIQ detected concurrent employment dates and merged overlapping timeframes to prevent double-counting tenure.
          </p>
        )}
      </div>

      {/* Verified Skills & Evidence Provenance Section */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-3 border-b border-slate-100">
          <div>
            <h3 className="font-bold text-slate-900 text-base">Skill Evidence & Matching Matrix</h3>
            <p className="text-xs text-slate-500">Proof levels: Demonstrated in Experience, Projects, or Skills List</p>
          </div>

          <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-lg text-xs font-semibold">
            <button
              onClick={() => setSelectedFilter("all")}
              className={`px-3 py-1 rounded-md transition-colors ${
                selectedFilter === "all" ? "bg-white text-blue-600 shadow-xs" : "text-slate-600"
              }`}
            >
              All Skills ({matched_skills.length + missing_skills.length})
            </button>
            <button
              onClick={() => setSelectedFilter("matched")}
              className={`px-3 py-1 rounded-md transition-colors ${
                selectedFilter === "matched" ? "bg-white text-emerald-600 shadow-xs" : "text-slate-600"
              }`}
            >
              Verified ({matched_skills.length})
            </button>
            <button
              onClick={() => setSelectedFilter("mandatory")}
              className={`px-3 py-1 rounded-md transition-colors ${
                selectedFilter === "mandatory" ? "bg-white text-rose-600 shadow-xs" : "text-slate-600"
              }`}
            >
              Gaps ({missing_mandatory.length})
            </button>
            <button
              onClick={() => setSelectedFilter("related")}
              className={`px-3 py-1 rounded-md transition-colors ${
                selectedFilter === "related" ? "bg-white text-indigo-600 shadow-xs" : "text-slate-600"
              }`}
            >
              Related ({related_skills.length})
            </button>
          </div>
        </div>

        {/* Skills Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {(selectedFilter === "all" || selectedFilter === "matched") &&
            matched_skills.map((skill, idx) => (
              <div
                key={idx}
                className="p-3.5 bg-slate-50 rounded-xl border border-slate-200/80 space-y-2 text-xs"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    <span className="font-bold text-slate-800 text-sm">{skill.canonical}</span>
                  </div>
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-emerald-100 text-emerald-800">
                    {skill.evidence_level?.replace(/_/g, " ") || "Verified"}
                  </span>
                </div>
                <p className="text-slate-600 text-[11px] leading-relaxed">
                  {skill.provenance || skill.evidence || "Found in resume."}
                </p>
                {skill.snippet && (
                  <div className="p-2 bg-white rounded border border-slate-200 text-[11px] font-mono text-slate-600 line-clamp-2">
                    &ldquo;{skill.snippet}&rdquo;
                  </div>
                )}
              </div>
            ))}

          {(selectedFilter === "all" || selectedFilter === "related") &&
            related_skills.map((rel, idx) => (
              <div
                key={idx}
                className="p-3.5 bg-blue-50/50 rounded-xl border border-blue-200/80 space-y-1.5 text-xs"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-blue-900 text-sm">
                    Required: {rel.required} &rarr; Candidate: {rel.candidate_possesses}
                  </span>
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-blue-100 text-blue-800">
                    Partial Credit (40%)
                  </span>
                </div>
                <p className="text-slate-600 text-[11px] leading-relaxed">
                  {rel.relevance_note}
                </p>
              </div>
            ))}

          {(selectedFilter === "all" || selectedFilter === "mandatory") &&
            missing_skills.map((gap, idx) => (
              <div
                key={idx}
                className="p-3.5 bg-rose-50/50 rounded-xl border border-rose-200/80 space-y-1.5 text-xs"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-rose-900 text-sm">
                    Missing: {gap.canonical}
                  </span>
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-rose-100 text-rose-800">
                    {gap.is_mandatory ? "Mandatory Prerequisite" : "Preferred"}
                  </span>
                </div>
                <p className="text-rose-700 text-[11px] leading-relaxed">
                  {gap.context || "Not detected in candidate experience, projects, or skill lists."}
                </p>
              </div>
            ))}
        </div>
      </div>

      {/* Recommendations & Action Plan */}
      {report.recommendations && report.recommendations.length > 0 && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="font-bold text-slate-800 text-base">Actionable Improvement Plan</h3>
              <p className="text-xs text-slate-500">
                Evidence-based suggestions preserving authentic candidate facts
              </p>
            </div>
            <Link
              href={`/improve/${analysisId}`}
              className="text-xs text-blue-600 font-semibold hover:underline flex items-center gap-1"
            >
              <span>Launch Improvement Workspace</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-3">
            {report.recommendations.slice(0, 4).map((rec, i) => (
              <div
                key={i}
                className="p-3.5 bg-slate-50 rounded-xl border border-slate-200/70 text-xs space-y-1.5"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-800 uppercase tracking-wider text-[10px]">
                    {rec.category.replace("_", " ")} &bull; {rec.priority} Priority
                  </span>
                </div>
                <p className="text-slate-700 font-medium">{rec.suggested_text}</p>
                <p className="text-[11px] text-slate-500">{rec.reasoning}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default function ResultsPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-[60vh] flex items-center justify-center">
          <Loader2 className="w-10 h-10 animate-spin text-blue-600" />
        </div>
      }
    >
      <ResultsContent />
    </Suspense>
  );
}
