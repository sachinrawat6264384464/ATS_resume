import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from typing import Dict, Any


class PDFReportGenerator:
    """Generates an audit-ready, beautifully formatted PDF report for an ATS analysis."""

    @classmethod
    def generate(cls, analysis_data: Dict[str, Any]) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()

        # Custom typography styles
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=4
        )
        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#64748b")
        )
        section_heading = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#1e293b"),
            spaceBefore=12,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#334155")
        )
        bold_body = ParagraphStyle(
            "BoldBody",
            parent=body_style,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#0f172a")
        )

        story = []

        # 1. Header Banner
        candidate_name = analysis_data.get("candidate_name") or "Candidate"
        job_title = analysis_data.get("job_title") or "Target Role"
        scores = analysis_data.get("scores", {})
        overall_score = scores.get("overall", 0.0)

        story.append(Paragraph("ResumeIQ &mdash; ATS Audit & Intelligence Report", title_style))
        story.append(Paragraph(f"Candidate: <b>{candidate_name}</b> &nbsp;|&nbsp; Target Role: <b>{job_title}</b> &nbsp;|&nbsp; Scoring Engine: {analysis_data.get('scoring_version', 'v1.0.0')}", subtitle_style))
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=12))

        # 2. Executive Score Summary Box
        score_badge_text = "Exceptional Match" if overall_score >= 85 else ("Strong Match" if overall_score >= 70 else ("Moderate Match" if overall_score >= 55 else "Low Alignment"))
        score_color = "#16a34a" if overall_score >= 70 else ("#d97706" if overall_score >= 55 else "#dc2626")

        summary_data = [
            [
                Paragraph("<b>Overall ATS Score:</b>", body_style),
                Paragraph(f"<font color='{score_color}' size='16'><b>{overall_score} / 100</b></font> ({score_badge_text})", body_style),
                Paragraph("<b>Evaluation Method:</b>", body_style),
                Paragraph("Deterministic Multi-Agent NLP & Embeddings", body_style)
            ]
        ]
        summary_table = Table(summary_data, colWidths=[120, 160, 110, 140])
        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("PADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 12))

        # 3. Score Breakdown Table
        story.append(Paragraph("1. Calibrated Component Breakdown", section_heading))
        breakdown_data = [
            ["Evaluation Component", "Weight", "Score", "Mathematical Contribution"],
            ["Keyword & Taxonomy Match", "40%", f"{scores.get('keyword', 0)}%", f"{round(scores.get('keyword', 0) * 0.40, 1)} pts"],
            ["Semantic Relevance (BGE-small)", "25%", f"{scores.get('semantic', 0)}%", f"{round(scores.get('semantic', 0) * 0.25, 1)} pts"],
            ["Chronological Experience Match", "20%", f"{scores.get('experience', 0)}%", f"{round(scores.get('experience', 0) * 0.20, 1)} pts"],
            ["Technical Project Evidence", "10%", f"{scores.get('project', 0)}%", f"{round(scores.get('project', 0) * 0.10, 1)} pts"],
            ["Education & Degrees Prerequisite", "5%", f"{scores.get('education', 0)}%", f"{round(scores.get('education', 0) * 0.05, 1)} pts"],
            ["Total Calibrated ATS Score", "100%", "-", f"{overall_score} / 100"]
        ]
        breakdown_table = Table(breakdown_data, colWidths=[180, 70, 110, 170])
        breakdown_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ("TOPPADDING", (0, 0), (-1, 0), 6),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#f1f5f9")),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("PADDING", (0, 1), (-1, -1), 5),
            ("FONTSIZE", (0, 1), (-1, -1), 8.5)
        ]))
        story.append(breakdown_table)
        story.append(Spacer(1, 10))

        # 4. Mandatory Gaps (if any)
        missing_mandatory = analysis_data.get("missing_mandatory", [])
        if missing_mandatory:
            story.append(Paragraph("2. Critical Missing Mandatory Requirements", section_heading))
            gap_data = [["Missing Prerequisite", "Audit Impact"]]
            for m in missing_mandatory[:6]:
                gap_data.append([
                    m,
                    "Explicitly requested as minimum qualification in JD. High risk of ATS rejection."
                ])
            gap_table = Table(gap_data, colWidths=[160, 370])
            gap_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#be123c")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#fecdd3")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#fff1f2")),
                ("PADDING", (0, 0), (-1, -1), 5),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5)
            ]))
            story.append(gap_table)
            story.append(Spacer(1, 10))

        # 5. Verified Skills with Provenance Spans
        story.append(Paragraph("3. Verified Matched Skills with Evidence", section_heading))
        matched = analysis_data.get("matched_skills", [])
        if matched:
            match_rows = [["Canonical Skill", "Category", "Evidence Level", "Provenance"]]
            for item in matched[:10]:
                match_rows.append([
                    item.get("canonical", ""),
                    item.get("category", ""),
                    item.get("evidence_level", "verified").replace("_", " ").title(),
                    (item.get("provenance") or item.get("evidence") or "")[:70]
                ])
            match_table = Table(match_rows, colWidths=[110, 110, 120, 190])
            match_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f766e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ccfbf1")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f0fdfa")),
                ("PADDING", (0, 0), (-1, -1), 5),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5)
            ]))
            story.append(match_table)
            story.append(Spacer(1, 10))

        # 6. Actionable Resume Improvement Recommendations
        recs = analysis_data.get("recommendations", [])
        if recs:
            story.append(Paragraph("4. Actionable Bullet Point Enhancements", section_heading))
            rec_rows = [["Priority", "Type", "Recommendation / Suggested Fix"]]
            for r in recs[:5]:
                suggested = r.get("suggested_text") or r.get("reasoning", "")
                rec_rows.append([
                    r.get("priority", "medium").upper(),
                    r.get("category", "bullet").title(),
                    suggested[:100] + ("..." if len(suggested) > 100 else "")
                ])
            rec_table = Table(rec_rows, colWidths=[70, 90, 370])
            rec_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4338ca")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e0e7ff")),
                ("PADDING", (0, 0), (-1, -1), 5),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5)
            ]))
            story.append(rec_table)

        # Footer disclaimer
        story.append(Spacer(1, 16))
        story.append(Paragraph(
            "<b>Disclaimer:</b> This report is generated by ResumeIQ using deterministic NLP, canonical skill taxonomies, and local BGE-small embeddings. It does not represent proprietary corporate ATS software or guarantee hiring selection.",
            subtitle_style
        ))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
