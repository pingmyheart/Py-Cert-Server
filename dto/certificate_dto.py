from pydantic import BaseModel


class GenerateCertificateRequest(BaseModel):
    ca_id: str
    domain: str
    country: str
    location: str
    state: str
    organization: str
    organization_unit: str


class GenerateCertificateResponse(BaseModel):
    certificate_id: str
    domain: str
    crt: str
    key: str
