# AI Pattern Detector Dashboard

Interactive Streamlit dashboard for real-time detection of GTG-1002 style autonomous AI attacks.

## Features

- **Real-time Threat Detection**: Continuously analyzes requests for AI-driven attack patterns
- **🤖 AI-Enhanced Analysis**: Ollama LLM integration for natural language threat explanations and recommendations
- **Interactive Visualizations**: Threat timeline, pattern distribution, and threat level gauge
- **Alert Feed**: Real-time alerts with AI-powered explanations
- **AI Security Assistant**: Ask questions about threats and get AI-powered answers
- **Attack Simulation**: Built-in simulator to test detection capabilities
- **Export Functionality**: Download detection logs as CSV

## Installation

1. Install dependencies:
```bash
pip install -r ../ai_tools/requirements.txt
```

2. **Optional: Install Ollama for AI features**:
```bash
# Download Ollama from https://ollama.ai
# Pull a model (recommended: llama3)
ollama pull llama3
```

## Usage

Start the dashboard:
```bash
streamlit run dashboard/app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Dashboard Components

### Controls Panel (Sidebar)
- **🤖 AI Features**: Enable/disable Ollama LLM integration
  - Shows Ollama connection status
  - Displays active model name
- **Start/Stop Simulation**: Control traffic generation
- **Trigger Attack**: Simulate GTG-1002 style attack
- **Configuration**: Adjust detection thresholds
- **Reset**: Clear detection history
- **Export**: Download detection logs

### Main Dashboard

#### Metrics Panel
- Total detections count
- Malicious threats count
- Average threat score
- Peak threat score

#### Visualizations
1. **Threat Timeline**: Line chart showing threat scores over time
2. **Threat Gauge**: Current threat level indicator
3. **Pattern Distribution**: Bar chart of detected attack patterns

#### Alert Feed
Real-time alerts for:
- Superhuman speed detections
- Systematic enumeration patterns
- Behavioral anomalies
- **AI Insights**: Click "🤖 AI Insights" button on any alert for:
  - Natural language threat explanation
  - Intent classification (reconnaissance, enumeration, etc.)
  - Prioritized security recommendations
  - Attack scenario description

#### Recent Detections Table
Detailed view of recent detections with:
- Timestamp
- Threat score
- Threat level
- Pattern type
- Endpoint
- Source IP

#### AI Security Recommendations Panel
When AI is enabled and malicious detections occur:
- Prioritized security recommendations
- Pattern-specific actions
- High/medium priority indicators

#### Security Assistant
Collapsible Q&A interface:
- Ask questions about threats, detection logic, or security
- Get AI-powered answers with sources
- Context-aware responses based on current detections

## Understanding the Visualizations

### Threat Score Timeline
- **Green dots**: Normal traffic (score < 30)
- **Orange dots**: Suspicious activity (score 30-70)
- **Red dots**: Malicious attacks (score > 70)

### Threat Gauge
- **Green zone**: Low threat (0-30)
- **Yellow zone**: Medium threat (30-70)
- **Red zone**: High threat (70-100)

### Pattern Types
- **superhuman_speed**: Requests occurring at impossible human speeds
- **systematic_enumeration**: Sequential endpoint discovery
- **behavioral_anomaly**: Statistical anomalies in request patterns
- **normal**: Normal traffic patterns

## Configuration

Adjust detection sensitivity in the sidebar:
- **Superhuman Speed Threshold**: Requests per second threshold (default: 10 req/s)
- **Attack Intensity**: Ratio of attack traffic in simulation (0.0 to 1.0)

## Best Practices

1. **Enable AI Features**: Check "Enable AI Analysis" for enhanced threat insights (requires Ollama)
2. **Start with Normal Traffic**: Begin simulation to establish baseline
3. **Trigger Attack**: Use "Trigger Attack" button to simulate GTG-1002 attack
4. **Monitor Alerts**: Watch alert feed for real-time threat notifications
5. **Use AI Insights**: Click "🤖 AI Insights" on alerts for detailed analysis
6. **Ask Security Assistant**: Use Q&A interface for security questions
7. **Adjust Thresholds**: Fine-tune detection sensitivity based on your environment
8. **Export Logs**: Download detection logs for further analysis

## Troubleshooting

**Dashboard not updating:**
- Ensure simulation is running (click "Start Simulation")
- Check browser console for errors

**No detections:**
- Start simulation to generate traffic
- Trigger attack to see detection in action
- Adjust thresholds if needed

**Performance issues:**
- Reduce detection history size in config
- Limit displayed detections in sidebar

**AI features not working:**
- Ensure Ollama is installed and running: `ollama --version`
- Check model is pulled: `ollama list`
- Verify Ollama server is accessible: `curl http://localhost:11434/api/tags`
- See [AI Integration Guide](../docs/ai_integration_guide.md) for troubleshooting

## Technical Details

- **Refresh Rate**: 2 seconds (configurable)
- **Detection Window**: 10 minutes for timeline visualization
- **Max Detections**: 1000 (keeps last 1000 detections)
- **Alert Limit**: 20 most recent alerts displayed

