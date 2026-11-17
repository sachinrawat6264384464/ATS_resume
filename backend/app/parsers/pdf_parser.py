import fitz  # PyMuPDF
import os
import re
from typing import Dict, Any, List, Tuple


class PDFParser:
    """Extracts text, section boundaries, and layout details from PDF resumes."""

    @staticmethod
    def extract(file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            doc = fitz.open(file_path)
        except Exception as e:
            raise ValueError(f"Could not read PDF file: {str(e)}")

        if doc.is_encrypted:
            try:
                # Attempt empty password decrypt
                if not doc.authenticate(""):
                    raise ValueError("PDF is encrypted and password-protected.")
            except Exception:
                raise ValueError("PDF is encrypted and password-protected.")

        num_pages = len(doc)
        full_text_list: List[str] = []
        page_texts: List[Dict[str, Any]] = []
        all_blocks: List[Dict[str, Any]] = []

        is_two_column_suspected = False

        for page_idx in range(num_pages):
            page = doc[page_idx]
            page_text = page.get_text("text")
            full_text_list.append(page_text)

            # Extract detailed text blocks with coordinates to detect layout
            text_instances = page.get_text("blocks")  # (x0, y0, x1, y1, text, block_no, block_type)
            page_width = page.rect.width

            left_column_blocks = 0
            right_column_blocks = 0

            for b in text_instances:
                if len(b) >= 5 and b[4].strip():
                    x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4]
                    block_info = {
                        "page": page_idx + 1,
                        "bbox": [x0, y0, x1, y1],
                        "text": text.strip()
                    }
                    all_blocks.append(block_info)

                    # Check horizontal distribution
                    if x1 < page_width * 0.55:
                        left_column_blocks += 1
                    elif x0 > page_width * 0.45:
                        right_column_blocks += 1

            if left_column_blocks >= 3 and right_column_blocks >= 3:
                is_two_column_suspected = True

            page_texts.append({
                "page": page_idx + 1,
                "text": page_text
            })

        raw_text = "\n".join(full_text_list).strip()
        doc.close()

        # If text is nearly empty, it might be scanned/image-only
        is_scanned = len(raw_text.replace("\n", "").replace(" ", "")) < 60

        return {
            "raw_text": raw_text,
            "page_count": num_pages,
            "page_texts": page_texts,
            "blocks": all_blocks,
            "is_two_column": is_two_column_suspected,
            "is_scanned": is_scanned,
            "warnings": ["Document appears to be scanned image with little extractable text."] if is_scanned else []
        }
