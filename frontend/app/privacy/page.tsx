import { ShieldCheck, Lock, Trash2, EyeOff } from "lucide-react";
import Link from "next/link";

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-slate-50/70 py-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        <div className="space-y-4 border-b border-emerald-100 pb-8">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold shadow-xs">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>Zero-Knowledge Privacy Policy</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900">Privacy & Data Protection</h1>
          <p className="text-slate-600 text-base">
            ResumeIQ is designed from the ground up to respect candidate privacy. We do not require accounts, we do not monetize your data, and we do not train models on your resumes.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-5 bg-white rounded-2xl border border-emerald-100 space-y-2 shadow-sm">
            <EyeOff className="w-6 h-6 text-emerald-600" />
            <h3 className="font-bold text-slate-900">No User Accounts</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              No signup, login, or tracking cookies. Your sessions are fully anonymous.
            </p>
          </div>

          <div className="p-5 bg-white rounded-2xl border border-emerald-100 space-y-2 shadow-sm">
            <Trash2 className="w-6 h-6 text-emerald-600" />
            <h3 className="font-bold text-slate-900">24-Hour Auto-Purge</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Uploaded resumes and temporary processing artifacts are automatically expired and deleted.
            </p>
          </div>

          <div className="p-5 bg-white rounded-2xl border border-emerald-100 space-y-2 shadow-sm">
            <Lock className="w-6 h-6 text-emerald-600" />
            <h3 className="font-bold text-slate-900">No Third-Party Sharing</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Resume content is analyzed with local Python algorithms, never sent to external LLMs.
            </p>
          </div>
        </div>

        <div className="prose prose-slate max-w-none space-y-6 text-sm text-slate-600 leading-relaxed">
          <h2 className="text-lg font-bold text-slate-900">1. Information We Process</h2>
          <p>
            When you upload a resume or paste a job description, that data is processed solely for the purpose of computing
            ATS matching scores, extracting skill matrices, and producing evidence spans. No biometric or sensitive government identifiers are stored.
          </p>

          <h2 className="text-lg font-bold text-slate-900">2. File Security</h2>
          <p>
            Uploaded documents are sanitized, checked for MIME integrity, and stored with unguessable UUIDs in protected local directories.
            Executables and macros are strictly rejected.
          </p>

          <h2 className="text-lg font-bold text-slate-900">3. Deletion Rights</h2>
          <p>
            You may delete any analysis report immediately from the analysis dashboard. Furthermore, scheduled retention policies continuously
            purge files older than 24 hours.
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
