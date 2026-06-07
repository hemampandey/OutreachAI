from pydantic import BaseModel

class CompanyCreate(BaseModel):
    name: str
    website: str | None = None

class CompanyResponse(BaseModel):
    id: int
    name: str
    website: str | None = None

    class Config:
        from_attributes = True

class GraphRunRequest(BaseModel):
    company_name: str
    sender_company: str = "Our Company"
    pitch_context: str