from pydantic import BaseModel


class HomeResponse(BaseModel):
    message: str
    status: str
    version: str
    timestamp: str
    docs_url: str
