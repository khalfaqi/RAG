from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from app.services.embedding import EmbeddingService
from app.repository.document_store import DocumentStore

class GraphState(TypedDict):
    question: str
    context: List[str]
    answer: str

class RAGWorkflow:
    def __init__(self, document_store: DocumentStore, embedding_service: EmbeddingService):
        self.document_store = document_store
        self.embedding_service = embedding_service
        self.workflow = self._build_graph()

    def retrieve_node(self, state: GraphState):
        query = state.get("question", "")
        emb = self.embedding_service.get_embedding(query)
        
        results = self.document_store.search(query=query, embedding=emb)
        
        return {"context": results}

    def answer_node(self, state: GraphState):
        ctx = state.get("context", [])
        answer = f"I found this: '{ctx[0][:100]}...'" if ctx else "Sorry, I don't know."
        
        return {"answer": answer}

    def _build_graph(self):
        graph = StateGraph(GraphState)
        
        graph.add_node("retrieve", self.retrieve_node)
        graph.add_node("answer", self.answer_node)
        
        graph.set_entry_point("retrieve")
        graph.add_edge("retrieve", "answer")
        graph.add_edge("answer", END)
        
        return graph.compile()
