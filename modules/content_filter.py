import requests
import json
import xml.etree.ElementTree as ET
from pathlib import Path
try:
    from config import LLM_MODEL, LLM_API_KEY
except ImportError: 
    print("Error: config.py not found. Please create a config.py file with LLM_MODEL and LLM_API_KEY variables.")
def load_prompt_config(config_file='prompt_config.xml'):
    """
    Load prompt templates and request parameters for each reader type from the XML file.
    Returns a dict with reader types as keys and their configuration (prompt_template and request_params) as values.
    """
    if not Path(config_file).exists():
        create_default_config(config_file)
    
    tree = ET.parse(config_file)
    root = tree.getroot()

    config = {"reader_types": {}}
    reader_types_elem = root.find('reader_types')
    for reader_type_elem in reader_types_elem.findall('reader_type'):
        type_name = reader_type_elem.get('name')
        prompt_template_elem = reader_type_elem.find('prompt_template')
        prompt_template = prompt_template_elem.text if prompt_template_elem is not None else ""
        
        # Load request parameters specific to this reader type
        request_params = {}
        req_params_elem = reader_type_elem.find('request_params')
        if req_params_elem is not None:
            for param in req_params_elem:
                request_params[param.tag] = param.text
        
        config["reader_types"][type_name] = {
            "prompt_template": prompt_template,
            "request_params": request_params
        }
    
    return config

def filter_content(article_text, reader_type, proficiency, config_file='prompt_config.xml'):
    """
    Tailor the article text based on the reader type and proficiency level using the LLM API.
    Loads the prompt template and request parameters for the given reader type from the XML file.
    """
    config = load_prompt_config(config_file)
    if reader_type not in config['reader_types']:
        available = ', '.join(config['reader_types'].keys())
        return f"Unsupported reader type: {reader_type}. Available types: {available}"
    
    reader_config = config['reader_types'][reader_type]
    prompt_template = reader_config["prompt_template"]
    request_params = reader_config["request_params"]

    # Format the prompt with the provided article and proficiency
    prompt = prompt_template.format(proficiency=proficiency, article_text=article_text)

    # Retrieve API key from the environment (or use a fallback)
    api_key = LLM_API_KEY
    
    # Extract and convert request parameters
    model = request_params.get('model')
    try:
        temperature = float(request_params.get('temperature', 0.4))
    except ValueError:
        temperature = 0.4
    try:
        top_k = int(request_params.get('top_k', 32))
    except ValueError:
        top_k = 32
    try:
        top_p = float(request_params.get('top_p', 0.95))
    except ValueError:
        top_p = 0.95
    try:
        max_tokens = int(request_params.get('max_tokens', 8192))
    except ValueError:
        max_tokens = 8192

    # Build the API URL and payload based on the parameters from the XML
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": temperature,
            "topK": top_k,
            "topP": top_p,
            "maxOutputTokens": max_tokens
        }
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            response_data = response.json()
            # Extract the generated text from the response structure
            refined_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
            return refined_text
        else:
            return f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error making API request: {str(e)}"

#def add_reader_type(name, prompt_template, request_params, config_file='prompt_config.xml'):
#XML file give options to add new reader types, but not implemented yet.

def create_default_config(config_file):
    """
    Create a default XML configuration file with initial reader types for Business and IT.
    Each reader type includes its prompt template and request parameters.
    The prompt instructs the model to refine the given news article without adding any new information,
    and to produce an output that is at least three times shorter than the original text.
    """
    root = ET.Element('content_filter_config')
    reader_types = ET.SubElement(root, 'reader_types')
    
    # Business reader configuration
    business = ET.SubElement(reader_types, 'reader_type', name='Business')
    ET.SubElement(business, 'prompt_template').text = (
        "You are an expert content adapter specializing in business news. "
        "Your task is to refine the following business article without adding any new information. "
        "Ensure the refined version is at least three times shorter than the original text while preserving key business details. "
        "Background: {proficiency}\n\n"
        "Original Article: {article_text}\n\n"
        "Please output the refined article."
    )
    business_params = ET.SubElement(business, 'request_params')
    ET.SubElement(business_params, 'model').text = LLM_MODEL
    ET.SubElement(business_params, 'temperature').text = '0.4'
    ET.SubElement(business_params, 'top_k').text = '32'
    ET.SubElement(business_params, 'top_p').text = '0.95'
    ET.SubElement(business_params, 'max_tokens').text = '8192'
    
    # IT reader configuration
    it = ET.SubElement(reader_types, 'reader_type', name='IT')
    ET.SubElement(it, 'prompt_template').text = (
        "You are an expert content adapter specializing in technical news. "
        "Your task is to refine the following technical article without adding any new details. "
        "Make sure the refined version is at least three times shorter than the original text while retaining essential technical content. "
        "Background: {proficiency}\n\n"
        "Original Article: {article_text}\n\n"
        "Please output the refined article."
    )
    it_params = ET.SubElement(it, 'request_params')
    ET.SubElement(it_params, 'model').text = LLM_MODEL
    ET.SubElement(it_params, 'temperature').text = '0.4'
    ET.SubElement(it_params, 'top_k').text = '32'
    ET.SubElement(it_params, 'top_p').text = '0.95'
    ET.SubElement(it_params, 'max_tokens').text = '8192'
    
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(config_file, encoding='utf-8', xml_declaration=True)