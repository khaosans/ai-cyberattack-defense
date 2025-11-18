#!/usr/bin/env python3
"""
Environment check script for AI Pattern Detector
Verifies all dependencies and configuration
"""
import sys
import subprocess

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Found: {version.major}.{version.minor}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    import_name = import_name or package_name
    try:
        __import__(import_name)
        print(f"✓ {package_name} installed")
        return True
    except ImportError:
        print(f"❌ {package_name} not installed")
        return False

def check_ollama_server():
    """Check if Ollama server is running"""
    try:
        from ollama import Client
        client = Client()
        result = client.list()
        # Handle ListResponse object
        if hasattr(result, 'models'):
            models = result.models
            model_names = [m.model if hasattr(m, 'model') else str(m) for m in models[:3]]
        elif isinstance(result, dict):
            models = result.get('models', [])
            model_names = [m.get('name', 'unknown') for m in models[:3]]
        else:
            models = []
            model_names = []
        
        print(f"✓ Ollama server running")
        if model_names:
            print(f"  Available models: {', '.join(model_names)}")
        return True
    except Exception as e:
        print(f"⚠ Ollama server not accessible: {e}")
        print("  (This is optional - AI features will use fallback)")
        return False

def check_ollama_package():
    """Check if Ollama Python package is installed"""
    try:
        from ollama import Client
        client = Client()
        # Try to list models
        result = client.list()
        print(f"✓ Ollama Python package installed and working")
        return True
    except ImportError:
        print(f"❌ Ollama Python package not installed")
        print("  Install with: pip install ollama")
        return False
    except Exception as e:
        print(f"⚠ Ollama package installed but connection failed: {e}")
        return False

def check_project_structure():
    """Check if project structure is correct"""
    import os
    required_dirs = ['ai_tools', 'dashboard', 'docs']
    required_files = ['ai_tools/config.py', 'dashboard/app.py']
    
    all_good = True
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✓ {dir_name}/ directory exists")
        else:
            print(f"❌ {dir_name}/ directory missing")
            all_good = False
    
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✓ {file_name} exists")
        else:
            print(f"❌ {file_name} missing")
            all_good = False
    
    return all_good

def check_imports():
    """Check if core modules can be imported"""
    try:
        from ai_tools.detection.ai_pattern_detector import AIPatternDetector
        from ai_tools.detection.enhanced_detector import EnhancedAIPatternDetector
        from ai_tools.simulation.attack_simulator import AttackSimulator
        from ai_tools.config import Config
        print("✓ Core modules import successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("AI Pattern Detector - Environment Check")
    print("=" * 60)
    print()
    
    checks = []
    
    print("Python Environment:")
    checks.append(check_python_version())
    print()
    
    print("Project Structure:")
    checks.append(check_project_structure())
    print()
    
    print("Python Packages:")
    packages = [
        ('streamlit', 'streamlit'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('plotly', 'plotly'),
        ('scikit-learn', 'sklearn'),
        ('pydantic', 'pydantic'),
    ]
    for pkg_name, import_name in packages:
        checks.append(check_package(pkg_name, import_name))
    print()
    
    print("Ollama (Optional - for AI features):")
    ollama_pkg = check_ollama_package()
    ollama_server = check_ollama_server()
    print()
    
    print("Module Imports:")
    checks.append(check_imports())
    print()
    
    print("=" * 60)
    if all(checks):
        print("✓ All required checks passed!")
        if ollama_pkg and ollama_server:
            print("✓ Ollama AI features ready!")
        else:
            print("⚠ Ollama not available - AI features will use fallback")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

