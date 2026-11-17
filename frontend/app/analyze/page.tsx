"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import {
  FileText,
  Briefcase,
  ArrowRight,
  Sparkles,
  ShieldCheck,
  Zap,
} from "lucide-react";
import ResumeUploader from "@/components/resume/ResumeUploader";
import JobDescriptionInput from "@/components/analyzer/JobDescriptionInput";
import { ResumeUploadResponse, JobDescriptionResponse } from "@/services/api";

export default function AnalyzePage() {
  const router = useRouter();
  const [uploadedResume, setUploadedResume] = useState<ResumeUploadResponse | null>(null);
  const [parsedJob, setParsedJob] = useState<JobDescriptionResponse | null>(null);
  const [isStartingAnalysis, setIsStartingAnalysis] = useState(false);

  const canProceed = Boolean(uploadedResume && parsedJob);

  const handleStartAnalysis = () => {
    if (!uploadedResume || !parsedJob) return;
    setIsStartingAnalysis(true);
    // Navigate with query params for resume and job
    router.push(`/analyze/processing?resumeId=${uploadedResume.id}&jobId=${parsedJob.id}`);
  };

  return (
    <div className="min-h-screen bg-slate-50/70 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        {/* Page Header */}
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <div className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold shadow-sm">
            <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
            <span>Stage 1 & 2: Document Ingestion & Verification</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
            Upload Resume & Target Job Description
          </h1>
          <p className="text-sm sm:text-base text-slate-600 leading-relaxed">
            Our parser extracts structured sections, career dates, and skill inventories.
            Review and fine-tune your extracted details before running our deterministic ATS matching pipeline.
          </p>
        </div>

        {/* Main Dual-Column Upload & Input Area */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
          {/* Module B: Resume Upload */}
          <ResumeUploader
            uploadedResume={uploadedResume}
            onUploadSuccess={(data) => setUploadedResume(data)}
            onClear={() => setUploadedResume(null)}
          />

          {/* Module C: Job Description Input & Decomposer */}
          <JobDescriptionInput
            parsedJob={parsedJob}
            onJobParsed={(data) => setParsedJob(data)}
            onClear={() => setParsedJob(null)}
          />
        </div>

        {/* Action Footer Bar */}
        <div className="p-6 rounded-2xl bg-white border border-emerald-100 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div
              className={`w-3.5 h-3.5 rounded-full ${
                canProceed ? "bg-emerald-500 animate-pulse" : "bg-slate-300"
              }`}
            />
            <div className="text-xs">
              <span className="font-bold text-slate-800 block text-sm">
                {canProceed
                  ? "Ready for ATS Analysis"
                  : "Awaiting inputs: " +
                    (!uploadedResume ? "Upload Resume " : "") +
                    (!uploadedResume && !parsedJob ? "& " : "") +
                    (!parsedJob ? "Submit Job Description" : "")}
              </span>
              <span className="text-slate-500">
                {canProceed
                  ? "Both documents verified. Next: Exact Keyword, BM25 & Local BGE Embedding Matching."
                  : "Please complete both cards above to activate matching."}
              </span>
            </div>
          </div>

          <button
            onClick={handleStartAnalysis}
            disabled={!canProceed || isStartingAnalysis}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-3.5 rounded-xl text-sm font-bold text-white bg-emerald-600 hover:bg-emerald-700 disabled:opacity-40 disabled:pointer-events-none shadow-md shadow-emerald-600/20 active:scale-[0.98] transition-all"
          >
            <Zap className="w-4 h-4" />
            <span>{isStartingAnalysis ? "Initializing Agents..." : "Run ATS Matching Analysis"}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        {/* Privacy Callout */}
        <div className="text-center text-xs text-slate-500 flex items-center justify-center gap-2 pt-2">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>Your resume is processed in ephemeral memory and automatically purged after 24 hours.</span>
        </div>
      </div>
    </div>
  );
}
