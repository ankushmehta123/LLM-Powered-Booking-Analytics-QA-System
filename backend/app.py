import os
import pickle
import faiss
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import ast
from routes import router

app = FastAPI()

# Include additional routes
app.include_router(router)

# Load saved FAISS index and metadata
faiss_index = faiss.read_index("../vector_db/index.faiss")
with open("../vector_db/index.pkl", "rb") as f:
    index_metadata = pickle.load(f)

# Rebuild FAISS DB
db = FAISS(
    embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
    index=faiss_index,
    docstore=index_metadata[0],  # Fixed index access
    index_to_docstore_id=index_metadata[1]
)

# Load LLM
llm = OllamaLLM(model="llama2")

# Chat prompt template
prompt = ChatPromptTemplate.from_template("""
Answer the following question based only on the provided context.
Think step by step before providing a detailed answer.
NO PREAMBLE
<context>           
{context}
</context> 
Question: {input}
""")

retriever = db.as_retriever()

# Function to evaluate math expressions
def evaluate_math(expression: str):
    try:
        return eval(expression)
    except Exception:
        return "Invalid mathematical expression"

# Function to check if query is a mathematical expression
def is_math_expression(query: str):
    try:
        parsed_expr = ast.parse(query, mode='eval')
        return all(isinstance(node, (ast.Expression, ast.BinOp, ast.Num, ast.UnaryOp, ast.Call)) for node in ast.walk(parsed_expr))
    except Exception:
        return False

# Request Model
class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask_question(request: QueryRequest):
    query = request.query.strip()

    # Check if query is a mathematical expression
    if is_math_expression(query):
        return {"answer": str(evaluate_math(query))}

    # Retrieve context from FAISS
    retrieved_docs = retriever.get_relevant_documents(query)
    context = "\n".join([doc.page_content for doc in retrieved_docs])

    # Generate answer using LLM
    response = llm.predict(prompt.format(context=context, input=query))

    return {"answer": response}
