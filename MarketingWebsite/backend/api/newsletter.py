from fastapi import APIRouter, HTTPException
from schemas.newsletter import NewsletterCreate
from services.newsletter_service import save_subscriber

router = APIRouter(prefix="/newsletter", tags=["newsletter"])

@router.post("/subscribe")
async def subscribe_to_newsletter(data: NewsletterCreate):
    result = save_subscriber(data.email)
    
    if result["status"] == "already_exists":
        raise HTTPException(status_code=400, detail="Email already subscribed")
    
    return {"message": "Successfully subscribed to Breezi newsletter!"}