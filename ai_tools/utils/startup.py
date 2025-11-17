"""
Startup utilities for reliable initialization
"""
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import sys
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

logger = logging.getLogger(__name__)


class StartupManager:
    """Manages application startup and initialization"""
    
    def __init__(self):
        self.status: Dict[str, Any] = {
            'initialized': False,
            'errors': [],
            'warnings': [],
            'components': {}
        }
    
    def ensure_directories(self, base_path: Path) -> bool:
        """
        Ensure all necessary directories exist
        
        Args:
            base_path: Base directory for application data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            directories = [
                base_path,
                base_path / "chroma_db",
            ]
            
            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)
                if not directory.exists():
                    self.status['errors'].append(f"Failed to create directory: {directory}")
                    return False
            
            self.status['components']['directories'] = 'ok'
            return True
        except Exception as e:
            self.status['errors'].append(f"Directory creation failed: {e}")
            logger.error(f"Failed to ensure directories: {e}")
            return False
    
    def check_chromadb(self) -> Tuple[bool, Optional[str]]:
        """
        Check if ChromaDB is available and can be initialized
        
        Returns:
            Tuple of (available, error_message)
        """
        if not CHROMADB_AVAILABLE:
            return False, "ChromaDB not installed"
        
        try:
            # Test import
            import chromadb
            from chromadb.config import Settings
            
            # Test client creation (in-memory)
            test_client = chromadb.Client(settings=Settings(anonymized_telemetry=False))
            test_collection = test_client.get_or_create_collection("test")
            test_collection.add(ids=["test"], documents=["test"])
            test_client.delete_collection("test")
            
            return True, None
        except Exception as e:
            return False, f"ChromaDB test failed: {str(e)}"
    
    def initialize_vector_db(self, persist_directory: str) -> Tuple[Optional[Any], Optional[str]]:
        """
        Initialize vector database with proper error handling
        
        Args:
            persist_directory: Directory for vector DB persistence
            
        Returns:
            Tuple of (vector_db_instance, error_message)
        """
        if not CHROMADB_AVAILABLE:
            return None, "ChromaDB not installed"
        
        try:
            from .vector_db import VectorDB
            
            # Ensure directory exists
            persist_path = Path(persist_directory)
            persist_path.mkdir(parents=True, exist_ok=True)
            
            # Initialize vector DB
            vector_db = VectorDB(str(persist_path))
            
            # Verify it works
            stats = vector_db.get_stats()
            
            self.status['components']['vector_db'] = 'ok'
            logger.info(f"Vector DB initialized: {stats['total_vectors']} vectors")
            return vector_db, None
            
        except ImportError as e:
            error_msg = f"ChromaDB not available: {e}"
            self.status['warnings'].append(error_msg)
            logger.warning(error_msg)
            return None, error_msg
        except Exception as e:
            error_msg = f"Vector DB initialization failed: {e}"
            self.status['warnings'].append(error_msg)
            logger.warning(error_msg)
            return None, error_msg
    
    def validate_database(self, db_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate database file and directory
        
        Args:
            db_path: Path to database file
            
        Returns:
            Tuple of (valid, error_message)
        """
        try:
            db_file = Path(db_path)
            db_dir = db_file.parent
            
            # Ensure directory exists
            db_dir.mkdir(parents=True, exist_ok=True)
            
            # Check if we can write to directory
            if not os.access(db_dir, os.W_OK):
                return False, f"No write access to directory: {db_dir}"
            
            # Check if file exists and is readable (if it exists)
            if db_file.exists() and not os.access(db_file, os.R_OK):
                return False, f"Database file not readable: {db_file}"
            
            return True, None
            
        except Exception as e:
            return False, f"Database validation failed: {e}"
    
    def get_startup_summary(self) -> Dict[str, Any]:
        """
        Get startup status summary
        
        Returns:
            Dictionary with startup status
        """
        return {
            'initialized': self.status['initialized'],
            'errors': self.status['errors'],
            'warnings': self.status['warnings'],
            'components': self.status['components'],
            'chromadb_available': CHROMADB_AVAILABLE
        }


def create_startup_manager() -> StartupManager:
    """Create and return a startup manager instance"""
    return StartupManager()

