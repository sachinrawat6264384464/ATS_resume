"use client";

import React, { useState, useRef } from "react";
import {
  UploadCloud,
  FileText,
  CheckCircle2,
  AlertCircle,
  X,
  Loader2,
  Briefcase,
  Sparkles,
  ShieldAlert,
} from "lucide-react";
import { resumeApi, ResumeUploadResponse } from "@/services/api";
import { formatBytes } from "@/lib/utils";

interface ResumeUploaderProps {
  onUploadSuccess: (resumeData: ResumeUploadResponse) => void;
  onClear: () => void;
  uploadedResume: ResumeUploadResponse | null;
}

export default function ResumeUploader({
  onUploadSuccess,
  onClear,
  uploadedResume,
}: ResumeUploaderProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  const processFile = async (file: File) => {
    setErrorMessage(null);
    const validExtensions = [".pdf", ".docx", ".doc"];
    const ext = "." + file.name.split(".").pop()?.toLowerCase();

    if (!validExtensions.includes(ext)) {
      setErrorMessage("Unsupported file format. Please upload a PDF or Word (.docx) document.");
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setErrorMessage("File exceeds 10MB limit. Please upload a smaller file.");
      return;
    }

    setIsLoading(true);
    try {
      const data = await resumeApi.uploadResume(file);
      onUploadSuccess(data);
    } catch (err: any) {
      const msg = err.response?.data?.detail || "Failed to upload and parse resume. Please ensure the file is not corrupted.";
      setErrorMessage(msg);
    } finally {
      setIsLoading(false);
    }
  };

  const parsed = uploadedResume?.parsed_data;

  return (
    <div className="bg-white rounded-2xl border border-emerald-100 p-6 shadow-sm space-y-5">
      <div className="flex items-center justify-between pb-3 border-b border-slate-100">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 flex items-center justify-center font-bold text-sm">
            1
          </div>
          <div>
            <h3 className="font-bold text-slate-900 text-base">Candidate Resume</h3>
            <p className="text-xs text-slate-500">Upload PDF or DOCX (Max 10MB)</p>
          </div>
        </div>

        {uploadedResume && (
          <button
            onClick={onClear}
            className="text-xs text-rose-600 hover:text-rose-700 font-semibold flex items-center gap-1 px-2.5 py-1 rounded-md hover:bg-rose-50 transition-colors"
          >
            <X className="w-3.5 h-3.5" />
            <span>Remove</span>
          </button>
        )}
      </div>

      {errorMessage && (
        <div className="p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-start gap-2.5">
          <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-rose-600" />
          <span>{errorMessage}</span>
        </div>
      )}

      {!uploadedResume ? (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all ${
            isDragging
              ? "border-emerald-600 bg-emerald-50/50"
              : "border-emerald-200 hover:border-emerald-400 bg-emerald-50/20"
          }`}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileInput}
            accept=".pdf,.docx,.doc"
            className="hidden"
          />

          <div className="max-w-xs mx-auto space-y-3">
            <div className="w-12 h-12 rounded-2xl bg-emerald-100/80 text-emerald-700 mx-auto flex items-center justify-center">
              {isLoading ? (
                <Loader2 className="w-6 h-6 animate-spin text-emerald-600" />
              ) : (
                <UploadCloud className="w-6 h-6" />
              )}
            </div>

            <div>
              <p className="text-sm font-semibold text-slate-800">
                {isLoading ? "Parsing document with PyMuPDF..." : "Click to upload or drag & drop"}
              </p>
              <p className="text-xs text-slate-500 mt-1">PDF or DOCX files up to 10MB</p>
            </div>

            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white border border-emerald-100 text-[11px] font-medium text-emerald-800 shadow-sm">
              <FileText className="w-3 h-3 text-emerald-600" />
              <span>Single or Multi-Column Layouts Supported</span>
            </div>
          </div>
        </div>
      ) : (
        /* Parsed Resume Preview Card */
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-slate-50 border border-emerald-100 space-y-3">
            <div className="flex items-start justify-between gap-2">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-emerald-600 text-white flex items-center justify-center font-bold text-sm shadow-sm">
                  <FileText className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="font-bold text-slate-900 text-sm">
                    {parsed?.contact_info.name || uploadedResume.filename}
                  </h4>
                  <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500 mt-0.5">
                    {parsed?.contact_info.email && <span>{parsed.contact_info.email}</span>}
                    {parsed?.contact_info.phone && <span>&bull; {parsed.contact_info.phone}</span>}
                    <span>&bull; {formatBytes(uploadedResume.file_size)}</span>
                  </div>
                </div>
              </div>

              <span className="px-2.5 py-1 text-[11px] font-bold rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200 flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                <span>Extracted</span>
              </span>
            </div>

            {/* Confidence Score Bar */}
            {parsed && (
              <div className="pt-2 border-t border-slate-200/60">
                <div className="flex justify-between items-center text-xs mb-1">
                  <span className="text-slate-600 font-medium">Extraction Confidence</span>
                  <span className="font-bold text-emerald-700">
                    {Math.round(parsed.extraction_confidence * 100)}%
                  </span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-1.5">
                  <div
                    className="bg-emerald-600 h-1.5 rounded-full"
                    style={{ width: `${Math.round(parsed.extraction_confidence * 100)}%` }}
                  />
                </div>
              </div>
            )}
          </div>

          {/* Warnings alert if any */}
          {parsed?.warnings && parsed.warnings.length > 0 && (
            <div className="p-3 bg-amber-50 rounded-xl border border-amber-200 text-amber-800 text-xs space-y-1">
              <div className="flex items-center gap-1.5 font-bold">
                <ShieldAlert className="w-3.5 h-3.5 text-amber-600" />
                <span>Parser Notes:</span>
              </div>
              <ul className="list-disc pl-5 space-y-0.5 text-amber-700">
                {parsed.warnings.map((w, idx) => (
                  <li key={idx}>{w}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Extracted Skills Chips */}
          {parsed && parsed.skills.length > 0 && (
            <div className="space-y-1.5">
              <span className="text-xs font-semibold text-slate-700 flex items-center gap-1">
                <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
                Extracted Skills ({parsed.skills.length}):
              </span>
              <div className="flex flex-wrap gap-1.5 max-h-24 overflow-y-auto pr-1">
                {parsed.skills.map((skill, i) => (
                  <span
                    key={i}
                    className="px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-medium"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Work Experience Preview */}
          {parsed && parsed.work_experience.length > 0 && (
            <div className="space-y-2 pt-2 border-t border-slate-100">
              <span className="text-xs font-semibold text-slate-700 flex items-center gap-1">
                <Briefcase className="w-3.5 h-3.5 text-emerald-600" />
                Work Experience ({parsed.work_experience.length} roles found):
              </span>
              <div className="space-y-2 max-h-36 overflow-y-auto pr-1">
                {parsed.work_experience.map((job, idx) => (
                  <div key={idx} className="p-2.5 bg-slate-50 rounded-lg text-xs border border-slate-200/60">
                    <div className="flex justify-between font-bold text-slate-800">
                      <span>{job.title || "Role"}</span>
                      <span className="text-slate-500 font-normal">
                        {job.start_date || ""} &ndash; {job.end_date || ""}
                      </span>
                    </div>
                    {job.company && <p className="text-slate-600">{job.company}</p>}
                    {job.description && job.description.length > 0 && (
                      <p className="text-slate-500 text-[11px] mt-1 line-clamp-2">
                        &bull; {job.description[0]}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
