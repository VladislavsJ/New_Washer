from flask import Flask, request, jsonify
import json

# Import our modules
from modules import comparison, input_parser, content_filter, query_generation, web_scraper, output_generator
import config

app = Flask(__name__)
app.config["DEBUG"] = config.DEBUG

@app.route("/process-news", methods=["POST"])
def process_news():
    """
    Endpoint to process a news article.
    
    Expects a JSON payload with keys:
      - input_type: "url" | "text" | "json"
      - data: The input data (URL, text, or JSON string)
      - reader_type: "IT" or "Business"
      - proficiency: "Enthusiast", "Bachelor", or "Master"
      -- non mandatory
      - interest: "Technology", "Business", or "Physical Impelementation"
    
    Returns a JSON with the refined content and verification report.
    """
    try:
        # Parse input data
        input_data = input_parser.parse_input(request.get_json())
        reader_type = input_data["reader_type"]
        proficiency = input_data["proficiency"]
        
        # Get the original article text
        if input_data["input_type"] == "url":
            # For URL, use web scraper to get article text.
            article_text = web_scraper.scrape_web_page_sync(input_data["data"])
        elif input_data["input_type"] == "text":
            article_text = input_data["data"]
        elif input_data["input_type"] == "json":
            # Assuming the JSON contains a field "article" with the text.
            try:
                json_data = json.loads(input_data["data"])
                article_text = json_data.get("article", "")
            except Exception as e:
                return jsonify({"error": f"Error parsing JSON data: {e}"}), 400
        else:
            return jsonify({"error": "Invalid input type provided."}), 400
        #test pupose, not neede for now. 
        
        # 1. Content Filtering based on reader type and proficiency
        filtered_text = content_filter.filter_content(article_text, reader_type, proficiency)
        #filtered_text="TEST"
        # 2. Generate search queries (RAG part)
        queries = query_generation.generate_search_queries(article_text)
        # Create arrays of queries and get corresponding links and data
        #queries = ["OpenAI GPT-4.5 capabilities and limitations", "Microsoft Azure AI supercomputers training AI models"]
        links = web_scraper.google_searches(queries)  # Get links for each query
        scraped_data = web_scraper.scrape_web_pages(links, queries)  # Get scraped content for each link
        
        # Create list of tuples connecting related data
        connected_data = list(zip(queries, links, scraped_data))
        # Now connected_data[0] contains (queries[0], links[0], scraped_data[0]) etc.
        
        # 3. For each query, perform a search and scrape the top result.
        # NOTE: In this stub, we are assuming that the query directly gives a URL.
        # In production, you should integrate with a search API (e.g., Google Custom Search)
        # and then scrape the top two links.
        # Here, we'll simply assume that queries[0] and queries[1] are URLs (for demo purposes).
        # Replace the following with your actual search integration:

        # 4. Numerical Comparison between original article and scraped data.
        verification_report = comparison.get_verification_report(article_text, connected_data)
        #add links to the verification report
        verification_report["links"] = links

        # 5. Generate final output
        output = output_generator.generate_final_output(filtered_text, verification_report)
        
        return jsonify(output)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=config.DEBUG)
