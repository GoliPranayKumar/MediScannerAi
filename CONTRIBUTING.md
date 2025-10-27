# Contributing to MediScanner AI

Thank you for your interest in contributing to MediScanner AI! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions with other contributors.

## How to Contribute

### 1. Report Bugs

**Before creating a bug report, check if it already exists.**

When reporting bugs, include:
- Clear description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, etc.)

### 2. Suggest Enhancements

Enhancements are tracked as GitHub issues. When suggesting an enhancement:
- Use a clear, descriptive title
- Provide a detailed description
- Explain the use case
- List any related issues

### 3. Submit Pull Requests

#### Before You Start
1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature: `git checkout -b feature/YourFeature`
4. Make your changes
5. Test thoroughly
6. Commit with clear messages: `git commit -m 'Add YourFeature'`
7. Push to your fork: `git push origin feature/YourFeature`
8. Open a Pull Request

#### PR Guidelines
- Provide a clear description of changes
- Reference related issues
- Include screenshots for UI changes
- Ensure all tests pass
- Follow the existing code style
- Update documentation if needed

### 4. Development Setup

```bash
# Clone the repository
git clone https://github.com/GoliPranayKumar/MediScannerAi.git
cd MediScannerAi

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
npm run build
cd ..

# Run locally
python app.py
```

### 5. Code Style

- Follow PEP 8 for Python
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small
- Write docstrings for functions

### 6. Testing

```bash
# Run tests
python -m pytest test.py

# Check coverage
python -m pytest --cov=. test.py
```

### 7. Documentation

- Update README.md for user-facing changes
- Update docstrings for code changes
- Add comments for complex logic
- Update ARCHITECTURE.md for structural changes

## Areas for Contribution

### Backend
- Improve ML model accuracy
- Add new model architectures
- Optimize inference speed
- Enhance error handling
- Add more API endpoints

### Frontend
- Improve UI/UX
- Add new features
- Optimize performance
- Fix bugs
- Improve accessibility

### Documentation
- Improve README
- Add tutorials
- Create guides
- Fix typos
- Add examples

### Testing
- Write unit tests
- Add integration tests
- Improve test coverage
- Add edge case tests

## Commit Message Guidelines

Use clear, descriptive commit messages:
```
[Type] Brief description

Detailed explanation if needed.

Fixes #issue_number
```

Types:
- `[FEAT]` - New feature
- `[FIX]` - Bug fix
- `[DOCS]` - Documentation
- `[STYLE]` - Code style
- `[REFACTOR]` - Code refactoring
- `[PERF]` - Performance improvement
- `[TEST]` - Tests

## Review Process

1. Maintainer reviews your PR
2. Feedback provided if needed
3. Make requested changes
4. PR approved and merged

## Questions?

- Open an issue for questions
- Check existing documentation
- Review previous issues/PRs

## Recognition

Contributors will be recognized in:
- README.md
- GitHub contributors page
- Release notes

Thank you for contributing! 🎉
