from backend.app.models.detection_result import DetectionResult
from backend.app.models.network_request import NetworkRequest


def analyze_request(request: NetworkRequest) -> DetectionResult:
    """Analyze a network request using basic security rules."""

    suspicious_domains = {
        "malware.test",
        "phishing.test",
        "suspicious.test",
    }

    if request.domain.lower() in suspicious_domains:
        return DetectionResult(
            result_id=f"det-{request.request_id}",
            request_id=request.request_id,
            is_malicious=True,
            confidence=0.95,
            threat_type="suspicious_domain",
            explanation="The request targets a domain classified as suspicious.",
        )

    return DetectionResult(
        result_id=f"det-{request.request_id}",
        request_id=request.request_id,
        is_malicious=False,
        confidence=0.10,
        threat_type="none",
        explanation="No suspicious indicators were detected by the current rules.",
    )