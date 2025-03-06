import json

def parse_input(request_data):
    """
    Parses the incoming request data.
    Expected format (JSON):
      {
        "input_type": "url" | "text" | "json",
        "data": <string> (url, plain text, or JSON string),
        "reader_type": "IT" | "Business",
        "proficiency": "Enthusiast" | "Bachelor" | "Master"
      }
    Returns a dictionary with parsed values.
    """
    try:
        # If the content type is JSON, assume it's already a dict
        if isinstance(request_data, dict):
            parsed_data = request_data
        else:
            parsed_data = json.loads(request_data)
    except Exception as e:
        raise ValueError(f"Invalid input data format: {e}")
    
    # Basic validation
    required_keys = ["input_type", "data", "reader_type", "proficiency"]
    for key in required_keys:
        if key not in parsed_data:
            raise ValueError(f"Missing required key: {key}")
    
    return parsed_data
