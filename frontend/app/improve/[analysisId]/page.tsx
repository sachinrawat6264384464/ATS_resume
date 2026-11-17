"use client";

import React, { useEffect, useState, Suspense } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  FileText,
  Check,
  Copy,
  ArrowLeft,
  Sparkles,
  ShieldCheck,
  AlertCircle,
  Loader2,
} from "lucide-react";
import { analysisApi, AnalysisReport } from "@/services/api";

function ImproveContent() {
  const params = useParams();
  const analysisId = (params?.analysisId as string) || "";

  const [report, setReport] = useState<AnalysisReport | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [approvedIds, setApprovedIds] = useState<Set<string>>(new Set());
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!analysisId) return;

    async function loadReport() {
      try {
        const data = await analysisApi.getReport(analysisId);
        setReport(data);
        const initialApproved = new Set<string>();
        data.recommendations?.forEach((r) => {
          if (r.priority === "high" || r.original_text) {
            initialApproved.add(r.id);
          }
        });
        setApprovedIds(initialApproved);
      } catch (err: any) {
        setError("Failed to load recommendations.");
      } finally {
        setIsLoading(false);
      }
    }
    loadReport();
  }, [analysisId]);

  const toggleApproval = (id: string) => {
    const next = new Set(approvedIds);
    if (next.has(id)) {
      next.delete(id);
    } else {
      next.add(id);
    }
    setApprovedIds(next);
  };

  const handleCopyApproved = () => {
    if (!report) return;
    const textToCopy = report.recommendations
      .filter((r) => approvedIds.has(r.id))
      .map((r) => `• ${r.suggested_text || r.reasoning}`)
      .join("\n\n");

    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (isLoading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center space-y-4">
        <Loader2 className="w-8 h-8 animate-spin text-emerald-600" />
        <p className="text-sm font-semibold text-slate-600">Loading Improvement Workspace...</p>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="max-w-xl mx-auto px-4 py-20 text-center space-y-4">
        <AlertCircle className="w-10 h-10 text-rose-600 mx-auto" />
        <h2 className="text-xl font-bold text-slate-800">Workspace Unavailable</h2>
        <p className="text-sm text-slate-600">{error || "Analysis report not found."}</p>
        <Link
          href={`/results/${analysisId}`}
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-600 text-white text-xs font-bold hover:bg-emerald-700 transition-colors"
        >
          Return to Results
        </Link>
      </div>
    );
  }

  const bulletRecs = report.recommendations.filter((r) => r.category === "bullet_point");
  const keywordRecs = report.recommendations.filter((r) => r.category === "keyword");
  const otherRecs = report.recommendations.filter(
    (r) => r.category !== "bullet_point" && r.category !== "keyword"
  );

  return (
    <div className="min-h-screen bg-slate-50/70 py-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        {/* Top Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
          <div>
            <Link
              href={`/results/${analysisId}`}
              className="inline-flex items-center gap-1.5 text-xs text-emerald-700 hover:text-emerald-800 hover:underline font-semibold mb-1"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back to Audit Dashboard</span>
            </Link>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              Resume Improvement Workspace
            </h1>
            <p className="text-xs text-slate-500 mt-0.5">
              Side-by-side action-verb rewrites, keyword enrichment, and metric optimization.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handleCopyApproved}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-sm shadow-emerald-600/20 transition-all active:scale-[0.98]"
            >
              {copied ? <Check className="w-4 h-4 text-emerald-200" /> : <Copy className="w-4 h-4" />}
              <span>{copied ? "Copied to Clipboard!" : `Copy Approved (${approvedIds.size})`}</span>
            </button>
          </div>
        </div>

        {/* Non-Fabrication Guarantee Alert */}
        <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center gap-3 text-emerald-900 text-xs shadow-xs">
          <ShieldCheck className="w-5 h-5 text-emerald-600 shrink-0" />
          <div>
            <span className="font-bold">Zero-Fabrication Guarantee:</span>
            <p className="mt-0.5 text-emerald-800">
              ResumeIQ enhances syntax, replaces passive verbs, and highlights keyword context without inventing false employment history, credentials, or metrics.
            </p>
          </div>
        </div>

        {/* Bullet Points Side-by-Side Comparison */}
        {bulletRecs.length > 0 && (
          <div className="bg-white rounded-2xl border border-emerald-100 p-6 shadow-sm space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h3 className="font-bold text-slate-900 text-base">
                Work Experience Bullet Rewrites ({bulletRecs.length})
              </h3>
              <span className="text-xs text-slate-500">Side-by-side executive action verb upgrade</span>
            </div>

            <div className="space-y-4">
              {bulletRecs.map((rec) => {
                const isApproved = approvedIds.has(rec.id);

                return (
                  <div
                    key={rec.id}
                    className={`p-4 rounded-xl border transition-all ${
                      isApproved
                        ? "bg-emerald-50/40 border-emerald-200 shadow-xs"
                        : "bg-slate-50 border-slate-200 opacity-80"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 flex-1 text-xs">
                        {/* Original */}
                        <div className="p-3 bg-white rounded-lg border border-slate-200/80 space-y-1">
                          <span className="text-[10px] font-bold uppercase text-slate-400 block">
                            Original Phrasing
                          </span>
                          <p className="text-slate-600 line-through leading-relaxed">
                            {rec.original_text}
                          </p>
                        </div>

                        {/* Suggested */}
                        <div className="p-3 bg-emerald-50/60 rounded-lg border border-emerald-200 space-y-1">
                          <span className="text-[10px] font-bold uppercase text-emerald-800 block flex items-center gap-1">
                            <Sparkles className="w-3 h-3 text-emerald-600" />
                            <span>Recommended Action-Verb Upgrade</span>
                          </span>
                          <p className="text-emerald-950 font-medium leading-relaxed">
                            {rec.suggested_text}
                          </p>
                        </div>
                      </div>

                      {/* Approve Toggle */}
                      <button
                        onClick={() => toggleApproval(rec.id)}
                        className={`px-3.5 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 shrink-0 transition-colors ${
                          isApproved
                            ? "bg-emerald-600 text-white shadow-xs"
                            : "bg-slate-200 text-slate-700 hover:bg-slate-300"
                        }`}
                      >
                        <Check className="w-3.5 h-3.5" />
                        <span>{isApproved ? "Approved" : "Approve"}</span>
                      </button>
                    </div>

                    <p className="text-[11px] text-slate-500 mt-2 pl-1">
                      <b>Rationale:</b> {rec.reasoning}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Missing Keyword Integration Section */}
        {keywordRecs.length > 0 && (
          <div className="bg-white rounded-2xl border border-emerald-100 p-6 shadow-sm space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h3 className="font-bold text-slate-900 text-base">
                Missing Target Keywords ({keywordRecs.length})
              </h3>
              <span className="text-xs text-rose-600 font-semibold">Recruiter Prerequisite Gaps</span>
            </div>

            <div className="space-y-3">
              {keywordRecs.map((rec) => {
                const isApproved = approvedIds.has(rec.id);
                return (
                  <div
                    key={rec.id}
                    className="p-4 bg-slate-50 rounded-xl border border-slate-200 text-xs flex items-center justify-between gap-4"
                  >
                    <div className="space-y-1">
                      <p className="font-bold text-slate-900 text-sm">{rec.suggested_text}</p>
                      <p className="text-[11px] text-slate-500">{rec.reasoning}</p>
                    </div>

                    <button
                      onClick={() => toggleApproval(rec.id)}
                      className={`px-3.5 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 shrink-0 transition-colors ${
                        isApproved
                          ? "bg-emerald-600 text-white shadow-xs"
                          : "bg-slate-200 text-slate-700 hover:bg-slate-300"
                      }`}
                    >
                      <Check className="w-3.5 h-3.5" />
                      <span>{isApproved ? "Approved" : "Approve"}</span>
                    </button>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Formatting & Structural Advice */}
        {otherRecs.length > 0 && (
          <div className="bg-white rounded-2xl border border-emerald-100 p-6 shadow-sm space-y-4">
            <h3 className="font-bold text-slate-900 text-base">Structure & Layout Advice</h3>
            <div className="space-y-3">
              {otherRecs.map((rec) => (
                <div
                  key={rec.id}
                  className="p-3.5 bg-slate-50 rounded-xl border border-slate-200/80 text-xs space-y-1"
                >
                  <p className="font-bold text-slate-800">{rec.suggested_text}</p>
                  <p className="text-[11px] text-slate-500">{rec.reasoning}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function ImprovePage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-[60vh] flex items-center justify-center">
          <Loader2 className="w-10 h-10 animate-spin text-emerald-600" />
        </div>
      }
    >
      <ImproveContent />
    </Suspense>
  );
}
