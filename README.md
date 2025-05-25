# Wikipedia Word-Frequency Dictionary

A Python server application that takes an article and a depth parameter as input, and generates a word-frequency dictionary by traversing Wikipedia articles up to the specified depth.

## Features

- Traverse Wikipedia articles starting from a given article
- Follow links to other Wikipedia articles up to a specified depth
- Generate word-frequency dictionaries from the traversed articles
- Filter results by ignoring specific words
- Filter results by percentile threshold

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Oli200110/wikipedia-word-frequency.git
   cd wikipedia-word-frequency
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -e .
   ```

## Running the Application

To start the server, run:

```bash
python run.py
```

This will start the server at http://localhost:8000 and automatically open the API documentation in your browser.

### Command-line Options

The run script supports several command-line options:

```bash
python run.py --help
```

Available options:
- `--host`: Host to bind the server to (default: 0.0.0.0)
- `--port`: Port to bind the server to (default: 8000)
- `--no-browser`: Don't open the browser automatically
- `--no-reload`: Disable auto-reload on code changes

### Utility Scripts

The project includes several utility scripts:

- `check_dependencies.py`: Check if all required dependencies are installed
- `run_tests.py`: Run all unit tests
- `example.py`: Example script demonstrating how to use the API

To check if all dependencies are installed:

```bash
python check_dependencies.py
```

To run all tests:

```bash
python run_tests.py
```

## API Endpoints

### GET /word-frequency

Generate a word-frequency dictionary for a Wikipedia article and its linked articles.

**Parameters:**
- `article` (string): The title of the Wikipedia article to start from.
- `depth` (int): The depth of traversal within Wikipedia articles.

**Example:**
```
GET /word-frequency?article=Python&depth=1
```

**Response:**
```json
{
  "word_count": {
    "python": 120,
    "programming": 45,
    "language": 30,
    ...
  },
  "word_frequency": {
    "python": 10.5,
    "programming": 3.9,
    "language": 2.6,
    ...
  }
}
```

### POST /keywords

Generate a filtered word-frequency dictionary for a Wikipedia article and its linked articles.

**Request Body:**
```json
{
  "article": "Python",
  "depth": 1,
  "ignore_list": ["the", "and", "is", "in", "of", "to"],
  "percentile": 50
}
```

**Parameters:**
- `article` (string): The title of the Wikipedia article.
- `depth` (int): The depth of traversal.
- `ignore_list` (array[string]): A list of words to ignore.
- `percentile` (int): The percentile threshold for word frequency.

**Response:**
Same format as the GET /word-frequency endpoint, but with words in the ignore list excluded and filtered by the specified percentile.

## Running Tests

To run the tests, use:

```bash
pytest
```

## Project Structure

- `wiki_word_freq/`: Main package directory
  - `__init__.py`: Package initialization
  - `main.py`: FastAPI application and API endpoints
  - `models.py`: Pydantic models for request/response data
  - `wikipedia.py`: Wikipedia client for fetching and traversing articles
  - `word_frequency.py`: Word frequency analysis
  - `tests/`: Test directory
    - `test_api.py`: Tests for API endpoints
    - `test_wikipedia.py`: Tests for Wikipedia client
    - `test_word_frequency.py`: Tests for word frequency analyzer
- `run.py`: Script to run the application
- `run_tests.py`: Script to run all unit tests
- `check_dependencies.py`: Script to check if all required dependencies are installed
- `example.py`: Example script demonstrating how to use the API
- `README.md`: Project documentation
- `pyproject.toml`: Project configuration and dependencies

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
