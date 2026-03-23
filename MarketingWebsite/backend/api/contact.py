from fastapi import APIRouter
from schemas.contact import ContactCreate, ContactResponse
from services import contact_service

router = APIRouter(
    prefix="/contact",
    tags=["Contact Us"]
)

@router.post("/", response_model=ContactResponse, status_code=201)
def submit_contact_form(contact: ContactCreate):
    """
    Endpoint to receive contact us form submissions.
    """
    saved_contact = contact_service.save_contact_submission(contact)
    return saved_contact
