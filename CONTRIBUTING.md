# Contributing to GhostLens-Pro

Thank you for your interest in contributing to GhostLens-Pro! This document provides guidelines for contributing to this project.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- No external dependencies required (standard library only)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ghostlens-pro.git
   cd ghostlens-pro
   ```

2. Run the CLI to verify installation:
   ```bash
   python -m ghostlens_pro.cli --help
   ```

3. Run tests:
   ```bash
   python -m pytest tests/test_core.py -v
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- All functions and classes must have complete docstrings
- Use type annotations for all function signatures
- Keep functions focused and concise
- Add comments for complex logic

### Project Structure

```
ghostlens-pro/
  ghostlens_pro/
    __init__.py              # Package initialization
    __main__.py              # Package entry point
    cli.py                   # CLI interface
    fingerprint_collector.py # Fingerprint collection engine
    detection_scorer.py      # Anti-detection scoring engine
    profile_generator.py     # Fingerprint profile generator
    consistency_checker.py   # Consistency checker
    fingerprint_comparator.py# Fingerprint comparator
    tui_dashboard.py         # TUI dashboard
  tests/
    test_core.py             # Core unit tests
  setup.py                   # Installation configuration
  requirements.txt           # Dependencies (zero external)
  LICENSE                    # MIT License
  .gitignore                 # Git ignore rules
  CONTRIBUTING.md            # This file
```

### Adding New Features

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Write code with proper docstrings and type annotations

3. Add tests for new functionality

4. Ensure all existing tests pass:
   ```bash
   python -m pytest tests/test_core.py -v
   ```

5. Verify CLI functionality:
   ```bash
   python -m ghostlens_pro.cli --help
   ```

### Commit Messages

Use conventional commit format:

- `feat: add new fingerprint dimension`
- `fix: correct scoring algorithm`
- `docs: update contribution guide`
- `test: add tests for consistency checker`
- `refactor: improve code structure`

### Pull Request Process

1. Ensure your code passes all tests
2. Update documentation if needed
3. Describe your changes clearly in the PR description
4. Wait for code review before merging

## Reporting Issues

When reporting issues, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs

## License

By contributing to GhostLens-Pro, you agree that your contributions will be licensed under the MIT License.
