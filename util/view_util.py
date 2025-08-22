from dto.ca_dto import GenerateCertificateAuthorityRequest
from dto.certificate_dto import GenerateCertificateRequest


def extract_ca_create_request(request) -> GenerateCertificateAuthorityRequest:
    return GenerateCertificateAuthorityRequest(
        domain=request.form.get("domain"),
        country=request.form.get("country"),
        location=request.form.get("location")
    )


def extract_certificate_create_request(request) -> GenerateCertificateRequest:
    return GenerateCertificateRequest(
        ca_id=request.form.get("ca_id"),
        domain=request.form.get("domain"),
        country=request.form.get("country"),
        location=request.form.get("location"),
        state=request.form.get("state"),
        organization=request.form.get("organization"),
        organization_unit=request.form.get("organization_unit")
    )
