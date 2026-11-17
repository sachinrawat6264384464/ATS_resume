"use client";

import React, { useState } from "react";
import {
  Briefcase,
  Sparkles,
  Plus,
  X,
  Edit2,
  Check,
  Loader2,
  AlertCircle,
  FileCheck2,
} from "lucide-react";
import { jobApi, JobDescriptionResponse, JobExtractedData } from "@/services/api";

interface JobDescriptionInputProps {
  onJobParsed: (jobData: JobDescriptionResponse) => void;
  onClear: () => void;
  parsedJob: JobDescriptionResponse | null;
}

const SAMPLE_JD = `Senior Full Stack Software Engineer
Datadog Inc. - New York, NY

About the Role:
We are seeking a Senior Full Stack Software Engineer to build scalable real-time observability platforms and cloud-native dashboard tools.

Key Responsibilities:
- Design and develop robust backend APIs using Python (FastAPI/Django) and Go.
- Architect high-throughput data processing pipelines leveraging PostgreSQL, Redis, and Kafka.
- Build clean, reactive frontends in TypeScript, React, and Next.js.
- Ensure end-to-end security, observability, and containerized deployment via Docker and Kubernetes.

Minimum Qualifications:
- 4+ years of professional software engineering experience.
- Strong proficiency in Python, TypeScript, and modern relational databases (PostgreSQL).
- Experience designing RESTful and GraphQL APIs.
- Bachelor's degree in Computer Science, Software Engineering, or related field.

Preferred Qualifications:
- Experience with AWS or GCP cloud infrastructure.
- Familiarity with CI/CD automation, Terraform, and microservices architecture.
- Real-time caching strategies with Redis or vector databases.`;

