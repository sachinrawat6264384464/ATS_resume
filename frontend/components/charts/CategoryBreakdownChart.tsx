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
    { name: "Keyword Match (40%)", score: scores.keyword, fill: "#2563eb" },
    { name: "Semantic Relevance (25%)", score: scores.semantic, fill: "#4f46e5" },
    { name: "Experience Tenure (20%)", score: scores.experience, fill: "#059669" },
    { name: "Project Evidence (10%)", score: scores.project, fill: "#d97706" },
    { name: "Education Match (5%)", score: scores.education, fill: "#7c3aed" },
  ];

  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 10, right: 25, left: 20, bottom: 5 }}
        >
          <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 11 }} />
          <YAxis
            type="category"
            dataKey="name"
            tick={{ fontSize: 11, fill: "#334155" }}
            width={160}
          />
          <Tooltip
            formatter={(value: any) => [`${value}%`, "Score"]}
            contentStyle={{
              borderRadius: "8px",
              border: "1px solid #e2e8f0",
              fontSize: "12px",
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

