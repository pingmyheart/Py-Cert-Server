from pydantic import BaseModel


class CertificateEntity(BaseModel):
    certificate_id: str
    ca_id: str
    domain: str
    crt: str
    key: str
