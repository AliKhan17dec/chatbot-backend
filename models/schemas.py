"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatQuery(BaseModel):
    """Request model for chat queries."""
    question: str = Field(..., min_length=1, max_length=1000, description="User's question")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "What is ROS 2 and why is it important for robotics?",
                    "session_id": "user-123-session-456"
                }
            ]
        }
    }


class ChatQueryWithSelection(BaseModel):
    """Request model for queries based on selected text."""
    question: str = Field(..., min_length=1, max_length=1000, description="User's question")
    selected_text: str = Field(..., min_length=10, description="Text selected by user")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "Explain this concept in simpler terms",
                    "selected_text": "ROS 2 Nodes, Topics, and Services...",
                    "session_id": "user-123-session-456"
                }
            ]
        }
    }


class Source(BaseModel):
    """Source document information."""
    title: str = Field(..., description="Document title or section")
    content: str = Field(..., description="Relevant content snippet")
    similarity_score: float = Field(..., description="Similarity score")
    metadata: Optional[dict] = Field(None, description="Additional metadata")


class ChatResponse(BaseModel):
    """Response model for chat queries."""
    answer: str = Field(..., description="Generated answer")
    sources: List[Source] = Field(default_factory=list, description="Source documents used")
    session_id: Optional[str] = Field(None, description="Session ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "answer": "ROS 2 is a middleware framework for robot control...",
                    "sources": [
                        {
                            "title": "Module 1: ROS 2 Architecture",
                            "content": "ROS 2 provides...",
                            "similarity_score": 0.89
                        }
                    ],
                    "session_id": "user-123-session-456",
                    "timestamp": "2025-12-07T10:30:00"
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    qdrant_connected: bool = Field(..., description="Qdrant connection status")
    database_connected: bool = Field(..., description="Database connection status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class IndexingRequest(BaseModel):
    """Request to trigger document indexing."""
    force_reindex: bool = Field(False, description="Force re-indexing of all documents")


class IndexingResponse(BaseModel):
    """Response for indexing operation."""
    status: str = Field(..., description="Indexing status")
    documents_processed: int = Field(..., description="Number of documents processed")
    chunks_created: int = Field(..., description="Number of chunks created")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
