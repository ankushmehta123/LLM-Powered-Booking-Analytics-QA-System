from fastapi import FastAPI
import faiss
import pickle
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from routes import router  # Import API routes

app = FastAPI()

# Load FAISS Index
index_path = "../vector_db/index.faiss"
meta_path = "../vector_db/index.pkl"

with open(meta_path, "rb") as f:
    index_metadata = pickle.load(f)  # Load FAISS metadata

faiss_index = faiss.read_index(index_path)  # Load FAISS index

# Initialize FAISS Vector Store
db = FAISS(
    embedding_function=OllamaEmbeddings(model="nomic-embed-text"), 
    index=faiss_index, 
    docstore=index_metadata[0], 
    index_to_docstore_id=index_metadata[1]
)

retriever = db.as_retriever()

@app.post("/ask/")
def ask_question(query: dict):
    """Handles user queries via FAISS retrieval"""
    search_results = retriever.get_relevant_documents(query["query"])
    
    if search_results:
        response = {"answer": search_results[0].page_content}
    else:
        response = {"answer": "No relevant data found."}
    
    return response

# Include additional routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
