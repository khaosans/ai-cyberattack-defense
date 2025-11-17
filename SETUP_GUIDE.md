# Setup Guide: AI Pattern Detector

This guide provides step-by-step instructions for setting up the AI Pattern Detector on your local machine.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Setup](#quick-setup)
- [Detailed Setup](#detailed-setup)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Optional Components](#optional-components)

## Prerequisites

### Required

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Usually included with Python
- **Git** - [Download Git](https://git-scm.com/downloads)

### Optional (for enhanced features)

- **Ollama** - For AI-powered threat analysis ([Download Ollama](https://ollama.ai))
- **ChromaDB** - For vector database features (installed via pip)

## Quick Setup

### Linux/macOS

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd Anthropic-Disrupting-agent-cyber-attack

# Run setup script
chmod +x setup.sh
./setup.sh

# Start the dashboard
streamlit run dashboard/app.py
```

### Windows

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd Anthropic-Disrupting-agent-cyber-attack

# Run setup script
setup.bat

# Start the dashboard
streamlit run dashboard\app.py
```

## Detailed Setup

### Step 1: Verify Python Installation

```bash
# Check Python version
python3 --version  # Linux/macOS
python --version   # Windows

# Should show Python 3.8 or higher
```

If Python is not installed or version is too old:
- **Linux**: `sudo apt-get install python3 python3-pip` (Ubuntu/Debian)
- **macOS**: `brew install python3` or download from [python.org](https://www.python.org/downloads/)
- **Windows**: Download from [python.org](https://www.python.org/downloads/)

### Step 2: Create Virtual Environment (Recommended)

Virtual environments isolate project dependencies and prevent conflicts.

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt when activated.

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install project dependencies
pip install -r ai_tools/requirements.txt
```

This installs:
- Streamlit (dashboard framework)
- Pandas (data processing)
- NumPy (numerical computing)
- Plotly (visualizations)
- scikit-learn (machine learning)
- Pydantic (data validation)
- Ollama (AI integration)
- ChromaDB (vector database)

### Step 4: Verify Installation

```bash
python3 check_environment.py  # Linux/macOS
python check_environment.py   # Windows
```

This script checks:
- ✅ Python version
- ✅ Required packages
- ✅ Project structure
- ✅ Module imports
- ⚠️ Optional components (Ollama, ChromaDB)

### Step 5: Start the Dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard will:
- Open automatically in your browser at `http://localhost:8501`
- Display the AI Pattern Detector interface
- Show real-time threat detection capabilities

## Platform-Specific Instructions

### Linux

**Ubuntu/Debian:**
```bash
# Install Python and pip
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# Run setup
./setup.sh
```

**Fedora/RHEL:**
```bash
# Install Python and pip
sudo dnf install python3 python3-pip

# Run setup
./setup.sh
```

### macOS

**Using Homebrew:**
```bash
# Install Python
brew install python3

# Run setup
./setup.sh
```

**Using Python.org installer:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. Run `./setup.sh`

### Windows

**Using Python installer:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. **Important**: Check "Add Python to PATH" during installation
3. Run `setup.bat` from Command Prompt or PowerShell

**Using Windows Store:**
```powershell
# Install Python from Microsoft Store
# Then run setup.bat
```

## Verification

### Quick Verification

Run the automated test suite:
```bash
python3 demo_dashboard.py  # Linux/macOS
python demo_dashboard.py   # Windows
```

Expected output:
```
✅ All critical tests passed!
Dashboard is ready for demo.
```

### Manual Verification

1. **Check Python version:**
   ```bash
   python3 --version  # Should be 3.8+
   ```

2. **Check installed packages:**
   ```bash
   pip list | grep streamlit
   pip list | grep pandas
   ```

3. **Test imports:**
   ```python
   python3 -c "from ai_tools.detection.ai_pattern_detector import AIPatternDetector; print('OK')"
   ```

4. **Start dashboard:**
   ```bash
   streamlit run dashboard/app.py
   ```
   Should open browser automatically.

## Troubleshooting

### Common Issues

#### "Python not found" or "python3: command not found"

**Solution:**
- Verify Python is installed: `python --version` or `python3 --version`
- Check PATH environment variable includes Python
- Reinstall Python and ensure "Add to PATH" is checked

#### "pip: command not found"

**Solution:**
```bash
# Linux/macOS
python3 -m ensurepip --upgrade

# Windows
python -m ensurepip --upgrade
```

#### "Permission denied" errors

**Solution:**
- Use virtual environment (recommended)
- Or use `pip install --user` for user-level installation

#### Import errors when running dashboard

**Solution:**
```bash
# Ensure you're in the repository root directory
cd Anthropic-Disrupting-agent-cyber-attack

# Verify project structure
ls ai_tools/
ls dashboard/

# Reinstall dependencies
pip install -r ai_tools/requirements.txt --force-reinstall
```

#### Dashboard won't start

**Solution:**
```bash
# Check Streamlit is installed
pip show streamlit

# Try explicit Python path
python3 -m streamlit run dashboard/app.py

# Check for port conflicts
# Dashboard uses port 8501 by default
```

#### "ModuleNotFoundError" errors

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r ai_tools/requirements.txt
```

#### ChromaDB installation fails

**Solution:**
```bash
# ChromaDB is optional - system works without it
# If you need it:
pip install chromadb --upgrade

# Or use the helper script
python3 install_vector_db.py
```

### Getting Help

1. **Check environment:**
   ```bash
   python3 check_environment.py
   ```

2. **Review logs:**
   - Dashboard errors appear in terminal
   - Check browser console (F12) for frontend errors

3. **Verify setup:**
   - Run `demo_dashboard.py` to test all components
   - Check `QUICKSTART.md` for basic usage

4. **Documentation:**
   - See `docs/README.md` for full documentation index
   - Check `docs/CONFIGURATION.md` for configuration options

## Optional Components

### Ollama Setup (AI Features)

Ollama enables AI-powered threat analysis and explanations.

**Installation:**
1. Download from [ollama.ai](https://ollama.ai)
2. Install and start Ollama service
3. Pull a model:
   ```bash
   ollama pull llama3.2:3b
   ```

**Verification:**
```bash
ollama list  # Should show installed models
python3 check_environment.py  # Should show Ollama as available
```

**Note:** Dashboard works without Ollama - AI features will use fallback mode.

### ChromaDB Setup (Vector Database)

ChromaDB enables threat correlation and similarity search.

**Installation:**
```bash
pip install chromadb
```

**Verification:**
```python
python3 -c "import chromadb; print('ChromaDB installed')"
```

**Note:** Vector DB features are optional - system works without them.

### Virtual Environment Best Practices

**Activate before working:**
```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**Deactivate when done:**
```bash
deactivate
```

**Recreate if needed:**
```bash
# Remove old environment
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# Create new
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r ai_tools/requirements.txt
```

## Next Steps

After successful setup:

1. **Read Quick Start:** [QUICKSTART.md](./QUICKSTART.md)
2. **Explore Dashboard:** Start with `streamlit run dashboard/app.py`
3. **Run Demo:** `python3 demo_dashboard.py`
4. **Read Documentation:** [docs/README.md](./docs/README.md)

## Support

For additional help:
- Check [Troubleshooting](#troubleshooting) section above
- Review [docs/README.md](./docs/README.md) for documentation
- Open an issue on GitHub
- Check [CHANGELOG.md](./CHANGELOG.md) for recent changes

---

**Last Updated:** November 2025  
**Setup Script Version:** 2.0

