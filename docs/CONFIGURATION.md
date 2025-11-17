# Configuration Guide

## Overview

This document describes all configuration options for the AI Pattern Detector system.

## Environment Variables

All configuration can be set via environment variables or modified in `ai_tools/config.py`.

### Detection Configuration

#### `SUPERHUMAN_SPEED_THRESHOLD`
- **Default**: `10.0`
- **Type**: Float
- **Description**: Requests per second threshold for superhuman speed detection
- **Example**: `export SUPERHUMAN_SPEED_THRESHOLD=5.0`

#### `ENUMERATION_SEQUENCE_LENGTH`
- **Default**: `5`
- **Type**: Integer
- **Description**: Minimum sequence length for enumeration detection
- **Example**: `export ENUMERATION_SEQUENCE_LENGTH=3`

#### `ANOMALY_Z_SCORE_THRESHOLD`
- **Default**: `2.0`
- **Type**: Float
- **Description**: Z-score threshold for anomaly detection (standard deviations)
- **Example**: `export ANOMALY_Z_SCORE_THRESHOLD=2.5`

### Request History Configuration

#### `MAX_HISTORY_SIZE`
- **Default**: `1000`
- **Type**: Integer
- **Description**: Maximum number of requests to keep in history
- **Example**: `export MAX_HISTORY_SIZE=2000`

#### `SPEED_WINDOW_SECONDS`
- **Default**: `10`
- **Type**: Integer
- **Description**: Time window (seconds) for speed calculation
- **Example**: `export SPEED_WINDOW_SECONDS=15`

### Dashboard Configuration

#### `DASHBOARD_REFRESH_RATE`
- **Default**: `2`
- **Type**: Integer
- **Description**: Dashboard refresh rate in seconds
- **Example**: `export DASHBOARD_REFRESH_RATE=5`

#### `MAX_DETECTIONS_DISPLAY`
- **Default**: `100`
- **Type**: Integer
- **Description**: Maximum detections to display in dashboard
- **Example**: `export MAX_DETECTIONS_DISPLAY=200`

### Simulation Configuration

#### `SIMULATION_RATE`
- **Default**: `1.0`
- **Type**: Float
- **Description**: Requests per second for simulation
- **Example**: `export SIMULATION_RATE=2.0`

#### `ATTACK_INTENSITY`
- **Default**: `0.1`
- **Type**: Float
- **Description**: Ratio of attack traffic (0.0 to 1.0)
- **Example**: `export ATTACK_INTENSITY=0.3`

### Ollama AI Configuration

#### `OLLAMA_ENABLED`
- **Default**: `true`
- **Type**: Boolean (string: "true"/"false")
- **Description**: Enable/disable Ollama AI features
- **Example**: `export OLLAMA_ENABLED=false`

#### `OLLAMA_HOST`
- **Default**: `http://localhost:11434`
- **Type**: String
- **Description**: Ollama server URL
- **Example**: `export OLLAMA_HOST=http://localhost:11434`

#### `OLLAMA_MODEL`
- **Default**: `llama3`
- **Type**: String
- **Description**: Ollama model name to use
- **Example**: `export OLLAMA_MODEL=llama3:8b`

#### `AI_ANALYSIS_ENABLED`
- **Default**: `true`
- **Type**: Boolean (string: "true"/"false")
- **Description**: Enable/disable AI analysis features
- **Example**: `export AI_ANALYSIS_ENABLED=false`

#### `AI_CACHE_ENABLED`
- **Default**: `true`
- **Type**: Boolean (string: "true"/"false")
- **Description**: Enable/disable AI response caching
- **Example**: `export AI_CACHE_ENABLED=false`

### Logging Configuration

#### `LOG_LEVEL`
- **Default**: `INFO`
- **Type**: String
- **Description**: Logging level (DEBUG, INFO, WARNING, ERROR)
- **Example**: `export LOG_LEVEL=DEBUG`

## Configuration File

Configuration can also be modified directly in `ai_tools/config.py`:

```python
class Config:
    # Detection thresholds
    SUPERHUMAN_SPEED_THRESHOLD = 10.0
    ENUMERATION_SEQUENCE_LENGTH = 5
    ANOMALY_Z_SCORE_THRESHOLD = 2.0
    
    # Ollama configuration
    OLLAMA_ENABLED = True
    OLLAMA_HOST = "http://localhost:11434"
    OLLAMA_MODEL = "llama3"
```

## Example Configuration Files

### Development Configuration

```bash
# .env.development
SUPERHUMAN_SPEED_THRESHOLD=5.0
LOG_LEVEL=DEBUG
OLLAMA_ENABLED=true
OLLAMA_MODEL=llama3:8b
```

### Production Configuration

```bash
# .env.production
SUPERHUMAN_SPEED_THRESHOLD=10.0
LOG_LEVEL=INFO
OLLAMA_ENABLED=true
OLLAMA_MODEL=llama3
MAX_HISTORY_SIZE=5000
```

### Testing Configuration

```bash
# .env.testing
SUPERHUMAN_SPEED_THRESHOLD=2.0
LOG_LEVEL=DEBUG
OLLAMA_ENABLED=false
SIMULATION_RATE=10.0
```

## Configuration Validation

Configuration values are validated on startup. Invalid values will:
1. Log a warning
2. Fall back to defaults
3. Continue operation

## Best Practices

1. **Start with Defaults**: Begin with default values and adjust based on your environment
2. **Monitor Performance**: Adjust thresholds based on actual traffic patterns
3. **Test Changes**: Test configuration changes in development before production
4. **Document Changes**: Document any custom configurations
5. **Use Environment Variables**: Prefer environment variables for deployment flexibility

## Troubleshooting

**Configuration not taking effect:**
- Ensure environment variables are set before importing modules
- Check for typos in variable names
- Verify configuration file syntax

**Ollama not connecting:**
- Verify `OLLAMA_HOST` is correct
- Check Ollama is running: `ollama list`
- Verify firewall allows connection

**Performance issues:**
- Reduce `MAX_HISTORY_SIZE` for lower memory usage
- Increase `DASHBOARD_REFRESH_RATE` for less frequent updates
- Adjust `SIMULATION_RATE` for slower traffic generation

---

**Last Updated**: 2025-01-XX
**Version**: 1.0

