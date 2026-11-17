"use client";

import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { ScoreBreakdown } from "@/services/api";

interface CategoryBreakdownChartProps {
  scores: ScoreBreakdown;
}

export default function CategoryBreakdownChart({ scores }: CategoryBreakdownChartProps) {
  const data = [
    { name: "Keyword Match (40%)", score: scores.keyword, fill: "#047857" }, // emerald-700
    { name: "Semantic Relevance (25%)", score: scores.semantic, fill: "#059669" }, // emerald-600
    { name: "Experience Tenure (20%)", score: scores.experience, fill: "#10b981" }, // emerald-500
    { name: "Project Evidence (10%)", score: scores.project, fill: "#34d399" }, // emerald-400
    { name: "Education Match (5%)", score: scores.education, fill: "#0d9488" }, // teal-600
  ];

  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 10, right: 25, left: 20, bottom: 5 }}
        >
          <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 11, fill: "#64748b" }} />
          <YAxis
            type="category"
            dataKey="name"
            tick={{ fontSize: 11, fill: "#1e293b", fontWeight: 500 }}
            width={160}
          />
          <Tooltip
            formatter={(value: any) => [`${value}%`, "Score"]}
            contentStyle={{
              borderRadius: "10px",
              border: "1px solid #d1fae5",
              boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.05)",
              fontSize: "12px",
              backgroundColor: "#ffffff",
            }}
          />
          <Bar dataKey="score" radius={[0, 6, 6, 0]} barSize={18}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.fill} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
