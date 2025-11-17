# Glossary

## Terms and Definitions

### A

**AI-Orchestrated Attack**: A cyberattack where artificial intelligence systems autonomously execute attack phases with minimal human intervention.

**Anomaly Detection**: Statistical method for identifying unusual patterns in data that deviate from expected behavior.

**Attack Simulator**: Component that generates realistic network traffic patterns for testing detection capabilities.

### B

**Behavioral Anomaly**: Unusual request patterns detected through statistical analysis, such as unexpected endpoint depths or parameter counts.

### D

**Detection**: Result of analyzing a request for threat indicators, including threat score, level, and pattern type.

**Dashboard**: Interactive web interface (Streamlit) for real-time threat visualization and monitoring.

### E

**Enhanced Detector**: AI-enhanced version of the pattern detector that combines rule-based detection with LLM analysis.

**Enumeration**: Systematic discovery of endpoints or resources through sequential access patterns.

### G

**GTG-1002**: Threat actor designation for the first documented AI-orchestrated cyber espionage campaign (Anthropic, 2025).

### I

**Intent Classification**: AI-powered classification of request intent (reconnaissance, enumeration, exploitation, etc.).

**Isolation Forest**: Unsupervised machine learning algorithm used for anomaly detection.

### M

**MCP (Model Context Protocol)**: Protocol used by threat actors to manipulate AI models through context injection.

**Malicious**: Threat level indicating high-threat attacks (score 70-100).

### O

**Ollama**: Local LLM runtime for running large language models without cloud dependencies.

**OllamaClient**: Wrapper class for integrating Ollama LLM capabilities into the detection system.

### P

**Pattern Type**: Classification of detected attack patterns:
- **Normal**: No threat detected
- **Superhuman Speed**: Requests occurring at impossible human speeds
- **Systematic Enumeration**: Sequential endpoint discovery
- **Behavioral Anomaly**: Statistical outliers

### R

**Request**: HTTP request representation containing timestamp, IP address, endpoint, method, and user agent.

**Rule-Based Detection**: Detection method using predefined rules and thresholds rather than AI analysis.

### S

**Security Assistant**: AI-powered Q&A interface for answering security questions and providing recommendations.

**Superhuman Speed**: Request rate exceeding human capabilities (typically > 10 requests/second).

**Suspicious**: Threat level indicating medium-threat activity (score 30-69).

**Systematic Enumeration**: Pattern of sequential endpoint access indicating automated discovery.

### T

**Threat Analyzer**: AI component that provides enhanced threat analysis using LLM capabilities.

**Threat Level**: Classification of threat severity:
- **Normal**: Low threat (score 0-29)
- **Suspicious**: Medium threat (score 30-69)
- **Malicious**: High threat (score 70-100)

**Threat Score**: Numerical score (0-100) indicating threat severity based on detected patterns.

### References

- Anthropic. (2025, November 17). *Disrupting the first reported AI-orchestrated cyber espionage campaign* [Threat Intelligence Report]. Anthropic. https://www.anthropic.com/research/disrupting-ai-cyber-espionage

---

**Last Updated**: 2025-01-XX
**Version**: 1.0

