# from torch import cuda
# import pinecone
# import pinecone
# from config import SECRETS,SETTINGS

# device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

# # #EMBEDDING MODEL
# # embed_model_id = SETTINGS["EMBEDDINGS"]["embed_model_id"] 
# # embed_model = HuggingFaceEmbeddings(
# #         model_name=embed_model_id,
# #         model_kwargs={'device': device},
# #         encode_kwargs={'device': device, 'batch_size': SETTINGS["EMBEDDINGS"]["batch_size"] }
# #     )


# #PINECONE SETUP
# pinecone.init(
#         api_key= SECRETS["PINECONE_API_KEY"] ,
#         environment= SECRETS["PINECONE_ENVIRONMENT"] 
#     )

# index_name = SECRETS["INDEX_NAME"]
# index = pinecone.Index(index_name)
# vectorstore = Pinecone(
#     index, embed_model.embed_query, 'text'
# )

# #REPLICATE SETUP
# llm = Replicate(
#     model=SETTINGS["REPLICATE"]["model"] ,
#     model_kwargs={"temperature": SETTINGS["REPLICATE"]["temperature"] ,
#                   "max_length": SETTINGS["REPLICATE"]["maximum_length"] ,
#                   "top_p": SETTINGS["REPLICATE"]["top_p"] },
# )

