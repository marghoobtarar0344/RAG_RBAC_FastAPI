from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os

from schemas.token import TokenData
from schemas.rag import DocumentRequest, QueryRequest
from common.roles import check_role
from middleware.current_user import get_current_user
from database.session import get_db
from .crud import summarize_text_hugging_face, summarize_text_openAi
from config.global_variables import (
    VECTOR_DB_PATH,
    HUGGING_FACE_MODEL,
    RECURSIVE_SPLITTER_CHUNK_OVERLAP,
    RECURSIVE_SPLITTER_CHUNK_SIZE
)

router = APIRouter()
# RAG Setup

os.makedirs(VECTOR_DB_PATH, exist_ok=True)


# we can also utilize chroma db with the help of server
'''
import chromadb

chroma_client = chromadb.HttpClient(host="localhost", port=8000)
collection = chroma_client.get_or_create_collection(name="my_collection")

# Example: Add a document
collection.add(
    ids=["doc1"],
    metadatas=[{"source": "user"}],
    documents=["This is a sample document."]
)

# Example: Query documents
results = collection.query(query_texts=["sample"], n_results=2)
print(results)

'''
embedding_model = HuggingFaceEmbeddings(
    model_name=HUGGING_FACE_MODEL
)
vector_db = Chroma(
    persist_directory=VECTOR_DB_PATH,
    embedding_function=embedding_model
)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=RECURSIVE_SPLITTER_CHUNK_SIZE,
    chunk_overlap=RECURSIVE_SPLITTER_CHUNK_OVERLAP
)

# RAG Endpoints with Role-Based Access (async)


@router.post("/add_document")
async def add_document(request: DocumentRequest, user: TokenData = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Add a document to the vector database."""
    await check_role(user, "admin", "embedding", db)

    if not request.content.strip():
        raise HTTPException(status_code=400, detail="Empty document provided")

    # Split the document into chunks
    chunks = text_splitter.split_text(request.content)
    if not chunks:
        raise HTTPException(
            status_code=400, detail="No valid chunks generated from the document")

    # Convert chunks to Document objects
    documents = [Document(page_content=chunk) for chunk in chunks]

    # Store document chunks in vector DB
    try:
        vector_db.add_documents(documents)
        vector_db.persist()  # Ensure changes are saved
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to add document: {str(e)}")

    return {"message": f"Document added with {len(chunks)} chunks"}


@router.post("/query_hugging_face")
async def query_documents(request: QueryRequest, user: TokenData = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Retrieve the most relevant chunks based on query."""
    await check_role(user, "read", "llm_query", db)

    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Empty query provided")

    try:
        # Retrieve top-k results
        results = vector_db.similarity_search_with_score(request.query, k=1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

    if not results:
        raise HTTPException(
            status_code=404, detail="No relevant documents found")

    text = await summarize_text_hugging_face(results[0][0].page_content)

    return {"results": text}


@router.post("/query_openAI_GPT4")
async def query_documents(request: QueryRequest, user: TokenData = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Retrieve the most relevant chunks based on query."""
    await check_role(user, "read", "llm_query", db)

    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Empty query provided")

    try:
        # Retrieve top-1 results
        results = vector_db.similarity_search_with_score(request.query, k=1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

    if not results:
        raise HTTPException(
            status_code=404, detail="No relevant documents found")

    # Format results
    print(results[0][0].page_content)
    text = await summarize_text_openAi(results[0][0].page_content)

    return {"results": text}


@router.post("/clear_db")
async def clear_db(user: TokenData = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Clear the vector database."""
    await check_role(user, "admin", "document", db)

    try:
        await vector_db.delete_collection()
        await vector_db.persist()
        return {"message": "Vector database cleared successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to clear database: {str(e)}")
