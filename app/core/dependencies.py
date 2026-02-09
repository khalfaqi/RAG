from app.services.embedding import EmbeddingService
from app.repository.document_store import DocumentStore
from app.workflows.rag_workflow import RAGWorkflow
from app.core.config import settings

# Inisialisasi service utama
# Ini dilakukan di level modul agar instance tetap sama (reusable)
embedding_service = EmbeddingService(num_dimensions=settings.EMBEDDING_DIMENSION)
document_store = DocumentStore(use_qdrant=True)

# Inisialisasi Workflow dengan menyuntikkan dependencies
rag_workflow = RAGWorkflow(
    document_store=document_store,
    embedding_service=embedding_service
)

# Fungsi Dependency untuk FastAPI
def get_embedding_service() -> EmbeddingService:
    return embedding_service

def get_document_store() -> DocumentStore:
    return document_store

def get_rag_workflow() -> RAGWorkflow:
    return rag_workflow