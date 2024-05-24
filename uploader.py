import warnings
import os
import pinecone
import time
from llama_index.core import SimpleDirectoryReader
import pandas as pd
from torch import cuda
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

pinecone.init(
    api_key=os.environ.get('PINECONE_API_KEY') or '64cf8412-429a-4815-92ab-1b6aad6c5c33',
    environment=os.environ.get('PINECONE_ENVIRONMENT') or 'gcp-starter'
)


index_name = 'llama-2-rag'

if index_name not in pinecone.list_indexes():
    pinecone.create_index(
        index_name,
        dimension=384,
        metric='cosine'
    )
    # wait for index to finish initialization
    while not pinecone.describe_index(index_name).status['ready']:
        time.sleep(1)
index = pinecone.Index(index_name)

print(index.describe_index_stats())
def getEnding(start,text):
  ret=i=min(start+200,len(text)-1)
  while i>start:
    if text[i]==".":
      ret=i
      break
    i-=1
  return ret


reader = SimpleDirectoryReader('data')
documents = reader.load_data()

data = []
for doc in documents:
    text = doc.text
    start=0
    while start<len(text):
      end=getEnding(start,text)

      chunk =text[start:end]
      if not chunk:
        break
      data.append({'text': chunk, 'title': doc.metadata.get('file_name', '')})
      start=end+1

embed_model_id = 'sentence-transformers/all-MiniLM-L6-v2'

device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

embed_model = HuggingFaceEmbeddings(
    model_name=embed_model_id,
    model_kwargs={'device': device},
    encode_kwargs={'device': device, 'batch_size': 32}
)
data = pd.DataFrame(data)
import numpy as np
batch_size = 32
with warnings.catch_warnings():
  warnings.simplefilter('ignore')



  for i in range(0, len(data), batch_size):
      batch = data.iloc[i:i+batch_size]
      #print(batch)
      batch['chunk_id'] = batch.index
      ids = [f"{x['title']}-{x['chunk_id']}" for i, x in batch.iterrows()]
      texts = [x['text'] for i, x in batch.iterrows()]
      embeds = embed_model.embed_documents(texts)
      #embeds = np.array(embeds)
     # print(len(embeds[0]),texts)
      # get metadata to store in Pinecone
      metadata = [
      {'text': x['text'],'title': x['title']}
      for i, x in batch.iterrows()
  ]
      try:
      # add to Pinecone{
        index.upsert(vectors=zip(ids, embeds, metadata))
      except:
        print([len(e) for e in embeds])
        print(batch)

print(index.describe_index_stats())