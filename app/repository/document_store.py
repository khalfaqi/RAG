from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from app.core.config import settings
import uuid

class DocumentStore:
    def __init__(self, use_qdrant=True):
        self.use_qdrant = use_qdrant
        self.docs_memory = []

        if self.use_qdrant:
            try:
                self.qdrant = QdrantClient(settings.QDRANT_URL)
                self.qdrant.recreate_collection(
                    collection_name=settings.COLLECTION_NAME,
                    vectors_config=VectorParams(settings.EMBEDDING_DIMENSION, distance=Distance.COSINE)
                )
            except Exception as e:
                print("⚠️  Qdrant not available. Falling back to in-memory list.")
                self.use_qdrant = False

    def add_document(self, text: str, embedding: list):
        doc_id = str(uuid.uuid4())
        if self.use_qdrant:
            point = PointStruct(id=doc_id, vector=embedding, payload={"text": text})
            self.qdrant.upsert(collection_name=settings.COLLECTION_NAME, points=[point])
        self.docs_memory.append(text)
        return doc_id

    def search(self, query: str, embedding: list, limit: int = 2):
        results = []
        if self.use_qdrant:
            hits = self.qdrant.search(collection_name=settings.COLLECTION_NAME, query_vector=embedding, limit=limit)
            for hit in hits:
                results.append(hit.payload["text"])
        else:
            for doc in self.docs_memory:
                if query.lower() in doc.lower():
                    results.append(doc)
            if not results and self.docs_memory:
                results = [self.docs_memory[0]]  
        return results[:limit]
