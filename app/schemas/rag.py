from pydantic import BaseModel

class DocumentRequest(BaseModel):
    content: str

class QueryRequest(BaseModel):
    query: str
