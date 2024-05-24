from abc import ABC, abstractmethod
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingsBase(ABC):

    def __init__(self):
        pass
       

    @abstractmethod
    def embed(self, text: str) -> np.ndarray:
        """
        Return an ND Array
        """
        pass




class AllMiniLML6V2(EmbeddingsBase):

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        super().__init__()
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> np.ndarray:
        return self.model.encode([text])


# embedder = AllMiniLML6V2()

# print(embedder.embed("hi hello"))