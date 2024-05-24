from pinecone import Pinecone
from embedders import AllMiniLML6V2
from typing import List
import os

class VectorDatabase:
    def __init__(self) -> None:
        pass
    def query(self, query: str):
        pass


class PineConeRetriver(VectorDatabase):
    def __init__(self, encoder, api_key=None) -> None:
        super().__init__()
        index_name=os.environ.get("INDEX_NAME",None)
        if api_key is None:
            
            api_key = os.environ.get("PINECONE_API_KEY",None)
            if not api_key:
                raise Exception("API KEY is required. Please put PIENCONE_API")
        
        self.pc = Pinecone(api_key=api_key)
        self.index_name = index_name
        self.encoder = encoder
  
        self._connect_to_index()

    def _connect_to_index(self):
        self.index = self.pc.Index(self.index_name)

    def get_index_stats(self):
        stats = self.index.describe_index_stats()
        print(stats)
        return stats
    
    def query(self, query: str,top_k=5)->List:
        xq = self.encoder.embed(query).tolist()
        xc = self.index.query(vector=xq, top_k=top_k, include_metadata=True)

        results = []
        for result in xc['matches']:
            if result["score"]>0.5:
                results.append({"title": result["metadata"]["title"] , 
                                "text":result["metadata"]["text"],
                                "score": result["score"] })

        return results
