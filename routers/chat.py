"""
Chat router for handling chatbot endpoints.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.schemas import (
    ChatQuery,
    ChatQueryWithSelection,
    ChatResponse,
    IndexingRequest,
    IndexingResponse,
    Source
)
from services.rag_service import rag_service
from services.qdrant_service import qdrant_service
from utils.document_loader import document_loader
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/query", response_model=ChatResponse)
async def query_chatbot(query: ChatQuery):
    """
    Query the chatbot with a question about the book content.
    
    The chatbot uses RAG to retrieve relevant sections from the book
    and generates an answer using Gemini.
    """
    try:
        logger.info(f"Received query: {query.question[:50]}...")
        
        # Generate answer using RAG
        answer, sources = rag_service.generate_answer(query.question)
        
        # Convert sources to response format
        source_objects = [
            Source(
                title=src['title'],
                content=src['content'],
                similarity_score=src['similarity_score'],
                metadata=src.get('metadata', {})
            )
            for src in sources
        ]
        
        return ChatResponse(
            answer=answer,
            sources=source_objects,
            session_id=query.session_id,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.post("/query-selection", response_model=ChatResponse)
async def query_with_selection(query: ChatQueryWithSelection):
    """
    Query the chatbot about a specific text selection.
    
    This endpoint is used when the user selects text in the book
    and asks a question about it. No retrieval is needed as the
    context is provided in the selection.
    """
    try:
        logger.info(f"Received selection query: {query.question[:50]}...")
        
        # Generate answer from selected text
        answer = rag_service.generate_answer_from_selection(
            question=query.question,
            selected_text=query.selected_text
        )
        
        # Create a source from the selection
        source = Source(
            title="Selected Text",
            content=query.selected_text[:200] + "..." if len(query.selected_text) > 200 else query.selected_text,
            similarity_score=1.0,
            metadata={"type": "user_selection"}
        )
        
        return ChatResponse(
            answer=answer,
            sources=[source],
            session_id=query.session_id,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error processing selection query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing selection query: {str(e)}")


@router.post("/index", response_model=IndexingResponse)
async def index_documents(
    request: IndexingRequest,
    background_tasks: BackgroundTasks
):
    """
    Index or re-index all book documents.
    
    This endpoint loads all MDX files from the book, chunks them,
    generates embeddings, and stores them in Qdrant.
    
    Note: This can take several minutes depending on the number of documents.
    """
    try:
        logger.info("Starting document indexing...")
        
        # Create or recreate collection
        qdrant_service.create_collection(force_recreate=request.force_reindex)
        
        # Load and chunk documents
        chunks = document_loader.load_and_chunk_all()
        
        if not chunks:
            raise HTTPException(status_code=400, detail="No documents found to index")
        
        # Extract texts and metadata
        texts = [chunk[0] for chunk in chunks]
        metadatas = [chunk[1] for chunk in chunks]
        
        # Count unique documents
        unique_docs = len(set(meta['filepath'] for meta in metadatas))
        
        # Index documents
        indexed_count = rag_service.index_documents(texts, metadatas)
        
        return IndexingResponse(
            status="success",
            documents_processed=unique_docs,
            chunks_created=indexed_count,
            timestamp=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error indexing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error indexing documents: {str(e)}")


@router.get("/collection-info")
async def get_collection_info():
    """
    Get information about the Qdrant collection.
    
    Returns statistics about the indexed documents.
    """
    try:
        info = qdrant_service.get_collection_info()
        return {
            "status": "success",
            "collection": info
        }
    except Exception as e:
        logger.error(f"Error getting collection info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting collection info: {str(e)}")
