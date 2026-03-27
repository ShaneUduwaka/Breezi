from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import contact, newsletter, and the new blogs router
from api import contact, newsletter, blogs

app = FastAPI(title="Breezi Marketing Website API")

# Configure CORS so the frontend (Next.js) can communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the contact router
app.include_router(contact.router, prefix="/api")

# Register the newsletter router
app.include_router(newsletter.router, prefix="/api")

# Register the new blogs router
app.include_router(blogs.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Breezi Backend is running"}