from flask import Flask, render_template, request
from src.helper import download_hugging_face_embeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
from langchain_community.vectorstores import Chroma
from chromadb import PersistentClient
import os

app = Flask(__name__)

load_dotenv()
GROQ_API_KEY=os.environ.get('GROQ_API_KEY')

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

embeddings = download_hugging_face_embeddings()

# Initialize a global variable for index_name
index_name = None

# Initialize the client with the path to your Chroma database
client = PersistentClient(path="./chroma_db")

# Get all collections
collections = client.list_collections()
# Print collection names
for collection in collections:
    index_name = collection

# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = Chroma(
    client=client,
    collection_name=index_name,
    embedding_function=embeddings
)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    response = rag_chain.invoke({"input": msg})
    return str(response["answer"])



 
if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080)