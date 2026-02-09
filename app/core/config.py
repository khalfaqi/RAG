class Settings:
    PROJECT_NAME: str = "Learning RAG Demo"
    QDRANT_URL: str = "http://localhost:6333"
    COLLECTION_NAME: str = "demo_collection"
    EMBEDDING_DIMENSION: int = 128

settings = Settings()