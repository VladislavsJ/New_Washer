from flask import Flask, request, jsonify, render_template
import json

# Import our modules
from modules import comparison, input_parser, content_filter, query_generation, web_scraper, output_generator
import config

app = Flask(__name__)
app.config["DEBUG"] = config.DEBUG

@app.route("/")
def index():
    """Serve the main frontend page"""
    return render_template("index.html")

@app.route("/process-news", methods=["POST"])
def process_news():
    """
    Endpoint to process a news article.
    
    Expects a JSON payload with keys:
      - input_type: "url" | "text" 
      - data: The input data (URL, text)
      - reader_type: "IT" or "Business"
      - proficiency: "Any string explaining the reader's proficiency"
    
    Returns a JSON with the refined content and verification report.
    """
    try:
        # Parse input data
        input_data = input_parser.parse_input(request.get_json())
        reader_type = input_data["reader_type"]
        proficiency = input_data["proficiency"]
        
        # Get the original article text
        if input_data["input_type"] == "url":
            try:
                article_text = web_scraper.scrape_web_page_sync(input_data["data"])
                if not article_text:
                    return jsonify({"error": "Failed to scrape URL - no content retrieved"}), 400
                print(f"Scraped text length: {len(article_text)}")  # Debug logging
            except Exception as e:
                return jsonify({"error": f"Failed to scrape URL: {str(e)}"}), 400
        elif input_data["input_type"] == "text":
            article_text = input_data["data"]
        else:
            return jsonify({"error": "Invalid input type provided."}), 400
        
        # 1. Content Filtering based on reader type and proficiency
        filtered_text = content_filter.filter_content(article_text, reader_type, proficiency)
        # query generation using llm 
        queries = query_generation.generate_search_queries(article_text)
        # For each query, performs a search and scrape the top result.
        links = web_scraper.google_searches(queries)  # Get links for each query
        # check if links are valid
        valid_links = web_scraper.validate_links(links)
        # get the scraped data
        if valid_links:
            scraped_data = web_scraper.scrape_web_pages(valid_links, queries)  # Get scraped content for each link
        else:
            error_message = "No valid links found, most probable case, API limit reached"
            return jsonify({"error": error_message}), 400
        
        connected_data = list(zip(queries, links, scraped_data))
        

        # 4.  Comparison between original article and scraped data.
        verification_report = comparison.get_verification_report(article_text, connected_data)
        #add links to the verification report


        # 5. Generate final output
        try:
            output = output_generator.generate_final_output(filtered_text, verification_report, links)
        except Exception as e:
            output = {
                "error": f"Error generating final output: {str(e)}",
                "filtered_text": filtered_text,
                "verification_report": verification_report,
                "links": links
            }
        
        return jsonify(output)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=config.DEBUG)
