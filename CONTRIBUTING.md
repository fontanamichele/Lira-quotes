# Contributing to Lira quotes

Thank you for your interest in contributing to Lira quotes! This document provides guidelines and information for contributors.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request, please:

1. Check if the issue already exists in the [Issues](https://github.com/fontanamichele/lira-quotes/issues) section
2. Create a new issue with a clear title and description
3. Include steps to reproduce the problem (for bugs)
4. Specify your environment (Python version, OS, etc.)

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Clone the repository:

```bash
git clone https://github.com/fontanamichele/lira-quotes.git
cd lira-quotes
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the API:

```bash
python main.py
```

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Add type hints where appropriate

## Testing

Before submitting a pull request, please:

1. Test your changes locally
2. Ensure the API starts without errors
3. Test the endpoints you've modified
4. Check that currency conversion works correctly

## API Testing

You can test the API endpoints using curl or any HTTP client:

```bash
# Test current prices
curl "http://localhost:8000/prices/current?tickers=AAPL&currency=USD"

# Test historical prices
curl "http://localhost:8000/prices/historical?tickers=AAPL&period=1mo"

# Test currency conversion
curl "http://localhost:8000/prices/current?tickers=VWCE.AS&currency=USD"
```

## Documentation

- Update the README.md if you add new features
- Add docstrings to new functions
- Update API documentation in the code comments

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have any questions about contributing, please open an issue or contact the maintainers.

Thank you for contributing! 🚀
