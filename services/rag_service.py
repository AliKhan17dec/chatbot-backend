"""
RAG (Retrieval-Augmented Generation) service combining Qdrant and Gemini.
"""
from typing import List, Tuple, Dict
import logging
from services.gemini_service import gemini_service
from services.qdrant_service import qdrant_service
from config import settings

logger = logging.getLogger(__name__)


class RAGService:
    """Service for Retrieval-Augmented Generation pipeline."""
    
    def __init__(self):
        """Initialize RAG service with Gemini and Qdrant services."""
        self.gemini = gemini_service
        self.qdrant = qdrant_service
        self.top_k = settings.top_k_results
        self.similarity_threshold = settings.similarity_threshold
        logger.info("RAG service initialized")
    
    def retrieve_context(
        self,
        query: str,
        top_k: int = None,
        score_threshold: float = None
    ) -> List[Tuple[str, float, Dict]]:
        """
        Retrieve relevant context for a query.
        
        Args:
            query: User's query
            top_k: Number of results to retrieve (default from settings)
            score_threshold: Minimum similarity score (default from settings)
            
        Returns:
            List of tuples (text, score, metadata)
        """
        try:
            # Generate query embedding
            query_embedding = self.gemini.generate_query_embedding(query)
            
            # Search in Qdrant
            results = self.qdrant.search(
                query_embedding=query_embedding,
                limit=top_k or self.top_k,
                score_threshold=score_threshold or self.similarity_threshold
            )
            
            logger.info(f"Retrieved {len(results)} relevant documents for query")
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            raise
    
    def format_context(
        self,
        results: List[Tuple[str, float, Dict]]
    ) -> str:
        """
        Format retrieved results into a context string.
        
        Args:
            results: List of tuples (text, score, metadata)
            
        Returns:
            Formatted context string
        """
        if not results:
            return "No relevant context found in the textbook."
        
        context_parts = []
        for i, (text, score, metadata) in enumerate(results, 1):
            title = metadata.get('title', 'Unknown Section')
            module = metadata.get('module', '')
            
            context_parts.append(
                f"[Source {i}] {title} (Module: {module})\n"
                f"Relevance: {score:.2f}\n"
                f"{text}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    def generate_answer(
        self,
        question: str,
        top_k: int = None,
        score_threshold: float = None
    ) -> Tuple[str, List[Dict]]:
        """
        Generate answer using RAG pipeline.
        
        Args:
            question: User's question
            top_k: Number of context documents to retrieve
            score_threshold: Minimum similarity score
            
        Returns:
            Tuple of (answer, sources) where sources is list of dicts
        """
        try:
            # Retrieve relevant context
            results = self.retrieve_context(question, top_k, score_threshold)
            
            if not results:
                answer = (
                    "I couldn't find relevant information in the textbook to answer your question. "
                    "Could you rephrase or ask about topics covered in the Physical AI & Humanoid Robotics course?"
                )
                return answer, []
            
            # Format context for generation
            context = self.format_context(results)
            
            # Generate answer
            answer = self.gemini.generate_answer(question, context)
            
            # Format sources
            sources = [
                {
                    "title": metadata.get('title', 'Unknown'),
                    "content": text[:200] + "..." if len(text) > 200 else text,
                    "similarity_score": score,
                    "metadata": metadata
                }
                for text, score, metadata in results
            ]
            
            logger.info(f"Generated answer with {len(sources)} sources")
            return answer, sources
            
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise
    
    def generate_answer_from_selection(
        self,
        question: str,
        selected_text: str
    ) -> str:
        """
        Generate answer based on user-selected text (no retrieval needed).
        
        Args:
            question: User's question
            selected_text: Text selected by the user
            
        Returns:
            Generated answer
        """
        try:
            answer = self.gemini.generate_answer_from_selection(
                question=question,
                selected_text=selected_text
            )
            
            logger.info("Generated answer from selected text")
            return answer
            
        except Exception as e:
            logger.error(f"Error generating answer from selection: {str(e)}")
            raise
    
    def index_documents(
        self,
        texts: List[str],
        metadatas: List[Dict]
    ) -> int:
        """
        Index documents in the vector database.
        
        Args:
            texts: List of document texts
            metadatas: List of metadata dictionaries
            
        Returns:
            Number of documents indexed
        """
        try:
            logger.info(f"Starting to index {len(texts)} documents")
            
            # Generate embeddings
            embeddings = self.gemini.generate_batch_embeddings(texts)
            
            # Store in Qdrant
            count = self.qdrant.add_documents(texts, embeddings, metadatas)
            
            logger.info(f"Successfully indexed {count} documents")
            return count
            
        except Exception as e:
            logger.error(f"Error indexing documents: {str(e)}")
            raise


# Global service instance
rag_service = RAGService()
