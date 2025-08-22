from pydantic import BaseModel


class GenerateCertificateAuthorityRequest(BaseModel):
    domain: str
    country: str
    location: str


class GenerateCertificateAuthorityResponse(BaseModel):
    ca_id: str
    domain: str
    crt: str
