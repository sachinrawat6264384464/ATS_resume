import docx
import os
from typing import Dict, Any, List


class DocxParser:
    """Extracts text, tables, and section hierarchies from Microsoft Word (DOCX) files."""

    @staticmethod
    def extract(file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            doc = docx.Document(file_path)
        except Exception as e:
            raise ValueError(f"Could not read DOCX document: {str(e)}")

        paragraphs_text: List[str] = []
        structured_items: List[Dict[str, Any]] = []

        # Extract regular paragraphs
        for p in doc.paragraphs:
            text = p.text.strip()
            if text:
                paragraphs_text.append(text)
                is_heading = p.style.name.startswith("Heading") or (
                    len(text) < 40 and not text.endswith(".") and p.runs and p.runs[0].bold
                )
                structured_items.append({
                    "type": "heading" if is_heading else "paragraph",
                    "style": p.style.name,
                    "text": text
                })

        # Extract tables if present
        table_texts: List[str] = []
        for table in doc.tables:
            for row in table.rows:
                row_cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_cells:
                    # Deduplicate repeated merged cell values
                    unique_cells = []
                    for c in row_cells:
                        if not unique_cells or c != unique_cells[-1]:
                            unique_cells.append(c)
                    row_str = " | ".join(unique_cells)
                    table_texts.append(row_str)
                    structured_items.append({
                        "type": "table_row",
                        "text": row_str
                    })

        all_text_lines = paragraphs_text + table_texts
        raw_text = "\n".join(all_text_lines).strip()

        is_empty = len(raw_text.replace("\n", "").replace(" ", "")) < 30

        return {
            "raw_text": raw_text,
            "structured_items": structured_items,
            "paragraph_count": len(paragraphs_text),
            "table_count": len(doc.tables),
            "is_empty": is_empty,
            "warnings": ["DOCX document has very little extractable text."] if is_empty else []
        }

