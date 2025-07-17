# this_file: CONTRIBUTING.md

# Contributing to html22text

Thank you for your interest in contributing to html22text! This document provides guidelines for contributing to the project.

## Quick Start

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment:
   ```bash
   ./scripts/dev-setup.sh
   ```
4. Make your changes
5. Run tests and checks:
   ```bash
   ./scripts/test.sh
   ```
6. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git

### Environment Setup

```bash
git clone https://github.com/your-username/html22text.git
cd html22text
./scripts/dev-setup.sh
```

This will:
- Install all dependencies
- Set up pre-commit hooks
- Make scripts executable

### Manual Setup

If you prefer manual setup:

```bash
pip install -e ".[dev]"
pre-commit install
```

## Development Workflow

### 1. Code Quality

We use several tools to ensure code quality:

- **Ruff**: Linting and formatting
- **MyPy**: Type checking
- **Pytest**: Testing

Run all checks:
```bash
./scripts/test.sh
```

Individual commands:
```bash
# Linting
python -m ruff check src/ tests/
python -m ruff format src/ tests/

# Type checking
python -m mypy --package html22text --package tests

# Testing
python -m pytest --cov=src/html22text --cov-report=term-missing tests/
```

### 2. Testing

- Write tests for new features
- Ensure existing tests pass
- Maintain or improve test coverage
- Tests are in the `tests/` directory

### 3. Building

Build the package locally:
```bash
./scripts/build.sh
```

This will create distribution files in the `dist/` directory.

## Release Process

### For Maintainers

1. Ensure all tests pass
2. Update `CHANGELOG.md`
3. Create a new version tag:
   ```bash
   ./scripts/release.sh v1.2.3
   ```

This will:
- Run all tests
- Build the package
- Create and push a git tag
- Trigger automated CI/CD for PyPI publishing

### Automated Release

When a version tag is pushed:
1. CI runs tests on all platforms
2. Package is built
3. PyPI release is published
4. GitHub release is created
5. Executables are built and attached

## Code Style Guidelines

### Python Code

- Follow PEP 8 (enforced by Ruff)
- Use type hints
- Write docstrings for public functions
- Keep functions focused and small

### Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions
- Update CHANGELOG.md for releases

### Git Commits

- Write clear, descriptive commit messages
- Keep commits focused on a single change
- Consider using [Conventional Commits](https://www.conventionalcommits.org/)

## Pull Request Guidelines

1. **Branch naming**: Use descriptive names like `feature/add-new-parser` or `fix/handle-empty-input`

2. **Pull request description**: Include:
   - What changes you made
   - Why you made them
   - Any breaking changes
   - Tests you added

3. **Checklist before submitting**:
   - [ ] Tests pass locally
   - [ ] Code is formatted (Ruff)
   - [ ] Type checking passes (MyPy)
   - [ ] New tests added if needed
   - [ ] Documentation updated if needed

## Reporting Issues

When reporting bugs:
1. Use GitHub Issues
2. Include Python version and platform
3. Provide a minimal reproduction example
4. Include expected vs actual behavior

## Feature Requests

For new features:
1. Check existing issues first
2. Describe the use case
3. Provide examples of desired behavior
4. Consider implementation complexity

## Getting Help

- GitHub Issues for bugs and feature requests
- GitHub Discussions for questions and ideas
- Check existing documentation and tests

## Code of Conduct

Be respectful and inclusive. We want this to be a welcoming project for everyone.

## License

By contributing, you agree that your contributions will be licensed under the same MIT License as the project.