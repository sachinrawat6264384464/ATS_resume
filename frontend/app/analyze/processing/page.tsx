"use client";

import React, { useEffect, useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import {
  Cpu,
  CheckCircle2,
  Loader2,
  AlertTriangle,
  ShieldCheck,
} from "lucide-react";
import { analysisApi, AnalysisStatusResponse } from "@/services/api";

const AGENT_STAGES = [
  { name: "Resume Parser Agent", desc: "Extracting blocks, contact, and section geometry" },
  { name: "JD Analyzer Agent", desc: "Decomposing requirements, experience & qualifications" },
  { name: "Skill Intelligence Agent", desc: "Canonical taxonomy normalization and alias resolution" },
  { name: "Matching Engine Agent", desc: "Exact keyword, BM25 ranking, and local BGE embeddings" },
  { name: "Scoring Engine Agent", desc: "Calculating calibrated mathematical ATS weights" },
  { name: "Resume Improvement Agent", desc: "Formulating non-hallucinatory bullet rewrites" },
  { name: "Validation Agent", desc: "Auditing calculation integrity and evidence spans" },
  { name: "Report Generation Agent", desc: "Assembling final explainable dashboard report" },
];

function ProcessingContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const resumeId = searchParams.get("resumeId");
  const jobId = searchParams.get("jobId");

  const [analysisId, setAnalysisId] = useState<string | null>(null);
  const [statusData, setStatusData] = useState<AnalysisStatusResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // 1. Initial Dispatch
  useEffect(() => {
    if (!resumeId || !jobId) {
      setError("Missing resume ID or job ID. Please return to the upload screen.");
      return;
    }

    let isMounted = true;

    async function startAnalysis() {
      try {
        const initial = await analysisApi.createAnalysis(resumeId!, jobId!);
        if (isMounted) {
          setAnalysisId(initial.analysis_id);
          setStatusData(initial);
        }
      } catch (err: any) {
        if (isMounted) {
          setError(err.response?.data?.detail || "Failed to initialize ATS agent pipeline.");
        }
      }
    }

    startAnalysis();

    return () => {
      isMounted = false;
    };
  }, [resumeId, jobId]);

  // 2. Polling Loop
  useEffect(() => {
    if (!analysisId) return;

    let timer: NodeJS.Timeout;

    const pollStatus = async () => {
      try {
        const current = await analysisApi.getStatus(analysisId);
        setStatusData(current);

        if (current.status === "completed") {
          // Smooth transition to results page
          setTimeout(() => {
            router.push(`/results/${analysisId}`);
          }, 800);
        } else if (current.status === "failed") {
          setError(current.error || "Analysis pipeline encountered a validation error.");
        } else {
          timer = setTimeout(pollStatus, 1500);
        }
      } catch (err: any) {
        setError("Failed to query analysis progress.");
      }
    };

    timer = setTimeout(pollStatus, 1200);

    return () => clearTimeout(timer);
  }, [analysisId, router]);

  const progress = statusData?.progress_percentage || 10;
  const currentStageIndex = Math.min(
    AGENT_STAGES.length - 1,
    Math.floor((progress / 100) * AGENT_STAGES.length)
  );

  return (
    <div className="min-h-screen bg-slate-50/70 py-16">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10">
        {/* Header */}
        <div className="text-center space-y-3">
          <div className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold shadow-sm">
            <Cpu className="w-3.5 h-3.5 animate-pulse text-emerald-600" />
            <span>Stage 3: LangGraph Agent Orchestration</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
            Analyzing Your Resume
          </h1>
          <p className="text-sm text-slate-600 max-w-lg mx-auto leading-relaxed">
            Running 8 deterministic Python agents across keyword normalization, BM25 retrieval, and local BGE-small embeddings.
          </p>
        </div>

        {error ? (
          <div className="p-6 bg-rose-50 rounded-2xl border border-rose-200 text-rose-800 space-y-4 text-center">
            <AlertTriangle className="w-8 h-8 text-rose-600 mx-auto" />
            <div>
              <h3 className="font-bold text-base">Processing Error</h3>
              <p className="text-xs text-rose-700 mt-1">{error}</p>
            </div>
            <button
              onClick={() => router.push("/analyze")}
              className="px-5 py-2.5 rounded-xl bg-emerald-600 text-white text-xs font-bold hover:bg-emerald-700 transition-colors shadow-sm"
            >
              Return to Upload
            </button>
          </div>
        ) : (
          <div className="bg-white rounded-2xl border border-emerald-100 p-6 sm:p-8 shadow-sm space-y-8">
            {/* Progress Bar */}
            <div className="space-y-2">
              <div className="flex justify-between items-center text-xs">
                <span className="font-bold text-slate-700 flex items-center gap-2">
                  <Loader2 className="w-3.5 h-3.5 animate-spin text-emerald-600" />
                  <span>{statusData?.stage || "Orchestrating agents..."}</span>
                </span>
                <span className="font-mono font-bold text-emerald-700 text-sm">
                  {progress}%
                </span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-emerald-600 to-teal-500 h-2.5 rounded-full transition-all duration-500"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>

            {/* Agent Pipeline Steps */}
            <div className="space-y-3 pt-2">
              <h4 className="text-xs uppercase font-bold tracking-wider text-slate-400">
                Active Agent Pipeline (LangGraph)
              </h4>

              <div className="divide-y divide-slate-100 border border-slate-100 rounded-xl overflow-hidden">
                {AGENT_STAGES.map((agent, idx) => {
                  const isCompleted = idx < currentStageIndex || progress >= 100;
                  const isCurrent = idx === currentStageIndex && progress < 100;

                  return (
                    <div
                      key={idx}
                      className={`p-3.5 flex items-center justify-between text-xs transition-colors ${
                        isCurrent
                          ? "bg-emerald-50/60"
                          : isCompleted
                          ? "bg-white"
                          : "bg-slate-50/40 opacity-60"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div
                          className={`w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold ${
                            isCompleted
                              ? "bg-emerald-100 text-emerald-700"
                              : isCurrent
                              ? "bg-emerald-600 text-white animate-bounce"
                              : "bg-slate-200 text-slate-500"
                          }`}
                        >
                          {isCompleted ? <CheckCircle2 className="w-4 h-4 text-emerald-700" /> : idx + 1}
                        </div>

                        <div>
                          <span className={`font-bold block ${isCurrent ? "text-emerald-950" : "text-slate-800"}`}>
                            {agent.name}
                          </span>
                          <span className="text-[11px] text-slate-500">{agent.desc}</span>
                        </div>
                      </div>

                      <div>
                        {isCompleted ? (
                          <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                            Done
                          </span>
                        ) : isCurrent ? (
                          <span className="text-[10px] font-semibold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded flex items-center gap-1 border border-emerald-200">
                            <Loader2 className="w-2.5 h-2.5 animate-spin text-emerald-700" />
                            <span>Active</span>
                          </span>
                        ) : (
                          <span className="text-[10px] text-slate-400">Queued</span>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {/* Trust Callout */}
        <div className="text-center text-xs text-slate-500 flex items-center justify-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>No external cloud LLM calls &middot; 100% deterministic mathematical evaluation</span>
        </div>
      </div>
    </div>
  );
}

export default function ProcessingPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-[50vh] flex items-center justify-center">
          <Loader2 className="w-8 h-8 animate-spin text-emerald-600" />
        </div>
      }
    >
      <ProcessingContent />
    </Suspense>
  );
}
