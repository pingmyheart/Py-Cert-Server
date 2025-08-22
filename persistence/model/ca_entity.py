from pydantic import BaseModel


class CAEntity(BaseModel):
    ca_id: str
    domain: str
    crt: str
    key: str
