# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not** open a public issue. Instead, please report it privately by:

1. **Email**: Contact the repository maintainers directly
2. **GitHub Security Advisory**: Use GitHub's private vulnerability reporting feature (if enabled)

### What to Include

When reporting a security vulnerability, please include:

- **Description**: Clear description of the vulnerability
- **Impact**: Potential impact and severity
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Suggested Fix**: If you have a suggested fix, please include it
- **Affected Versions**: Which versions are affected

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution**: Depends on severity and complexity

## Security Best Practices

When using this repository:

1. **Keep Dependencies Updated**: Regularly update dependencies to receive security patches
2. **Review Configuration**: Ensure environment variables and configuration files are properly secured
3. **Use Environment Variables**: Never commit API keys, passwords, or sensitive tokens
4. **Follow Principle of Least Privilege**: Run services with minimal required permissions
5. **Monitor Logs**: Regularly review logs for suspicious activity
6. **Network Security**: Use HTTPS/TLS for all network communications
7. **Regular Backups**: Maintain regular backups of detection data and configurations

## Known Security Considerations

### AI Model Integration

- **Ollama**: Runs locally by default. If exposing Ollama over a network, ensure proper authentication and network security
- **Model Security**: Use trusted models from verified sources

### Database Security

- **SQLite**: Default database is SQLite (file-based). For production, consider using a more robust database with proper access controls
- **ChromaDB**: Vector database runs locally. Ensure proper file permissions

### Network Exposure

- **Dashboard**: Streamlit dashboard runs on `localhost:8501` by default. Do not expose to public networks without proper authentication
- **API Endpoints**: If exposing API endpoints, implement proper authentication and rate limiting

## Security Updates

Security updates will be:

- Released as patch versions (e.g., 1.0.1, 1.0.2)
- Documented in CHANGELOG.md
- Tagged with security labels in GitHub

## Acknowledgments

We appreciate responsible disclosure of security vulnerabilities. Contributors who report security issues will be acknowledged (with permission) in our security advisories.

