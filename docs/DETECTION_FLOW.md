# Detection Algorithm Flow

## Overview

This document describes the detection algorithm flow, decision trees, and threat scoring process for the AI Pattern Detector.

## Request Analysis Flow

```mermaid
flowchart TD
    START[HTTP Request Received] --> PARSE[Parse Request Data]
    PARSE --> STORE[Store in Request History]
    STORE --> SPEED[Check Superhuman Speed]
    SPEED --> SPEED_DETECT{Speed Detected?}
    SPEED_DETECT -->|Yes| SPEED_SCORE[Calculate Speed Score]
    SPEED_DETECT -->|No| ENUM[Check Enumeration]
    SPEED_SCORE --> ENUM
    ENUM --> ENUM_DETECT{Enumeration Detected?}
    ENUM_DETECT -->|Yes| ENUM_SCORE[Calculate Enumeration Score]
    ENUM_DETECT -->|No| ANOMALY[Check Behavioral Anomaly]
    ENUM_SCORE --> ANOMALY
    ANOMALY --> ANOMALY_DETECT{Anomaly Detected?}
    ANOMALY_DETECT -->|Yes| ANOMALY_SCORE[Calculate Anomaly Score]
    ANOMALY_DETECT -->|No| COMBINE[Combine Scores]
    ANOMALY_SCORE --> COMBINE
    COMBINE --> TOTAL[Calculate Total Threat Score]
    TOTAL --> LEVEL[Determine Threat Level]
    LEVEL --> PATTERN[Determine Pattern Type]
    PATTERN --> RETURN[Return Detection]
```

## Pattern Detection Decision Tree

```mermaid
graph TD
    REQ[Request Analysis] --> SPEED_CHECK{Requests/sec > Threshold?}
    SPEED_CHECK -->|Yes| SPEED_PATTERN[Pattern: Superhuman Speed<br/>Score: 0-40 points]
    SPEED_CHECK -->|No| ENUM_CHECK{Sequential Endpoints?}
    ENUM_CHECK -->|Yes| ENUM_PATTERN[Pattern: Systematic Enumeration<br/>Score: 0-35 points]
    ENUM_CHECK -->|No| ANOMALY_CHECK{Statistical Anomaly?}
    ANOMALY_CHECK -->|Yes| ANOMALY_PATTERN[Pattern: Behavioral Anomaly<br/>Score: 0-25 points]
    ANOMALY_CHECK -->|No| NORMAL_PATTERN[Pattern: Normal<br/>Score: 0 points]
    
    SPEED_PATTERN --> FINAL[Final Detection]
    ENUM_PATTERN --> FINAL
    ANOMALY_PATTERN --> FINAL
    NORMAL_PATTERN --> FINAL
```

## Threat Scoring Process

```mermaid
graph LR
    SUB1[Speed Score<br/>0-40] --> SUM[Sum Scores]
    SUB2[Enumeration Score<br/>0-35] --> SUM
    SUB3[Anomaly Score<br/>0-25] --> SUM
    SUM --> CAP[Cap at 100]
    CAP --> LEVEL{Score Range?}
    LEVEL -->|0-29| NORM[Threat Level: Normal]
    LEVEL -->|30-69| SUSP[Threat Level: Suspicious]
    LEVEL -->|70-100| MAL[Threat Level: Malicious]
```

## Superhuman Speed Detection

**Algorithm**:
1. Track requests per second over 10-second window
2. Calculate average rate
3. Compare to threshold (default: 10 req/s)
4. If exceeded, calculate score based on excess

**Scoring Formula**:
```
speed_score = min(40, (rps / threshold) * 30)
```

## Systematic Enumeration Detection

**Algorithm**:
1. Track endpoint access patterns
2. Identify sequential numeric patterns (e.g., /api/users/1, /api/users/2)
3. Count sequence length
4. If length >= threshold (default: 5), flag as enumeration

**Scoring Formula**:
```
enum_score = min(35, sequence_length * 5)
```

## Behavioral Anomaly Detection

**Algorithm**:
1. Track statistical features:
   - Endpoint depth
   - Parameter count
   - Request intervals
2. Use Isolation Forest for anomaly detection
3. Calculate z-score for anomalies
4. Flag if z-score > threshold (default: 2.0)

**Scoring Formula**:
```
anomaly_score = min(25, (z_score / threshold) * 20)
```

## Threat Level Determination

- **Normal**: Score 0-29
- **Suspicious**: Score 30-69
- **Malicious**: Score 70-100

## Pattern Type Priority

1. Superhuman Speed (highest priority)
2. Systematic Enumeration
3. Behavioral Anomaly
4. Normal (default)

---

**Last Updated**: 2025-01-XX
**Version**: 1.0

