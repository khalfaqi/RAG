from fastapi import FastAPI, Depends
from app.core.dependencies import get_document_store, get_embedding_service, get_rag_workflow
from app.api.schemas import QuestionRequest, DocumentRequest
from app.repository.document_store import DocumentStore
from app.services.embedding import EmbeddingService
from app.workflows.rag_workflow import RAGWorkflow
from app.core.config import settings

app = FastAPI()

@app.post("/add")
def add_document(
    req: DocumentRequest, 
    doc_store: DocumentStore = Depends(get_document_store),
    embed_service: EmbeddingService = Depends(get_embedding_service)
):
    # Proses tetap sama, tapi instance didapat dari Depends
    vector = embed_service.get_embedding(req.text)
    doc_id = doc_store.add_document(req.text, vector)
    
    return {"id": doc_id, "status": "added"}

@app.post("/ask")
def ask_question(
    req: QuestionRequest,
    rag: RAGWorkflow = Depends(get_rag_workflow)
):
    # Endpoint hanya memanggil workflow yang sudah jadi
    result = rag.workflow.invoke({"question": req.question})
    
    return {
        "question": req.question,
        "answer": result["answer"],
        "context": result.get("context", [])
    }

@app.get("/status")
def get_status(
    doc_store: DocumentStore = Depends(get_document_store),
    rag: RAGWorkflow = Depends(get_rag_workflow)
):
    return {
        "qdrant_connected": doc_store.use_qdrant,
        "total_docs_in_memory": len(doc_store.docs_memory),
        "embedding_dim": settings.EMBEDDING_DIMENSION,
        "workflow_ready": rag.workflow is not None,
        "collection_name": settings.COLLECTION_NAME if doc_store.use_qdrant else "N/A"
    }