from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import contact

app = FastAPI(title="Breezi Marketing Website API")

# Configure CORS so the frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the contact router
app.include_router(contact.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Breezi Backend is running"}
