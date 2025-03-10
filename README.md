# Fetch PubMed API

## Overview

This project allows users to fetch research papers from PubMed based on a user-specified query. The fetched data includes details like title, authors, publication date, DOI, and more. The results can be displayed in the terminal or saved to a CSV file.

## Code Organization

The project is structured as follows:

```
fetch-pubmedAPI-main/
│── task/
│   ├── __init__.py
│   ├── cli.py               # Command-line interface for fetching papers
│   ├── fetch_data.py        # Contains functions to retrieve and process papers
│── poetry.lock              # Dependency lock file
│── pyproject.toml           # Poetry configuration file
│── README.md                # Documentation
```

### Files & Functions:

- **`cli.py`**: Provides the CLI interface to fetch papers using command-line arguments.
- **`fetch_data.py`**: Handles API requests to PubMed and processes the response.
- **`pyproject.toml`**: Contains dependency and project configurations for Poetry.

## Installation & Setup

### Prerequisites

Ensure you have the following installed:

- Python 3.11+
- Poetry (for dependency management)

### Install Dependencies

Use Poetry to install dependencies:

```bash
poetry install
```

## Usage

### Fetching Papers from PubMed

Run the following command to fetch research papers based on a search query:

```bash
poetry run get-papers-list "your_query_here"
```

### Additional Options:

- **Enable Debugging**:
  ```bash
  poetry run get-papers-list "your_query_here" -d
  ```
- **Save Results to CSV**:
  ```bash
  poetry run get-papers-list "your_query_here" -f results.csv
  ```

## API Configuration

The project fetches papers from the PubMed API using the `eutils` endpoints. Ensure that you have a valid API and email key set in `constants.py`:

```python
# constants.py
API_KEY = "your_api_key_here"
EMAIL = "your_email_here"
```

## Dependencies

The project uses the following dependencies:

- `requests`: For making API requests
- `pandas`: For data processing
- `numpy`: For handling numerical operations

These dependencies are managed using Poetry and specified in `pyproject.toml`.

---

