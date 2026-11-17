# ResumeIQ — Security & Privacy Architecture

## 1. Threat Model & Mitigation Matrix

| Threat Vector | Potential Impact | ResumeIQ Mitigation Mechanism |
|---|---|---|
| **Malicious Executable Upload** | Arbitrary code execution (.exe, .sh, .bat disguised as .pdf) | Strict extension check + magic byte verification (`%PDF-` and OpenXML zip signature) + no execute permissions in `/uploads`. |
| **ZIP Bomb / XML Entity Expansion** | Denial of Service via resource exhaustion | Maximum 10MB payload limit + selective file extraction without recursive zip resolution. |
| **Stored XSS Injection** | Script execution in reviewer browser via resume content | Regex sanitization neutralizing `<script>`, `<iframe>`, and `javascript:` protocols before database storage or client rendering. |
| **API Flooding / Scraping** | System denial of service | IP-based sliding-window rate limiting middleware (60 requests/minute) returning HTTP 429 with `Retry-After`. |
| **Data Breach / Credential Leak** | Candidate credential compromise | Zero-Auth architecture: no passwords, emails, or user accounts are stored for authentication. |
| **Privacy / PII Exposure** | Candidate resume data retention | All resumes can be purged via `DELETE /api/v1/resumes/{id}`. Local storage is ephemeral and isolated. |

---

## 2. Magic Byte & Document Verification

Uploaded files undergo deep payload inspection before touching any parser or persistent disk location:

```python
PDF_MAGIC = b"%PDF-"
DOCX_ZIP_MAGIC = b"PK\x03\x04"
```

1. **PDF Files**: The first 5 bytes must strictly equal `%PDF-`.
2. **DOCX Files**: The first 4 bytes must match the PKZIP header signature `PK\x03\x04`, and the archive structure must contain the standard OpenXML entry `word/document.xml`. Files failing this check are rejected with HTTP 400.

---

## 3. Untrusted Text Sanitization

Extracted raw text from resume documents and job descriptions is scrubbed to prevent stored cross-site scripting and parser disruption:

```python
def sanitize_text(text: str) -> str:
    cleaned = text.replace("\x00", "")  # Strip null bytes
    cleaned = re.sub(r"<\s*script[^>]*>.*?<\s*/\s*script\s*>", "", cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"<\s*iframe[^>]*>.*?<\s*/\s*iframe\s*>", "", cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"javascript\s*:", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()
```

---

## 4. HTTP Security Headers

All HTTP responses served by the backend include standard protective headers:

```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

---

## 5. Rate Limiting

The `RateLimitMiddleware` maintains a per-IP sliding window tracking request timestamps:
- Window size: 60 seconds
- Max allowed: 60 requests
- Response upon breach: HTTP 429 Too Many Requests with header `Retry-After: 60`.

