from pydantic import BaseModel

class HelloResponse(BaseModel):
    message: str
    id: str
    title: str
    desc: str
