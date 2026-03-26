from pydantic import BaseModel, EmailStr

class NewsletterCreate(BaseModel):
    email: EmailStr  # This automatically validates the email format