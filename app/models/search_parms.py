from pydantic import BaseModel

class SearchParams(BaseModel):
    query: str
    category: str
    page: int  | None = None   
