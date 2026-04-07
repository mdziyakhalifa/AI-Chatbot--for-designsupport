import os
import shutil
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from rag_pipeline.chain import RAGChain
from rag_pipeline.document_processor import DocumentProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
rag_chain = RAGChain()
document_processor = DocumentProcessor()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@router.post("/query", response_model=QueryResponse)
async def query_chatbot(request: QueryRequest):
    """
    Endpoint to interact with the chatbot using RAG.
    """
    logger.info(f"Received query: {request.question}")
    result = rag_chain.ask(request.question)
    
    if isinstance(result, str):
        # Handle the case where the knowledge base is empty
        return QueryResponse(answer=result, sources=[])
    
    return QueryResponse(
        answer=result.get("answer"),
        sources=result.get("sources")
    )

@router.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload PDF or TXT documents to the knowledge base.
    """
    upload_dir = "data"
    os.makedirs(upload_dir, exist_ok=True)
    
    all_docs = []
    for file in files:
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Saved file: {file.filename}")
        docs = document_processor.process_file(file_path)
        all_docs.extend(docs)
    
    if all_docs:
        rag_chain.vector_store_manager.add_documents(all_docs)
        # Update the chain to use the new documents
        rag_chain.chain = rag_chain._initialize_chain()
        return {"message": f"Successfully processed {len(files)} files and updated knowledge base."}
    
    raise HTTPException(status_code=400, detail="No suitable documents found to process.")

@router.post("/clear-history")
async def clear_history():
    """Endpoint to clear chat history."""
    rag_chain.reset_memory()
    return {"message": "Chat history cleared."}