export default function JobDescriptionInput({
  onJobParsed,
  onClear,
  parsedJob,
}: JobDescriptionInputProps) {
  const [rawText, setRawText] = useState("");
  const [jobTitle, setJobTitle] = useState("");
  const [company, setCompany] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Skill editing state
  const [newRequiredSkill, setNewRequiredSkill] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [editableData, setEditableData] = useState<JobExtractedData | null>(null);

  const handleParseJob = async () => {
    if (!rawText.trim() || rawText.trim().length < 20) {
      setErrorMessage("Please paste a valid job description with at least 20 characters.");
      return;
    }

    setErrorMessage(null);
    setIsLoading(true);

    try {
      const data = await jobApi.createJob(rawText, jobTitle || undefined, company || undefined);
      onJobParsed(data);
      setEditableData(data.extracted_data);
    } catch (err: any) {
      setErrorMessage(err.response?.data?.detail || "Failed to analyze job description.");
    } finally {
      setIsLoading(false);
    }
  };

  const loadSample = () => {
    setRawText(SAMPLE_JD);
    setJobTitle("Senior Full Stack Software Engineer");
    setCompany("Datadog");
  };

  const handleAddSkill = () => {
    if (!newRequiredSkill.trim() || !editableData) return;
    const updated = {
      ...editableData,
      required_skills: [...editableData.required_skills, newRequiredSkill.trim()],
    };
    setEditableData(updated);
    setNewRequiredSkill("");
  };

  const handleRemoveSkill = (skillToRemove: string) => {
    if (!editableData) return;
    const updated = {
      ...editableData,
      required_skills: editableData.required_skills.filter((s) => s !== skillToRemove),
    };
    setEditableData(updated);
  };

  const handleSaveEdits = async () => {
    if (!parsedJob || !editableData) return;
    setIsLoading(true);
    try {
      const updated = await jobApi.updateJob(parsedJob.id, editableData);
      onJobParsed(updated);
      setIsEditing(false);
    } catch (err: any) {
      setErrorMessage("Failed to save changes to job description.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-emerald-100 p-6 shadow-sm space-y-5">
      <div className="flex items-center justify-between pb-3 border-b border-slate-100">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 flex items-center justify-center font-bold text-sm">
            2
          </div>
          <div>
            <h3 className="font-bold text-slate-900 text-base">Job Description (JD)</h3>
            <p className="text-xs text-slate-500">Paste job requirements or load sample</p>
          </div>
        </div>

        {parsedJob ? (
          <button
            onClick={() => {
              onClear();
              setRawText("");
              setEditableData(null);
            }}
            className="text-xs text-rose-600 hover:text-rose-700 font-semibold flex items-center gap-1 px-2.5 py-1 rounded-md hover:bg-rose-50 transition-colors"
          >
            <X className="w-3.5 h-3.5" />
            <span>Reset JD</span>
          </button>
        ) : (
          <button
            onClick={loadSample}
            className="text-xs text-emerald-700 hover:text-emerald-800 font-semibold flex items-center gap-1 px-2.5 py-1 rounded-md hover:bg-emerald-50 transition-colors"
          >
            <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
            <span>Load Sample JD</span>
          </button>
        )}
      </div>

      {errorMessage && (
        <div className="p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-start gap-2.5">
          <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-rose-600" />
          <span>{errorMessage}</span>
        </div>
      )}

      {!parsedJob ? (
        <div className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Target Role / Title (Optional)
              </label>
              <input
                type="text"
                placeholder="e.g. Senior Software Engineer"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Company Name (Optional)
              </label>
              <input
                type="text"
                placeholder="e.g. Datadog, Stripe, Meta"
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Job Description Content *
            </label>
            <textarea
              rows={8}
              value={rawText}
              onChange={(e) => setRawText(e.target.value)}
              placeholder="Paste full job description, qualifications, and requirements here..."
              className="w-full p-3.5 text-xs text-slate-800 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 font-mono leading-relaxed"
            />
          </div>

          <button
            onClick={handleParseJob}
            disabled={isLoading || !rawText.trim()}
            className="w-full py-3 px-4 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 disabled:pointer-events-none shadow-sm shadow-emerald-600/20 flex items-center justify-center gap-2 transition-all active:scale-[0.99]"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-white" />
                <span>Analyzing Job Description...</span>
              </>
            ) : (
              <>
                <FileCheck2 className="w-4 h-4 text-white" />
                <span>Extract & Verify Requirements</span>
              </>
            )}
          </button>
        </div>
      ) : (
        /* Parsed JD Review & Fine-tune Mode */
        <div className="space-y-4">
          <div className="p-4 bg-slate-50 rounded-xl border border-emerald-100 space-y-2.5">
            <div className="flex items-start justify-between">
              <div>
                <h4 className="font-bold text-slate-900 text-sm">
                  {parsedJob.title || "Job Requirements Decomposed"}
                </h4>
                {parsedJob.company && (
                  <p className="text-xs text-slate-500">{parsedJob.company}</p>
                )}
              </div>
              <button
                onClick={() => setIsEditing(!isEditing)}
                className="text-xs text-emerald-700 font-semibold hover:underline flex items-center gap-1"
              >
                <Edit2 className="w-3.5 h-3.5" />
                <span>{isEditing ? "Close Editor" : "Fine-Tune Skills"}</span>
              </button>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs pt-2 border-t border-slate-200/60">
              <div className="p-2 bg-white rounded-lg border border-slate-200/60">
                <span className="text-slate-500 block text-[10px] uppercase font-semibold">
                  Experience Prerequisite
                </span>
                <span className="font-bold text-slate-900">
                  {editableData?.experience_years_required || 0}+ Years
                </span>
              </div>
              <div className="p-2 bg-white rounded-lg border border-slate-200/60">
                <span className="text-slate-500 block text-[10px] uppercase font-semibold">
                  Required Skills Extracted
                </span>
                <span className="font-bold text-emerald-700">
                  {editableData?.required_skills.length || 0} Skills
                </span>
              </div>
            </div>
          </div>

          {/* Required Skills Tags (Editable) */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-800">
                Mandatory & Core Requirements:
              </span>
              {isEditing && (
                <span className="text-[10px] text-emerald-700">Click &times; to remove</span>
              )}
            </div>

            <div className="flex flex-wrap gap-1.5 max-h-32 overflow-y-auto pr-1">
              {editableData?.required_skills.map((skill, i) => (
                <span
                  key={i}
                  className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-medium"
                >
                  <span>{skill}</span>
                  {isEditing && (
                    <button
                      onClick={() => handleRemoveSkill(skill)}
                      className="text-emerald-700 hover:text-emerald-900 ml-0.5"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  )}
                </span>
              ))}
            </div>

            {/* Add skill input if in edit mode */}
            {isEditing && (
              <div className="flex items-center gap-2 pt-2">
                <input
                  type="text"
                  placeholder="Add missing required skill..."
                  value={newRequiredSkill}
                  onChange={(e) => setNewRequiredSkill(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleAddSkill()}
                  className="flex-1 px-3 py-1.5 text-xs rounded-lg border border-slate-300 focus:outline-none focus:border-emerald-500"
                />
                <button
                  onClick={handleAddSkill}
                  className="px-3 py-1.5 rounded-lg bg-emerald-600 text-white text-xs font-semibold flex items-center gap-1 hover:bg-emerald-700"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>Add</span>
                </button>
                <button
                  onClick={handleSaveEdits}
                  className="px-3 py-1.5 rounded-lg bg-emerald-700 text-white text-xs font-semibold flex items-center gap-1 hover:bg-emerald-800"
                >
                  <Check className="w-3.5 h-3.5" />
                  <span>Save</span>
                </button>
              </div>
            )}
          </div>

          {/* Preferred Skills */}
          {editableData?.preferred_skills && editableData.preferred_skills.length > 0 && (
            <div className="space-y-1.5 pt-1">
              <span className="text-xs font-semibold text-slate-600">Preferred / Bonus:</span>
              <div className="flex flex-wrap gap-1.5">
                {editableData.preferred_skills.map((skill, i) => (
                  <span
                    key={i}
                    className="px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 border border-slate-200 text-[11px] font-medium"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
