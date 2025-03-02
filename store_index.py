from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
import os

load_dotenv()

extracted_data=load_pdf_file(data='Data/')
text_chunks=text_split(extracted_data)
embeddings = download_hugging_face_embeddings()

# Embed each chunk and upsert the embeddings into your Pinecone index.
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

vectorstore.add_documents(text_chunks)