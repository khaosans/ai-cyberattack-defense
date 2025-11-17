"""
SQLite database for persistent detection storage
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from .models import Detection, Request, ThreatLevel, PatternType

# Import vector DB (optional)
try:
    from .vector_db import VectorDB
    VECTOR_DB_AVAILABLE = True
except ImportError:
    VECTOR_DB_AVAILABLE = False
    VectorDB = None


class DetectionDB:
    """SQLite database for storing detections"""
    
    def __init__(self, db_path: str = "detections.db", enable_vector_db: bool = True):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
            enable_vector_db: Whether to enable vector database for similarity search
        """
        self.db_path = db_path
        db_file = Path(db_path)
        
        # Ensure directory exists
        db_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize SQLite connection
        try:
            self.conn = sqlite3.connect(db_path, check_same_thread=False, timeout=10.0)
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
            self._create_tables()
        except sqlite3.Error as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"SQLite initialization failed: {e}")
            raise
        
        # Initialize vector database if available
        self.vector_db = None
        self.vector_db_status = "disabled"
        
        if enable_vector_db:
            if VECTOR_DB_AVAILABLE:
                try:
                    vector_db_path = Path(db_path).parent / "chroma_db"
                    # Ensure vector DB directory exists
                    vector_db_path.mkdir(parents=True, exist_ok=True)
                    
                    # Initialize vector DB
                    self.vector_db = VectorDB(str(vector_db_path))
                    
                    # Verify initialization
                    stats = self.vector_db.get_stats()
                    self.vector_db_status = "active"
                    
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.info(f"Vector DB initialized: {stats['total_vectors']} vectors")
                except Exception as e:
                    # Vector DB is optional, continue without it
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f"Vector DB initialization failed: {e}")
                    self.vector_db_status = f"failed: {str(e)[:50]}"
            else:
                self.vector_db_status = "chromadb_not_installed"
    
    def _create_tables(self):
        """Create database tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Detections table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                threat_score INTEGER NOT NULL,
                threat_level TEXT NOT NULL,
                pattern_type TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                method TEXT,
                user_agent TEXT,
                parameters TEXT,
                details TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON detections(timestamp)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_threat_level ON detections(threat_level)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_pattern_type ON detections(pattern_type)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_ip_address ON detections(ip_address)
        """)
        
        self.conn.commit()
    
    def _serialize_json(self, obj: Any) -> Optional[str]:
        """Safely serialize object to JSON string"""
        if obj is None:
            return None
        try:
            # Convert non-serializable types
            def json_serializer(obj):
                if isinstance(obj, (datetime,)):
                    return obj.isoformat()
                elif isinstance(obj, (bool,)):
                    return bool(obj)
                elif isinstance(obj, (int, float, str, type(None))):
                    return obj
                elif isinstance(obj, dict):
                    return {k: json_serializer(v) for k, v in obj.items()}
                elif isinstance(obj, (list, tuple)):
                    return [json_serializer(item) for item in obj]
                else:
                    return str(obj)
            
            serializable = json_serializer(obj)
            return json.dumps(serializable)
        except Exception:
            return json.dumps(str(obj))
    
    def save_detection(self, detection: Detection) -> int:
        """
        Save a detection to the database
        
        Args:
            detection: Detection object to save
            
        Returns:
            ID of the saved detection
        """
        cursor = self.conn.cursor()
        
        # Serialize details and parameters
        details_json = self._serialize_json(detection.details) if detection.details else None
        params_json = self._serialize_json(detection.request.parameters) if detection.request.parameters else None
        
        cursor.execute("""
            INSERT INTO detections (
                timestamp, threat_score, threat_level, pattern_type,
                endpoint, ip_address, method, user_agent, parameters, details
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            detection.timestamp.isoformat(),
            detection.threat_score,
            detection.threat_level.value,
            detection.pattern_type.value,
            detection.request.endpoint,
            detection.request.ip_address,
            detection.request.method,
            detection.request.user_agent,
            params_json,
            details_json
        ))
        
        self.conn.commit()
        detection_id = cursor.lastrowid
        
        # Save to vector database if available
        if self.vector_db:
            try:
                self.vector_db.save_detection(detection, detection_id=detection_id)
            except Exception as e:
                # Vector DB is optional, log but don't fail
                import logging
                logging.getLogger(__name__).warning(f"Failed to save to vector DB: {e}")
        
        return detection_id
    
    def get_recent_detections(self, limit: int = 100, minutes: Optional[int] = None) -> List[Detection]:
        """
        Get recent detections
        
        Args:
            limit: Maximum number of detections to return
            minutes: Optional time window in minutes
            
        Returns:
            List of Detection objects
        """
        cursor = self.conn.cursor()
        
        if minutes:
            cutoff = (datetime.now().timestamp() - (minutes * 60))
            cutoff_iso = datetime.fromtimestamp(cutoff).isoformat()
            cursor.execute("""
                SELECT * FROM detections
                WHERE timestamp >= ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (cutoff_iso, limit))
        else:
            cursor.execute("""
                SELECT * FROM detections
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
        
        rows = cursor.fetchall()
        return [self._row_to_detection(row) for row in rows]
    
    def get_detections_by_threat_level(self, threat_level: str, limit: int = 100) -> List[Detection]:
        """
        Get detections by threat level
        
        Args:
            threat_level: Threat level (normal, suspicious, malicious)
            limit: Maximum number of detections to return
            
        Returns:
            List of Detection objects
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM detections
            WHERE threat_level = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (threat_level, limit))
        
        rows = cursor.fetchall()
        return [self._row_to_detection(row) for row in rows]
    
    def get_statistics(self, minutes: Optional[int] = None) -> Dict[str, Any]:
        """
        Get detection statistics
        
        Args:
            minutes: Optional time window in minutes
            
        Returns:
            Dictionary with statistics
        """
        cursor = self.conn.cursor()
        
        if minutes:
            cutoff = (datetime.now().timestamp() - (minutes * 60))
            cutoff_iso = datetime.fromtimestamp(cutoff).isoformat()
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN threat_level = 'normal' THEN 1 ELSE 0 END) as normal_count,
                    SUM(CASE WHEN threat_level = 'suspicious' THEN 1 ELSE 0 END) as suspicious_count,
                    SUM(CASE WHEN threat_level = 'malicious' THEN 1 ELSE 0 END) as malicious_count,
                    AVG(threat_score) as avg_score,
                    MAX(threat_score) as max_score
                FROM detections
                WHERE timestamp >= ?
            """, (cutoff_iso,))
        else:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN threat_level = 'normal' THEN 1 ELSE 0 END) as normal_count,
                    SUM(CASE WHEN threat_level = 'suspicious' THEN 1 ELSE 0 END) as suspicious_count,
                    SUM(CASE WHEN threat_level = 'malicious' THEN 1 ELSE 0 END) as malicious_count,
                    AVG(threat_score) as avg_score,
                    MAX(threat_score) as max_score
                FROM detections
            """)
        
        row = cursor.fetchone()
        return {
            "total_detections": row["total"] or 0,
            "normal_count": row["normal_count"] or 0,
            "suspicious_count": row["suspicious_count"] or 0,
            "malicious_count": row["malicious_count"] or 0,
            "avg_threat_score": round(row["avg_score"] or 0, 1),
            "peak_threat_score": row["max_score"] or 0
        }
    
    def get_pattern_distribution(self, minutes: Optional[int] = None) -> Dict[str, int]:
        """
        Get pattern type distribution
        
        Args:
            minutes: Optional time window in minutes
            
        Returns:
            Dictionary mapping pattern types to counts
        """
        cursor = self.conn.cursor()
        
        if minutes:
            cutoff = (datetime.now().timestamp() - (minutes * 60))
            cutoff_iso = datetime.fromtimestamp(cutoff).isoformat()
            cursor.execute("""
                SELECT pattern_type, COUNT(*) as count
                FROM detections
                WHERE timestamp >= ?
                GROUP BY pattern_type
            """, (cutoff_iso,))
        else:
            cursor.execute("""
                SELECT pattern_type, COUNT(*) as count
                FROM detections
                GROUP BY pattern_type
            """)
        
        rows = cursor.fetchall()
        return {row["pattern_type"]: row["count"] for row in rows}
    
    def clear_old_detections(self, days: int = 7):
        """
        Clear detections older than specified days
        
        Args:
            days: Number of days to keep
        """
        cutoff = (datetime.now().timestamp() - (days * 24 * 60 * 60))
        cutoff_iso = datetime.fromtimestamp(cutoff).isoformat()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM detections
            WHERE timestamp < ?
        """, (cutoff_iso,))
        
        self.conn.commit()
        return cursor.rowcount
    
    def _row_to_detection(self, row: sqlite3.Row) -> Detection:
        """Convert database row to Detection object"""
        # Parse timestamp
        timestamp = datetime.fromisoformat(row["timestamp"])
        
        # Parse request parameters
        parameters = None
        if row["parameters"]:
            try:
                parameters = json.loads(row["parameters"])
            except:
                parameters = None
        
        # Parse details
        details = None
        if row["details"]:
            try:
                details = json.loads(row["details"])
            except:
                details = None
        
        # Create Request object
        request = Request(
            timestamp=timestamp,
            endpoint=row["endpoint"],
            ip_address=row["ip_address"],
            method=row["method"] or "GET",
            user_agent=row["user_agent"] or "",
            parameters=parameters
        )
        
        # Create Detection object
        detection = Detection(
            timestamp=timestamp,
            request=request,
            threat_score=row["threat_score"],
            threat_level=ThreatLevel(row["threat_level"]),
            pattern_type=PatternType(row["pattern_type"]),
            details=details
        )
        
        return detection
    
    def find_similar_detections(self, detection: Detection, limit: int = 5) -> List[Detection]:
        """
        Find similar detections using vector database
        
        Args:
            detection: Detection to find similar ones for
            limit: Maximum number of results
            
        Returns:
            List of similar Detection objects
        """
        if not self.vector_db:
            return []
        
        try:
            similar = self.vector_db.find_similar(detection, limit=limit)
            similar_detections = []
            
            for item in similar:
                # Get detection from SQLite using metadata
                detection_id = item['metadata'].get('detection_id')
                if detection_id:
                    cursor = self.conn.cursor()
                    cursor.execute("SELECT * FROM detections WHERE id = ?", (detection_id,))
                    row = cursor.fetchone()
                    if row:
                        similar_detections.append(self._row_to_detection(row))
            
            return similar_detections
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Similarity search failed: {e}")
            return []
    
    def get_threat_clusters(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get threat clusters (grouped similar attacks)
        
        Args:
            limit: Maximum number of clusters
            
        Returns:
            List of clusters
        """
        if not self.vector_db:
            return []
        
        try:
            return self.vector_db.get_threat_clusters(limit=limit)
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Clustering failed: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

