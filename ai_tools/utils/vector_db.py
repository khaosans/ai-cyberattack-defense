"""
Vector Database for Threat Correlation and Similarity Search
Uses ChromaDB for storing detection embeddings
"""
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

from .models import Detection


class VectorDB:
    """Vector database for threat similarity search and correlation"""
    
    def __init__(self, persist_directory: str = "chroma_db"):
        """
        Initialize ChromaDB vector database
        
        Args:
            persist_directory: Directory to persist ChromaDB data
            
        Raises:
            ImportError: If ChromaDB is not installed
            Exception: If initialization fails
        """
        if not CHROMADB_AVAILABLE:
            raise ImportError("ChromaDB not installed. Install with: pip install chromadb")
        
        self.persist_directory = Path(persist_directory)
        
        # Ensure directory exists with proper permissions
        try:
            self.persist_directory.mkdir(parents=True, exist_ok=True)
            
            # Verify directory is writable
            if not os.access(self.persist_directory, os.W_OK):
                raise PermissionError(f"Cannot write to directory: {self.persist_directory}")
        except Exception as e:
            raise Exception(f"Failed to create vector DB directory: {e}")
        
        # Initialize ChromaDB client with error handling
        try:
            self.client = chromadb.PersistentClient(
                path=str(self.persist_directory),
                settings=Settings(anonymized_telemetry=False)
            )
        except Exception as e:
            raise Exception(f"Failed to create ChromaDB client: {e}")
        
        # Get or create collection with error handling
        try:
            self.collection = self.client.get_or_create_collection(
                name="detections",
                metadata={"description": "Threat detection embeddings"}
            )
        except Exception as e:
            raise Exception(f"Failed to create/get collection: {e}")
    
    def _create_embedding(self, detection: Detection) -> List[float]:
        """
        Create embedding vector from detection
        
        Args:
            detection: Detection object
            
        Returns:
            Embedding vector as list of floats
        """
        # Create feature vector from detection characteristics
        features = []
        
        # 1. Endpoint pattern features (normalized)
        endpoint = detection.request.endpoint
        # Extract base path (remove IDs/parameters)
        base_path = endpoint.split('?')[0].split('/')
        # Normalize numeric IDs to placeholder
        normalized_path = '/'.join(['ID' if part.isdigit() else part for part in base_path])
        features.extend(self._text_to_features(normalized_path))
        
        # 2. Threat pattern features
        pattern_type = detection.pattern_type.value
        threat_level = detection.threat_level.value
        threat_score = detection.threat_score / 100.0  # Normalize to 0-1
        
        # Encode pattern type
        pattern_features = [0.0] * 4  # normal, superhuman_speed, systematic_enumeration, behavioral_anomaly
        pattern_map = {
            'normal': 0,
            'superhuman_speed': 1,
            'systematic_enumeration': 2,
            'behavioral_anomaly': 3
        }
        if pattern_type in pattern_map:
            pattern_features[pattern_map[pattern_type]] = 1.0
        features.extend(pattern_features)
        
        # Encode threat level
        level_features = [0.0] * 3  # normal, suspicious, malicious
        level_map = {'normal': 0, 'suspicious': 1, 'malicious': 2}
        if threat_level in level_map:
            level_features[level_map[threat_level]] = 1.0
        features.extend(level_features)
        
        features.append(threat_score)
        
        # 3. Detection details features
        if detection.details:
            details = detection.details
            
            # Speed detection features
            if 'speed_detection' in details:
                speed = details['speed_detection']
                features.append(1.0 if speed.get('detected', False) else 0.0)
                features.append(min(speed.get('requests_per_second', 0) / 100.0, 1.0))  # Normalize
            else:
                features.extend([0.0, 0.0])
            
            # Enumeration detection features
            if 'enumeration_detection' in details:
                enum = details['enumeration_detection']
                features.append(1.0 if enum.get('detected', False) else 0.0)
                features.append(min(enum.get('sequence_length', 0) / 20.0, 1.0))  # Normalize
            else:
                features.extend([0.0, 0.0])
            
            # Anomaly detection features
            if 'anomaly_detection' in details:
                anomaly = details['anomaly_detection']
                features.append(1.0 if anomaly.get('detected', False) else 0.0)
                features.append(min(anomaly.get('z_score', 0) / 10.0, 1.0))  # Normalize
            else:
                features.extend([0.0, 0.0])
        else:
            features.extend([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        
        # 4. IP address features (hash-based for similarity)
        ip_hash = hash(detection.request.ip_address) % 1000 / 1000.0
        features.append(ip_hash)
        
        # 5. Method features
        method_map = {'GET': 0.0, 'POST': 0.5, 'PUT': 0.75, 'DELETE': 1.0}
        method_val = method_map.get(detection.request.method, 0.0)
        features.append(method_val)
        
        # Pad or truncate to fixed size (64 dimensions)
        target_size = 64
        if len(features) < target_size:
            features.extend([0.0] * (target_size - len(features)))
        elif len(features) > target_size:
            features = features[:target_size]
        
        return features
    
    def _text_to_features(self, text: str) -> List[float]:
        """Convert text to feature vector using simple character frequency"""
        # Simple character frequency-based features
        features = [0.0] * 10
        if not text:
            return features
        
        # Character frequency features
        chars = text.lower()
        for i, char in enumerate(chars[:10]):
            if i < len(features):
                features[i] = ord(char) % 100 / 100.0
        
        return features
    
    def save_detection(self, detection: Detection, detection_id: Optional[int] = None) -> str:
        """
        Save detection embedding to vector database
        
        Args:
            detection: Detection object
            detection_id: Optional database ID for reference
            
        Returns:
            Vector DB document ID
        """
        # Create embedding
        embedding = self._create_embedding(detection)
        
        # Create document ID
        doc_id = f"detection_{detection_id}" if detection_id else f"det_{detection.timestamp.isoformat()}"
        
        # Prepare metadata
        metadata = {
            "timestamp": detection.timestamp.isoformat(),
            "threat_level": detection.threat_level.value,
            "pattern_type": detection.pattern_type.value,
            "threat_score": str(detection.threat_score),
            "endpoint": detection.request.endpoint[:200],  # Limit length
            "ip_address": detection.request.ip_address,
            "method": detection.request.method,
            "detection_id": str(detection_id) if detection_id else ""
        }
        
        # Add to collection
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            metadatas=[metadata],
            documents=[f"{detection.pattern_type.value} attack on {detection.request.endpoint}"]
        )
        
        return doc_id
    
    def find_similar(self, detection: Detection, limit: int = 5, min_score: float = 0.5) -> List[Dict[str, Any]]:
        """
        Find similar detections
        
        Args:
            detection: Detection to find similar ones for
            limit: Maximum number of results
            min_score: Minimum similarity score (0-1)
            
        Returns:
            List of similar detections with scores
        """
        # Create embedding for query detection
        query_embedding = self._create_embedding(detection)
        
        # Query collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit + 1,  # +1 to exclude the detection itself
            include=["metadatas", "distances", "documents"]
        )
        
        # Process results
        similar = []
        if results['ids'] and len(results['ids'][0]) > 0:
            for i, (doc_id, metadata, distance, document) in enumerate(zip(
                results['ids'][0],
                results['metadatas'][0],
                results['distances'][0],
                results['documents'][0]
            )):
                # Convert distance to similarity score (ChromaDB uses cosine distance)
                similarity = 1.0 - distance  # Cosine distance -> similarity
                
                if similarity >= min_score:
                    similar.append({
                        "id": doc_id,
                        "similarity": round(similarity, 3),
                        "metadata": metadata,
                        "document": document,
                        "distance": distance
                    })
        
        return similar
    
    def get_threat_clusters(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get threat clusters (grouped similar attacks)
        
        Args:
            limit: Maximum number of clusters
            
        Returns:
            List of clusters with representative detections
        """
        # Get all detections
        all_results = self.collection.get(include=["metadatas", "embeddings"])
        
        if not all_results['ids'] or len(all_results['ids']) < 2:
            return []
        
        # Simple clustering: find groups of similar detections
        clusters = []
        processed = set()
        
        for i, doc_id in enumerate(all_results['ids']):
            if doc_id in processed:
                continue
            
            # Find similar to this detection
            embedding = all_results['embeddings'][i]
            similar = self.collection.query(
                query_embeddings=[embedding],
                n_results=limit,
                include=["metadatas", "distances"]
            )
            
            if similar['ids'] and len(similar['ids'][0]) > 0:
                cluster_members = []
                for j, (sid, metadata, distance) in enumerate(zip(
                    similar['ids'][0],
                    similar['metadatas'][0],
                    similar['distances'][0]
                )):
                    similarity = 1.0 - distance
                    if similarity >= 0.7:  # High similarity threshold for clusters
                        cluster_members.append({
                            "id": sid,
                            "similarity": round(similarity, 3),
                            "metadata": metadata
                        })
                        processed.add(sid)
                
                if len(cluster_members) > 1:  # Only clusters with multiple members
                    clusters.append({
                        "size": len(cluster_members),
                        "members": cluster_members,
                        "representative": cluster_members[0]  # First member as representative
                    })
        
        return clusters[:limit]
    
    def clear_old(self, days: int = 7):
        """
        Clear old detections from vector database
        
        Args:
            days: Number of days to keep
        """
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        cutoff_iso = datetime.fromtimestamp(cutoff).isoformat()
        
        # Get all detections
        all_results = self.collection.get(include=["metadatas"])
        
        ids_to_delete = []
        if all_results['ids']:
            for doc_id, metadata in zip(all_results['ids'], all_results['metadatas']):
                if metadata.get('timestamp', '') < cutoff_iso:
                    ids_to_delete.append(doc_id)
        
        if ids_to_delete:
            self.collection.delete(ids=ids_to_delete)
        
        return len(ids_to_delete)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector database statistics"""
        count = self.collection.count()
        return {
            "total_vectors": count,
            "collection_name": "detections"
        }

