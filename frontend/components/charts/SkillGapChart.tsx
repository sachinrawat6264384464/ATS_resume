"use client";

import React from "react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";

interface SkillGapChartProps {
  matchedCount: number;
  relatedCount: number;
  missingCount: number;
}

export default function SkillGapChart({
  matchedCount,
  relatedCount,
  missingCount,
}: SkillGapChartProps) {
  const data = [
    { name: "Verified Skills", value: matchedCount, color: "#059669" },
    { name: "Related Stacks", value: relatedCount, color: "#3b82f6" },
    { name: "Skill Gaps", value: missingCount, color: "#e11d48" },
  ].filter((item) => item.value > 0);

  if (data.length === 0) {
    return (
      <div className="h-48 flex items-center justify-center text-xs text-slate-400">
        No skill data available
      </div>
    );
  }

  return (
    <div className="w-full h-56">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={50}
            outerRadius={75}
            paddingAngle={4}
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              borderRadius: "8px",
              border: "1px solid #e2e8f0",
              fontSize: "12px",
            }}
          />
          <Legend
            verticalAlign="bottom"
            height={36}
            iconType="circle"
            wrapperStyle={{ fontSize: "11px", paddingTop: "10px" }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

