import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000/api/v1";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface ContactInfo {
  name?: string;
  email?: string;
  phone?: string;
  location?: string;
  linkedin?: string;
  github?: string;
  portfolio?: string;
}

export interface WorkExperienceItem {
  title?: string;
  company?: string;
  location?: string;
  start_date?: string;
  end_date?: string;
  is_current: boolean;
  duration_months: number;
  description: string[];
  technologies: string[];
}

export interface EducationItem {
  degree?: string;
  field_of_study?: string;
  institution?: string;
  graduation_year?: string;
  gpa?: string;
}

export interface ProjectItem {
  title?: string;
  description: string[];
  technologies: string[];
  link?: string;
}

export interface ParsedResume {
  id: string;
  resume_id: string;
  contact_info: ContactInfo;
  summary?: string;
  skills: string[];
  work_experience: WorkExperienceItem[];
  education: EducationItem[];
  projects: ProjectItem[];
  certifications: string[];
  achievements: string[];
  languages: string[];
  technical_tools: string[];
  extraction_confidence: number;
  warnings: string[];
}

export interface ResumeUploadResponse {
  id: string;
  filename: string;
  file_type: string;
  file_size: number;
  created_at: string;
  message: string;
  parsed_data?: ParsedResume;
}

export interface JobExtractedData {
  title?: string;
  company?: string;
  required_skills: string[];
  preferred_skills: string[];
  experience_years_required: number;
  education_required: string[];
  responsibilities: string[];
  qualifications: string[];
  technical_tools: string[];
}

export interface JobDescriptionResponse {
  id: string;
  title?: string;
  company?: string;
  raw_text: string;
  extracted_data: JobExtractedData;
  created_at: string;
}

export interface ScoreBreakdown {
  overall: number;
  keyword: number;
  semantic: number;
  experience: number;
  project: number;
  education: number;
  weights: Record<string, number>;
  rating?: string;
}

export interface MatchedSkill {
  canonical: string;
  category: string;
  found_in_resume: string;
  is_mandatory?: boolean;
  confidence: number;
  evidence?: string;
  evidence_level?: string;
  provenance?: string;
  snippet?: string;
}

export interface MissingSkill {
  canonical: string;
  category: string;
  is_mandatory?: boolean;
  context?: string;
}

export interface RelatedSkill {
  required: string;
  candidate_possesses: string;
  category: string;
  relevance_note: string;
}

export interface Recommendation {
  id: string;
  category: string;
  priority: string;
  original_text?: string;
  suggested_text?: string;
  reasoning: string;
}

export interface AnalysisStatusResponse {
  analysis_id: string;
  status: string;
  progress_percentage: number;
  stage: string;
  message?: string;
  error?: string;
}

export interface AnalysisReport {
  analysis_id: string;
  resume_id: string;
  job_id: string;
  status: string;
  candidate_name?: string;
  job_title?: string;
  scores: ScoreBreakdown;
  matched_skills: MatchedSkill[];
  missing_skills: MissingSkill[];
  missing_mandatory: string[];
  related_skills: RelatedSkill[];
  experience_analysis: Record<string, any>;
  recommendations: Recommendation[];
  scoring_version: string;
  created_at: string;
  completed_at?: string;
}

export const resumeApi = {
  uploadResume: async (file: File): Promise<ResumeUploadResponse> => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await apiClient.post<ResumeUploadResponse>("/resumes/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return res.data;
  },

  getResume: async (resumeId: string): Promise<ResumeUploadResponse> => {
    const res = await apiClient.get<ResumeUploadResponse>(`/resumes/${resumeId}`);
    return res.data;
  },

  deleteResume: async (resumeId: string): Promise<void> => {
    await apiClient.delete(`/resumes/${resumeId}`);
  },
};

export const jobApi = {
  createJob: async (raw_text: string, title?: string, company?: string): Promise<JobDescriptionResponse> => {
    const res = await apiClient.post<JobDescriptionResponse>("/jobs", {
      raw_text,
      title,
      company,
    });
    return res.data;
  },

  getJob: async (jobId: string): Promise<JobDescriptionResponse> => {
    const res = await apiClient.get<JobDescriptionResponse>(`/jobs/${jobId}`);
    return res.data;
  },

  updateJob: async (jobId: string, data: JobExtractedData): Promise<JobDescriptionResponse> => {
    const res = await apiClient.put<JobDescriptionResponse>(`/jobs/${jobId}`, data);
    return res.data;
  },
};

export const analysisApi = {
  createAnalysis: async (resume_id: string, job_id: string): Promise<AnalysisStatusResponse> => {
    const res = await apiClient.post<AnalysisStatusResponse>("/analysis", {
      resume_id,
      job_id,
    });
    return res.data;
  },

  getStatus: async (analysisId: string): Promise<AnalysisStatusResponse> => {
    const res = await apiClient.get<AnalysisStatusResponse>(`/analysis/${analysisId}/status`);
    return res.data;
  },

  getReport: async (analysisId: string): Promise<AnalysisReport> => {
    const res = await apiClient.get<AnalysisReport>(`/analysis/${analysisId}/report`);
    return res.data;
  },

  deleteAnalysis: async (analysisId: string): Promise<void> => {
    await apiClient.delete(`/analysis/${analysisId}`);
  },
};
