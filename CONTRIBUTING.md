# Contributing to html22text

Thanks for considering a contribution to html22text. Here's how to get started.

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

- Python 3.10+
- Git

### Environment Setup

```bash
git clone https://github.com/your-username/html22text.git
cd html22text
./scripts/dev-setup.sh
```

This script will:
- Install dependencies
- Set up pre-commit hooks
- Make scripts executable

### Manual Setup

If you're not into automation:

```bash
pip install -e ".[dev]"
pre-commit install
```

## Development Workflow

### 1. Code Quality

We use these tools to keep things clean:

- **Ruff**: Linting and formatting
- **MyPy**: Type checking
- **Pytest**: Testing

Run everything at once:
```bash
./scripts/test.sh
```

Or individually:
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
- Keep existing tests passing
- Don’t reduce test coverage
- All tests live in `tests/`

### 3. Building

Build the package locally:
```bash
./scripts/build.sh
```

Distribution files appear in `dist/`.

## Release Process

### For Maintainers

1. Make sure all tests pass  
2. Update `CHANGELOG.md`  
3. Create a version tag:
   ```bash
   ./scripts/release.sh v1.2.3
   ```

This does:
- Run tests
- Build the package
- Tag and push to GitHub
- Trigger CI/CD for PyPI

### Automated Release

Pushing a version tag triggers:
1. Cross-platform tests via CI
2. Package build
3. PyPI release
4. GitHub release creation
5. Executable builds attached to release

## Code Style Guidelines

### Python Code

- Follow PEP 8 (Ruff will enforce it)
- Use type hints
- Add docstrings for public functions
- Keep functions small and focused

### Documentation

- Update README.md if users will notice the change
- Add docstrings to new functions
- Keep CHANGELOG.md updated for releases

### Git Commits

- Write clear, concise commit messages
- One logical change per commit
- Optional but appreciated: [Conventional Commits](https://www.conventionalcommits.org/)

## Pull Request Guidelines

1. **Branch names** should describe the work: `feature/add-new-parser`, `fix/handle-empty-input`, etc.

2. **PR description** must include:
   - What changed
   - Why it changed
   - Breaking changes (if any)
   - New tests (if applicable)

3. **Before submitting**, confirm:
   - [ ] Tests pass locally
   - [ ] Code is formatted with Ruff
   - [ ] MyPy passes
   - [ ] New tests added where needed
   - [ ] Documentation updated if necessary

## Reporting Issues

To report a bug effectively:

1. Open a GitHub Issue  
2. Mention your Python version and OS  
3. Provide a minimal example that reproduces the issue  
4. State expected vs actual behavior  

## Feature Requests

Propose new features by:

1. Checking existing issues first  
2. Describing the use case clearly  
3. Showing examples of desired behavior  
4. Considering how complex it might be to implement  

## Getting Help

- Use GitHub Issues for bugs and features  
- Use GitHub Discussions for general questions  
- Read the documentation and tests before asking  

## Code of Conduct

Be respectful. Be constructive. Don’t be a jerk.

## License

By contributing, you agree your code will be licensed under the MIT License, same as the project.