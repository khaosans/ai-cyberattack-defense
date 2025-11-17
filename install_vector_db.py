#!/usr/bin/env python3
"""
Helper script to install ChromaDB for vector database features
"""
import subprocess
import sys

def install_chromadb():
    """Install ChromaDB"""
    print("Installing ChromaDB...")
    # Try different installation methods
    methods = [
        [sys.executable, "-m", "pip", "install", "--user", "chromadb", "--quiet"],
        [sys.executable, "-m", "pip", "install", "chromadb", "--break-system-packages", "--quiet"],
        [sys.executable, "-m", "pip", "install", "chromadb", "--quiet"],
    ]
    
    for method in methods:
        try:
            subprocess.check_call(method, stderr=subprocess.DEVNULL)
            print("✓ ChromaDB installed successfully")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    print("✗ Failed to install ChromaDB with standard methods")
    print("\nTry one of these:")
    print("  1. pip install --user chromadb")
    print("  2. python3 -m venv venv && source venv/bin/activate && pip install chromadb")
    print("  3. pip install chromadb --break-system-packages")
    return False

def test_installation():
    """Test ChromaDB installation"""
    try:
        import chromadb
        from ai_tools.utils.vector_db import VectorDB
        print("✓ ChromaDB imports successfully")
        
        # Test initialization
        import tempfile
        import shutil
        temp_dir = tempfile.mkdtemp()
        try:
            vdb = VectorDB(temp_dir)
            print("✓ VectorDB initialized successfully")
            stats = vdb.get_stats()
            print(f"✓ Vector DB stats: {stats}")
        finally:
            shutil.rmtree(temp_dir)
        
        return True
    except ImportError as e:
        print(f"✗ ChromaDB not available: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("ChromaDB Installation Helper")
    print("=" * 60)
    print()
    
    # Test if already installed
    if test_installation():
        print("\n✓ ChromaDB is already installed and working!")
        sys.exit(0)
    
    # Try to install
    print("\nChromaDB not found. Installing...")
    if install_chromadb():
        print("\nTesting installation...")
        if test_installation():
            print("\n✅ ChromaDB installed and working!")
            print("Vector database features are now enabled.")
        else:
            print("\n⚠️ Installation completed but test failed.")
            print("Try restarting the dashboard.")
    else:
        print("\n⚠️ Installation failed.")
        print("Vector database features will be disabled.")
        print("The dashboard will work without vector DB features.")

