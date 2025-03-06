# Project Overview

This project provides an API service that processes news articles in two key ways:

1. **Content Adaptation**: Tailors news content based on the reader's professional background (IT or Business) and expertise level (Enthusiast, Bachelor, Master)
2. **Fact Verification**: Cross-checks the article's claims against external sources to evaluate accuracy

The system accepts news content in multiple formats (URL, text, or JSON), processes it through a modular pipeline, and returns both refined content and a verification report.

## File Structure & Explanations

### `app.py`
The main Flask application that handles API requests and orchestrates the processing pipeline. It receives POST requests to `/process-news`, validates inputs, and sequences the execution of various modules.

### `modules/input_parser.py`
Validates incoming request data, ensuring it contains all required fields (`input_type`, `data`, `reader_type`, `proficiency`) and is properly formatted.

### `modules/content_filter.py`
Tailors article content based on reader preferences. Uses XML-configured prompt templates to generate audience-specific versions of the content via language model APIs.

### `modules/query_generation.py`
Creates search queries from the article text for verification purposes.

### `modules/web_scraper.py`
Handles all web interactions, including scraping the original article (if provided as URL) and retrieving external verification sources. Integrates with crawl4ai for content extraction and Google Custom Search API for search operations.

### `modules/comparison.py`
Compares article claims with information from external sources.provides an assessment of the article's accuracy.

### `modules/output_generator.py`
Assembles the final API response by combining the filtered content, verification report, and reference links into a structured JSON format.

### `prompt_config.xml`
Configuration file for content filtering, containing prompt templates and API parameters for different reader types.

### `query_config.xml`
Configuration file for query generation, specifying prompt templates and parameters for creating effective search queries.

### `config.py` (not shown in snippets)
Contains configuration variables such as API keys and model identifiers.

## Key Technologies

- **Flask**: 
- **Language Model APIs**:
- **crawl4ai**: Web scraping tool
- **Google Custom Search API**: 

The modular architecture allows each component to be developed, tested, and maintained independently. or IT SHOULD allow it. 