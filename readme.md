# Project Overview
This API processes news articles by tailoring content to match the reader's professional background and expertise level, and verifying numerical claims against external sources for accuracy. It accepts various input formats, uses AI to adapt content for different audience types, and delivers both refined articles and verification reports in a single structured response.

![Example](https://github.com/user-attachments/assets/d66b0e29-9d25-4605-ae34-00cf880f6a06)

1. **Content Adaptation**: Tailors news content based on the reader's professional background (IT or Business) and expertise level
2. **Query Generation/web scrapping** using LLM generates the query, that is used to get links from google search, and to scrap the web
3. **Fact Verification, RAG**: some sort of RAG, Cross-checks the article's claims against external sources to evaluate accuracy, and if llm training data is old
is may correct it using newest data from the web

 processes json and returns both refined content and a verification report + refernce links.

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


Adaptive News Verification & Refinement API
Overview
This API processes news articles by first tailoring the content based on reader type (IT or Business) and proficiency level (Enthusiast, Bachelor, Master), and then verifying key numerical claims via external sources. It leverages a configurable LLM (initially Llama-3.1-8B-Instruct) for text processing and query generation, and integrates a web-scraping tool (crawl4ai) to retrieve external evidence for cross-checking.


Key Functionalities
Input & Content Ingestion


Multi-format Input: Accept inputs as a URL link, plain text, or a JSON file containing the news article.
Parsing & Preprocessing: Standardize and parse the input, extract key sections, and prepare for analysis.
Audience-Based Content Filtering


Tailored Refinement: Use the LLM to modify the news text according to:
Reader Type: IT or Business focus.
Proficiency Level: Enthusiast, Bachelor, or Master.
Content Simplification/Enhancement: Adjust technical depth, language style, and context based on the target reader profile.
RAG (Retrieval Augmented Generation) for Data Verification


Query Generation:
Utilize the LLM to create search queries based on the topic—but intentionally omit explicit numerical details to retrieve unbiased sources.
Generate two distinct queries to fetch the top relevant search results.
Search Requests:
Integrate with a Google search API (or alternative search service) to retrieve links corresponding to the generated queries.
Web Data Retrieval:
Leverage crawl4ai to scrape and save the content from the top two search results as Markdown.
Numerical Data Comparison & Analysis


Extraction of Numerical Data: Identify key numerical values (e.g., pricing, statistics) from the original news article.
