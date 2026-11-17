import pytest
import io
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import sanitize_text, validate_file_content
from app.core.redis_client import ResilientCache
from app.core.middleware import InMemoryRateLimiter


client = TestClient(app)


def test_sanitize_text():
    # Null bytes
    malicious_null = "Hello\x00World"
    assert sanitize_text(malicious_null) == "HelloWorld"

    # Script tag injection
    malicious_script = "Software Engineer <script>alert('xss')</script> at Google"
    assert sanitize_text(malicious_script) == "Software Engineer  at Google"

    # Iframe injection
    malicious_iframe = "Profile: <iframe src='http://evil.com'></iframe>"
    assert sanitize_text(malicious_iframe) == "Profile:"

    # Normal text preservation
    normal_text = "5+ years of Python, Docker, and Kubernetes experience."
    assert sanitize_text(normal_text) == normal_text


def test_validate_file_content_rejections():
    # Disallowed extension
    with pytest.raises(Exception) as exc:
        validate_file_content("script.py", b"print('hello')")
    assert "Unsupported file format" in str(exc.value.detail)

    # Empty file
    with pytest.raises(Exception) as exc:
        validate_file_content("resume.pdf", b"")
    assert "too small" in str(exc.value.detail)

    # Corrupt PDF header
    with pytest.raises(Exception) as exc:
        validate_file_content("resume.pdf", b"NOT_A_REAL_PDF_HEADER_JUST_RANDOM_TEXT_HERE")
    assert "Header signature does not match" in str(exc.value.detail)

    # Corrupt DOCX (not a zip)
    with pytest.raises(Exception) as exc:
        validate_file_content("resume.docx", b"NOT_A_ZIP_ARCHIVE_HEADER_CORRUPTED_FILE")
    assert "File is not a valid OpenXML ZIP archive" in str(exc.value.detail)


def test_validate_file_content_valid_pdf():
    valid_pdf_bytes = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF"
    res = validate_file_content("my_resume.pdf", valid_pdf_bytes)
    assert res == "pdf"


def test_security_headers_middleware():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.headers.get("x-content-type-options") == "nosniff"
    assert response.headers.get("x-frame-options") == "DENY"
    assert "1; mode=block" in response.headers.get("x-xss-protection", "")


def test_rate_limiter_logic():
    limiter = InMemoryRateLimiter(limit_per_minute=3)
    test_ip = "192.168.1.100"

    assert limiter.is_allowed(test_ip) is True
    assert limiter.is_allowed(test_ip) is True
    assert limiter.is_allowed(test_ip) is True
    # 4th request exceeds limit of 3
    assert limiter.is_allowed(test_ip) is False


def test_resilient_cache_in_memory_fallback():
    # Instantiate with an unreachable port
    cache = ResilientCache("redis://127.0.0.1:9999/0")
    assert cache.is_redis_available is False

    # Setting and getting should work seamlessly in-memory
    assert cache.set("test_key", "test_value", expire_seconds=60) is True
    assert cache.get("test_key") == "test_value"

    # Delete
    assert cache.delete("test_key") is True
    assert cache.get("test_key") is None


def test_upload_corrupt_pdf_api_rejection():
    corrupt_bytes = b"Corrupted file payload with .pdf extension"
    files = {"file": ("fake_resume.pdf", corrupt_bytes, "application/pdf")}
    response = client.post("/api/v1/resumes/upload", files=files)
    assert response.status_code == 400
    assert "Header signature does not match" in response.json()["detail"]


def test_job_description_short_text_rejection():
    # Pydantic schema validation enforces min_length=20, rejecting with 422
    response = client.post("/api/v1/jobs", json={"title": "Dev", "company": "Co", "raw_text": "Too short"})
    assert response.status_code in [400, 422]
