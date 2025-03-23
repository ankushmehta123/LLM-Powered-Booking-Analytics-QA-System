# LLM-Powered-Booking-Analytics-QA-System 🚀

A **Retrieval-Augmented Generation (RAG) chatbot** using **FastAPI, FAISS, and LangChain**.  
It can **answer booking-related queries** and **perform calculations**.

---

## **⚡ Features**
- **Natural Language Querying**: Retrieve hotel booking insights.
- **Vector Search with FAISS**: Stores embeddings for fast retrieval.
- **Math Calculation Support**: Can process and return mathematical computations.
- **FastAPI Backend**: REST API for chatbot queries.
- **Streamlit Frontend**: Simple UI for chat.

---

## **🔹 Setup Instructions**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/yourusername/LLM_Booking_Analytics_System.git
cd LLM_Booking_Analytics_System 
```

### **2️⃣ Setup the Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate      # For Windows
```

### **3️⃣ Install Dependencies**

#### Backend Dependencies
```sh
cd backend
pip install -r requirements.txt
```
#### Frontend Dependencies
```sh
cd ../frontend
pip install -r requirements.txt
```

---

## **🔹 Running the Application**
### **1️⃣ Start FastAPI Backend**
```sh
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### **2️⃣ Run the Chatbot (CLI)**
```sh
cd ../frontend
python chatbot.py
```

---

## 🔹 API Endpoints

| **Method** | **Endpoint**            | **Description**                          |
|-----------|-------------------------|------------------------------------------|
| `POST`    | `/`                   | Ask a question using RAG                |
| `GET`     | `/revenue_trends/`       | Get revenue trends (requires `year` & `month`) |
| `GET`     | `/cancellations/`        | Get cancellations (requires `year`, `month`, `day`) |

### 🔹 Example Query

#### **📌 Ask a question using RAG**
```sh
curl -X 'POST' 'http://127.0.0.1:8000/' \
-H 'Content-Type: application/json' \
-d '{"query": "What is the highest revenue year?"}'





