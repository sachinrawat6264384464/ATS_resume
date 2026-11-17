"use client";

import React from "react";

interface ScoreGaugeProps {
  score: number;
  rating?: string;
  size?: number;
}

export default function ScoreGauge({
  score,
  rating = "Evaluated",
  size = 180,
}: ScoreGaugeProps) {
  const strokeWidth = 14;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (Math.min(100, Math.max(0, score)) / 100) * circumference;

  const getColor = (s: number) => {
    if (s >= 75) return "#059669"; // emerald-600
    if (s >= 55) return "#10b981"; // emerald-500
    return "#e11d48"; // rose-600
  };

  const color = getColor(score);

  return (
    <div className="flex flex-col items-center justify-center text-center">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="rotate-[-90deg]">
          {/* Background Circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#f1f5f9"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          {/* Animated Progress Circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={color}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Inner Score Text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
          <span className="text-4xl font-black text-slate-900 tracking-tight">
            {Math.round(score)}
          </span>
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
            out of 100
          </span>
        </div>
      </div>

      <div className="mt-3">
        <span
          className="inline-block px-3 py-1 text-xs font-bold rounded-full border"
          style={{
            backgroundColor: `${color}15`,
            color: color,
            borderColor: `${color}30`,
          }}
        >
          {rating}
        </span>
      </div>
    </div>
  );
}
