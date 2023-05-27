from pydantic import BaseModel

class IssueRequest(BaseModel):
    isbn:str
    
class IssueUpdate(IssueRequest):
    status:str
    
    
    