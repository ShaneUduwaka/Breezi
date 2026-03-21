from pydantic import BaseModel, EmailStr

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    company: str
    message: str

class ContactResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    company: str
    message: str
    timestamp: str
