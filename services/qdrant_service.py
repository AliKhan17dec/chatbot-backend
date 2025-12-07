"""
Qdrant vector database service for storing and retrieving embeddings.
"""
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    SearchRequest
)
from typing import List, Dict, Optional, Tuple
import logging
from config import settings
import uuid

logger = logging.getLogger(__name__)


class QdrantService:
    """Service for interacting with Qdrant vector database."""
    
    def __init__(self):
        """Initialize Qdrant client."""
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
        self.collection_name = settings.qdrant_collection_name
        self.vector_size = 768  # Gemini text-embedding-004 dimension
        logger.info("Qdrant service initialized")
    
    def create_collection(self, force_recreate: bool = False) -> bool:
        """
        Create collection in Qdrant if it doesn't exist.
        
        Args:
            force_recreate: If True, delete and recreate the collection
            
        Returns:
            True if collection was created/recreated, False if already exists
        """
        try:
            collections = self.client.get_collections().collections
            collection_exists = any(
                col.name == self.collection_name for col in collections
            )
            
            if collection_exists and force_recreate:
                logger.info(f"Deleting existing collection: {self.collection_name}")
                self.client.delete_collection(self.collection_name)
                collection_exists = False
            
            if not collection_exists:
                logger.info(f"Creating collection: {self.collection_name}")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    )
                )
                return True
            
            logger.info(f"Collection {self.collection_name} already exists")
            return False
            
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            raise
    
    def add_documents(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict]
    ) -> int:
        """
        Add documents with embeddings to Qdrant.
        
        Args:
            texts: List of document texts
            embeddings: List of embedding vectors
            metadatas: List of metadata dictionaries
            
        Returns:
            Number of documents added
        """
        try:
            points = []
            for i, (text, embedding, metadata) in enumerate(zip(texts, embeddings, metadatas)):
                point_id = str(uuid.uuid4())
                payload = {
                    "text": text,
                    **metadata
                }
                
                point = PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload
                )
                points.append(point)
            
            # Upload in batches for better performance
            batch_size = 100
            for i in range(0, len(points), batch_size):
                batch = points[i:i + batch_size]
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch
                )
            
            logger.info(f"Added {len(points)} documents to Qdrant")
            return len(points)
            
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
    
    def search(
        self,
        query_embedding: List[float],
        limit: int = 5,
        score_threshold: Optional[float] = None
    ) -> List[Tuple[str, float, Dict]]:
        """
        Search for similar documents.
        
        Args:
            query_embedding: Query embedding vector
            limit: Maximum number of results to return
            score_threshold: Minimum similarity score threshold
            
        Returns:
            List of tuples (text, score, metadata)
        """
        try:
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                score_threshold=score_threshold
            )
            
            results = []
            for scored_point in search_result:
                text = scored_point.payload.get("text", "")
                score = scored_point.score
                metadata = {
                    k: v for k, v in scored_point.payload.items()
                    if k != "text"
                }
                results.append((text, score, metadata))
            
            logger.info(f"Found {len(results)} similar documents")
            return results
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            raise
    
    def get_collection_info(self) -> Dict:
        """
        Get information about the collection.
        
        Returns:
            Dictionary with collection information
        """
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": info.config.params.vectors.size,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            return {}
    
    def check_connection(self) -> bool:
        """
        Check if Qdrant connection is working.
        
        Returns:
            True if connected, False otherwise
        """
        try:
            self.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Qdrant connection check failed: {str(e)}")
            return False
    
    def delete_collection(self) -> bool:
        """
        Delete the collection.
        
        Returns:
            True if successful
        """
        try:
            self.client.delete_collection(self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting collection: {str(e)}")
            return False


# Global service instance
qdrant_service = QdrantService()
