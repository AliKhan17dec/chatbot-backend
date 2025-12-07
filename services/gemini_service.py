"""
Gemini API integration service for embeddings and text generation.
"""
import google.generativeai as genai
from typing import List, Optional
import logging
from config import settings

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for interacting with Google Gemini API."""
    
    def __init__(self):
        """Initialize Gemini API with configuration."""
        genai.configure(api_key=settings.gemini_api_key)
        self.embedding_model = settings.embedding_model
        self.generation_model = genai.GenerativeModel(settings.generation_model)
        logger.info("Gemini service initialized")
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for given text.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding vector for a query.
        
        Args:
            query: Query text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generating query embedding: {str(e)}")
            raise
    
    def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        embeddings = []
        for text in texts:
            try:
                embedding = self.generate_embedding(text)
                embeddings.append(embedding)
            except Exception as e:
                logger.error(f"Error in batch embedding: {str(e)}")
                # Return zero vector on error to maintain batch size
                embeddings.append([0.0] * 768)  # Default embedding size
        return embeddings
    
    def generate_answer(
        self,
        question: str,
        context: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate answer using Gemini with RAG context.
        
        Args:
            question: User's question
            context: Retrieved context from vector database
            system_prompt: Optional custom system prompt
            
        Returns:
            Generated answer as string
        """
        try:
            if system_prompt is None:
                system_prompt = """You are an expert assistant for the Humanoid Robotics and Physical AI textbook. 
Your role is to help students understand concepts related to ROS 2, robot simulation, NVIDIA Isaac, 
and vision-language-action systems for humanoid robots.

Instructions:
- Provide accurate, clear, and educational answers based on the provided context
- If the context doesn't contain enough information, acknowledge this
- Use technical terms appropriately but explain complex concepts
- Include practical examples when helpful
- Reference specific modules or sections when relevant
- Be encouraging and supportive to learners"""
            
            prompt = f"""{system_prompt}

Context from the textbook:
{context}

Student's question: {question}

Answer:"""
            
            response = self.generation_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise
    
    def generate_answer_from_selection(
        self,
        question: str,
        selected_text: str
    ) -> str:
        """
        Generate answer based on user-selected text.
        
        Args:
            question: User's question about the selected text
            selected_text: Text selected by the user
            
        Returns:
            Generated answer as string
        """
        try:
            system_prompt = """You are an expert assistant for the Humanoid Robotics and Physical AI textbook.
The student has selected specific text and has a question about it.

Instructions:
- Focus your answer on the selected text
- Provide clear explanations and examples
- If the question asks for simplification, use analogies
- If the question asks for elaboration, provide more technical details
- Be concise but thorough"""
            
            prompt = f"""{system_prompt}

Selected text from the book:
{selected_text}

Student's question: {question}

Answer:"""
            
            response = self.generation_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating answer from selection: {str(e)}")
            raise
    
    async def agenerate_answer(
        self,
        question: str,
        context: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Async version of generate_answer.
        Note: google-generativeai doesn't have native async support yet,
        so this wraps the sync call.
        """
        return self.generate_answer(question, context, system_prompt)


# Global service instance
gemini_service = GeminiService()
