# CLI Testing Tool

Easy command-line interface for testing the AI Pattern Detector without using the dashboard.

## Quick Start

```bash
# Test with attack traffic (recommended for testing detections)
python3 tools/cli_test.py attack --count 20

# Test with normal traffic
python3 tools/cli_test.py normal --count 10

# Test with mixed traffic (30% attack)
python3 tools/cli_test.py mixed --count 30 --ratio 0.3

# Test a single custom request
python3 tools/cli_test.py single --endpoint "/api/user/123"

# Run continuous test for 60 seconds
python3 tools/cli_test.py continuous --duration 60 --intensity 0.5
```

## Commands

### `normal` - Test Normal Traffic
Tests the detector with normal, human-like traffic patterns.

```bash
python3 tools/cli_test.py normal --count 10
```

**Options:**
- `--count`: Number of requests to generate (default: 10)

### `attack` - Test Attack Traffic
Tests the detector with GTG-1002 style attack traffic (high-speed systematic enumeration).

```bash
python3 tools/cli_test.py attack --count 20
```

**Options:**
- `--count`: Number of requests to generate (default: 20)

**Note:** You need at least 10-15 requests to see detections, as the detector needs to build up request history to detect patterns.

### `mixed` - Test Mixed Traffic
Tests with a mix of normal and attack traffic.

```bash
python3 tools/cli_test.py mixed --count 30 --ratio 0.3
```

**Options:**
- `--count`: Number of requests to generate (default: 30)
- `--ratio`: Attack ratio from 0.0 to 1.0 (default: 0.3)

### `single` - Test Single Request
Test a single custom request.

```bash
python3 tools/cli_test.py single --endpoint "/api/user/123" --ip "198.51.100.42"
```

**Options:**
- `--endpoint`: Endpoint to test (required)
- `--ip`: IP address (default: 198.51.100.42)

### `continuous` - Continuous Test
Run a continuous test for a specified duration.

```bash
python3 tools/cli_test.py continuous --duration 60 --intensity 0.5
```

**Options:**
- `--duration`: Duration in seconds (default: 60)
- `--intensity`: Attack intensity from 0.0 to 1.0 (default: 0.5)

Press `Ctrl+C` to stop early.

## Expected Output

The tool shows:
- Real-time detection results with color-coded threat levels:
  - 🟢 Normal
  - 🟡 Suspicious  
  - 🔴 Malicious
- Detection details (score, pattern type, endpoint, IP)
- Summary statistics at the end

## Examples

### Quick Attack Test
```bash
python3 tools/cli_test.py attack --count 15
```

### Test Custom Endpoint
```bash
python3 tools/cli_test.py single --endpoint "/api/admin/users/1?id=1"
```

### Long Running Test
```bash
python3 tools/cli_test.py continuous --duration 120 --intensity 0.7
```

## Troubleshooting

**No threats detected?**
- Make sure you're generating enough requests (at least 10-15 for attack patterns)
- Check that attack intensity is > 0 for attack/mixed tests
- The detector needs to build up request history to detect patterns

**Detection thresholds too sensitive/not sensitive enough?**
- Adjust thresholds in `ai_tools/config.py`:
  - `SUPERHUMAN_SPEED_THRESHOLD`: Default 10 req/s
  - `ENUMERATION_SEQUENCE_LENGTH`: Default 5 sequential requests
  - `ANOMALY_Z_SCORE_THRESHOLD`: Default 2.0

