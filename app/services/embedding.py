import random

class EmbeddingService:
    def __init__(self, num_dimensions: int):
        self.num_dimensions = num_dimensions

    def get_embedding(self, text: str):
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(self.num_dimensions)]

    