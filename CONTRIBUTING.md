# Contributing to AI-Driven Cyberattack Defense Analysis

Thank you for your interest in contributing to this repository! This document provides guidelines for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Maintain professional discourse
- Respect intellectual property

## How to Contribute

### Reporting Issues

If you find errors, inconsistencies, or areas for improvement:

1. Check existing issues to avoid duplicates
2. Create a new issue with:
   - Clear description of the problem
   - Specific location (file, section, line)
   - Suggested fix (if applicable)
   - References to source materials

### Suggesting Enhancements

For new content or improvements:

1. Open an issue describing the enhancement
2. Explain the value and rationale
3. Provide references or sources
4. Wait for feedback before implementing

### Submitting Changes

1. **Fork the repository**
2. **Create a branch**: `git checkout -b feature/your-feature-name`
3. **Make changes**:
   - Follow existing formatting and style
   - Use APA citation style
   - Include proper references
   - Update documentation as needed
4. **Test your changes**: 
   - Run tests locally: `pytest tests/ -v --cov=ai_tools`
   - Ensure code passes linting: `flake8 ai_tools/ dashboard/ tests/`
   - Check formatting: `black --check ai_tools/ dashboard/ tests/`
   - Verify import sorting: `isort --check-only ai_tools/ dashboard/ tests/`
5. **Commit changes**: Use clear, descriptive commit messages
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Create a Pull Request**: Provide clear description of changes

### CI/CD Requirements

All pull requests must pass the CI pipeline before merging. The CI system checks:

- ✅ **Code Formatting**: Code must be formatted with Black
- ✅ **Import Sorting**: Imports must be sorted with isort
- ✅ **Linting**: Code must pass flake8 checks
- ✅ **Unit Tests**: All unit tests must pass
- ✅ **Integration Tests**: Integration tests must pass (Ollama-dependent tests skipped in CI)
- ✅ **Code Coverage**: Minimum 80% code coverage required
- ✅ **Security**: Code must pass Bandit security scanning

**Before submitting a PR:**
- Ensure all tests pass locally
- Run `make lint` to check code quality
- Run `make format` to auto-format code if needed
- Verify coverage meets the 80% threshold

**CI will automatically:**
- Run tests across Python 3.8, 3.10, and 3.11
- Check code quality and security
- Generate coverage reports
- Provide feedback on any failures

## Style Guidelines

### Markdown Formatting
- Use clear headings and structure
- Include visualizations (Mermaid) where they add value
- Maintain consistent formatting throughout
- Use tables for structured data

### Citations
- Follow APA style (7th edition)
- Include in-text citations for all claims
- Provide complete references
- Update CITATIONS.md for new sources

### Writing Style
- Use clear, professional language
- Balance technical accuracy with accessibility
- Provide context for technical terms
- Include practical examples where helpful

## Content Guidelines

### What to Include
- Factual information based on credible sources
- Practical recommendations and guidance
- Clear explanations of technical concepts
- Actionable defense strategies

### What to Avoid
- Speculation without evidence
- Unsubstantiated claims
- Vendor-specific recommendations without justification
- Sensitive operational details

## Review Process

1. All contributions will be reviewed
2. **CI must pass**: Pull requests will not be merged until CI checks pass
3. Reviewers may request changes
4. Contributors should respond to feedback promptly
5. Maintainers will merge approved changes after CI approval

## Development Setup

### Pre-commit Hooks

Install pre-commit hooks to catch issues before committing:

```bash
pip install pre-commit
pre-commit install
```

This will automatically check formatting, imports, and linting on each commit.

### Running Tests Locally

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run all tests with coverage
pytest tests/ -v --cov=ai_tools --cov-report=term-missing

# Run specific test categories
pytest tests/unit/ -v              # Unit tests only
pytest tests/integration/ -v        # Integration tests only
pytest tests/ -v -m "not requires_ollama"  # Skip Ollama-dependent tests
```

### Code Quality Checks

```bash
# Format code
black ai_tools/ dashboard/ tests/

# Sort imports
isort ai_tools/ dashboard/ tests/

# Check linting
flake8 ai_tools/ dashboard/ tests/ --max-line-length=100 --exclude=__pycache__

# Run security scan
bandit -r ai_tools/ dashboard/
```

## Questions?

If you have questions about contributing:
- Open an issue with the `question` label
- Check existing documentation
- Review similar contributions

Thank you for helping improve this resource!

