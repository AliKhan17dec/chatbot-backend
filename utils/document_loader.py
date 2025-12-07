"""
Document loader utility for parsing and chunking the book content.
"""
import os
from pathlib import Path
from typing import List, Dict, Tuple
import re
import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import settings

logger = logging.getLogger(__name__)


class DocumentLoader:
    """Utility for loading and processing book documents."""
    
    def __init__(self):
        """Initialize document loader."""
        self.docs_path = Path(settings.book_docs_path)
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n## ", "\n### ", "\n#### ", "\n\n", "\n", " ", ""],
            length_function=len
        )
        logger.info("Document loader initialized")
    
    def extract_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """
        Extract frontmatter metadata from MDX content.
        
        Args:
            content: Raw file content
            
        Returns:
            Tuple of (metadata dict, content without frontmatter)
        """
        frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(frontmatter_pattern, content, re.DOTALL)
        
        metadata = {}
        clean_content = content
        
        if match:
            frontmatter = match.group(1)
            clean_content = content[match.end():]
            
            # Parse simple key: value pairs
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip().strip('"\'')
        
        return metadata, clean_content
    
    def extract_title_from_content(self, content: str, filename: str) -> str:
        """
        Extract title from content or filename.
        
        Args:
            content: Document content
            filename: Filename as fallback
            
        Returns:
            Document title
        """
        # Try to find first H1 heading
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()
        
        # Fallback to filename
        return filename.replace('-', ' ').replace('_', ' ').title()
    
    def determine_module(self, file_path: Path) -> str:
        """
        Determine which module the file belongs to.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Module name
        """
        parts = file_path.parts
        for part in parts:
            if part.startswith('module'):
                return part.replace('-', ' ').title()
        
        # Check for other sections
        if 'appendices' in parts:
            return 'Appendices'
        elif 'capstone' in parts:
            return 'Capstone Project'
        elif 'glossary' in str(file_path):
            return 'Glossary'
        elif 'references' in str(file_path):
            return 'References'
        
        return 'General'
    
    def load_document(self, file_path: Path) -> Tuple[str, Dict]:
        """
        Load a single document file.
        
        Args:
            file_path: Path to the document
            
        Returns:
            Tuple of (content, metadata)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frontmatter
            frontmatter, clean_content = self.extract_frontmatter(content)
            
            # Build metadata
            metadata = {
                'filename': file_path.name,
                'filepath': str(file_path.relative_to(self.docs_path)),
                'module': self.determine_module(file_path),
                'title': frontmatter.get('title') or self.extract_title_from_content(clean_content, file_path.stem),
                **frontmatter
            }
            
            return clean_content, metadata
            
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {str(e)}")
            raise
    
    def load_all_documents(self) -> List[Tuple[str, Dict]]:
        """
        Load all MDX documents from the docs directory.
        
        Returns:
            List of tuples (content, metadata)
        """
        documents = []
        
        if not self.docs_path.exists():
            logger.error(f"Docs path does not exist: {self.docs_path}")
            return documents
        
        # Find all .mdx and .md files
        mdx_files = list(self.docs_path.rglob("*.mdx"))
        md_files = list(self.docs_path.rglob("*.md"))
        all_files = mdx_files + md_files
        
        logger.info(f"Found {len(all_files)} document files")
        
        for file_path in all_files:
            try:
                content, metadata = self.load_document(file_path)
                documents.append((content, metadata))
            except Exception as e:
                logger.warning(f"Skipping file {file_path}: {str(e)}")
                continue
        
        logger.info(f"Successfully loaded {len(documents)} documents")
        return documents
    
    def chunk_document(
        self,
        content: str,
        metadata: Dict
    ) -> List[Tuple[str, Dict]]:
        """
        Split a document into chunks.
        
        Args:
            content: Document content
            metadata: Document metadata
            
        Returns:
            List of tuples (chunk_text, chunk_metadata)
        """
        chunks = self.text_splitter.split_text(content)
        
        chunk_list = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = {
                **metadata,
                'chunk_index': i,
                'total_chunks': len(chunks)
            }
            chunk_list.append((chunk, chunk_metadata))
        
        return chunk_list
    
    def load_and_chunk_all(self) -> List[Tuple[str, Dict]]:
        """
        Load all documents and split them into chunks.
        
        Returns:
            List of tuples (chunk_text, chunk_metadata)
        """
        documents = self.load_all_documents()
        
        all_chunks = []
        for content, metadata in documents:
            chunks = self.chunk_document(content, metadata)
            all_chunks.extend(chunks)
        
        logger.info(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
        return all_chunks


# Global instance
document_loader = DocumentLoader()
