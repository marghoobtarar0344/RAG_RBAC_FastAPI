# 🚀 RAG-Based Document Query API with FastAPI & OpenAI GPT

## 📌 Overview
This FastAPI-based microservice implements a **Retrieval-Augmented Generation (RAG)** pipeline to fetch relevant document chunks from a **vector database** and optionally summarize them using OpenAI's **GPT model**.

## ✨ Features
-   **Retrieve Top-1 Relevant Chunks** from a vector database
-   **ChatGPT/Hugging-face Summarization** for concise insights
-   **JWT Authentication & Authorization** with role-based access control
-   **FastAPI's OpenAPI Documentation** for seamless API testing
-   **Asynchronous Processing** for better performance
-   **Exception Handling** for robust error management

##  Tech Stack
- **FastAPI** - API framework for building high-performance web services
- **LangChain** - Vector database similarity search
- **OpenAI GPT-4/ Huggingf Face** - Summarization of retrieved content
- **SQLAlchemy** - Database ORM for handling user authentication & permissions

---

##  Quick Start

### 1️ Clone the Repository
```sh
git clone https://github.com/marghoobtarar0344/RAG_RBAC_FastAPI.git
cd RAG_RBAC_FastAPI
```

### 2️ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️ Set Up Environment Variables
Create a `.env` file with the following variables:
```env
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
OPENAI_API_KEY= ""
```

### 4️ Run the Application
```sh
uvicorn main:app --reload
```

### 5️ Access API Docs 
Visit:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔥 API Endpoints

### 🔍 **Query Documents**
```http
POST /query
```
#### Request Body (JSON):
```json
{
  "query": "What is AI?",
}
```
#### Response Example:
```

 "AI replicates human intelligence through ML and deep learning."

```

### 🔐 **Authentication & Authorization**
- **JWT-based auth** with roles (e.g.,`admin`, `read`, `write` permissions)
- Users must include a valid token in requests

---

###  Using Docker
```sh
docker build -t rag-fastapi .
docker run -p 8000:8000 rag-fastapi
```


