import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

# Initialize FastAPI app
app = FastAPI(
    title="AI Customer Support Chatbot API",
    description="Backend API for customer support chatbot using RAG and local Ollama.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Customer Support Chatbot API. Access /docs for API documentation."}

if __name__ == "__main__":
    # Start the FastAPI server
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
