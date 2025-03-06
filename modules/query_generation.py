import requests
import json
import os
import xml.etree.ElementTree as ET
import re
from pathlib import Path

try:
    from config import LLM_MODEL_QUERY, LLM_API_KEY_QUERY
except ImportError:
    print("Error: config.py not found. Please create a config.py file with LLM_MODEL_QUERY and LLM_API_KEY_QUERY variables.")

def load_query_config(config_file='query_config.xml'):
    """
    Load query-generation configurations from the XML file.
    Returns a dict with query model names as keys and their configuration
    (prompt_template and request_params) as values.
    """
    if not Path(config_file).exists():
        create_default_query_config(config_file)
    
    tree = ET.parse(config_file)
    root = tree.getroot()
    
    config = {"query_models": {}}
    query_models_elem = root.find('query_models')
    for model_elem in query_models_elem.findall('query_model'):
        model_name = model_elem.get('name')
        prompt_template_elem = model_elem.find('prompt_template')
        prompt_template = prompt_template_elem.text if prompt_template_elem is not None else ""
        
        request_params = {}
        req_params_elem = model_elem.find('request_params')
        if req_params_elem is not None:
            for param in req_params_elem:
                request_params[param.tag] = param.text
        
        config["query_models"][model_name] = {
            "prompt_template": prompt_template,
            "request_params": request_params
        }
    return config

def create_default_query_config(config_file):
    """
    Create a default XML configuration file for query generation.
    The prompt instructs the model to generate two search queries as a JSON array,
    which makes parsing easier.
    """
    root = ET.Element('query_generation_config')
    query_models = ET.SubElement(root, 'query_models')
    
    # Default query generation model configuration
    default_model = ET.SubElement(query_models, 'query_model', name='default')
    ET.SubElement(default_model, 'prompt_template').text = (
        "You are an expert content adapter specializing in business news. "
        "Your task is to generate two search queries based on the following article. "
        "Output the two search queries as a JSON array (e.g. [\"query1\", \"query2\"]). "
        "The queries should help verify the accuracy of the article and must not include any numerical values to avoid false positives. "
        "Original Article: {article_text}"
    )
    default_params = ET.SubElement(default_model, 'request_params')
    ET.SubElement(default_params, 'model').text = LLM_MODEL_QUERY
    ET.SubElement(default_params, 'temperature').text = '0.4'
    ET.SubElement(default_params, 'top_k').text = '32'
    ET.SubElement(default_params, 'top_p').text = '0.95'
    ET.SubElement(default_params, 'max_tokens').text = '256'
    
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(config_file, encoding='utf-8', xml_declaration=True)

def generate_search_queries(article_text, query_model_name='default', config_file='query_config.xml'):
    """
    Generates two search queries based on the article text.
    The queries are intended to help verify the article's accuracy (without including numerical values).
    The output is parsed into a list, isert queries into the brackets " ", for example: ["query1", "query2"], for easier parsing.
    """
    config = load_query_config(config_file)
    if query_model_name not in config['query_models']:
        available = ', '.join(config['query_models'].keys())
        return f"Unsupported query model: {query_model_name}. Available models: {available}"
    
    model_config = config['query_models'][query_model_name]
    prompt_template = model_config["prompt_template"]
    request_params = model_config["request_params"]
    
    # Format the prompt with the provided article text
    prompt = prompt_template.format(article_text=article_text)
    
    # Use the API key from config.py
    api_key = LLM_API_KEY_QUERY
    
    # Extract request parameters
    model = request_params.get('model', LLM_MODEL_QUERY)
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
        max_tokens = int(request_params.get('max_tokens', 256))
    except ValueError:
        max_tokens = 256
    
    # Build the API URL and payload
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
            queries_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
            res = re.findall(r"\"(.*?)\"", queries_text)
            if len(res) >= 1:
                return res
            else:
                return f"len(res) < 1"
        else:
            return f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error making API request: {str(e)}"


#not tested code
def add_query_model(name, prompt_template, request_params, config_file='query_config.xml'):
    """
    Add or update a query generation model configuration in the XML file.
    `request_params` should be a dictionary containing keys such as model, temperature, top_k, top_p, and max_tokens.
    """
    tree = ET.parse(config_file)
    root = tree.getroot()
    query_models_elem = root.find('query_models')
    
    existing = query_models_elem.find(f"query_model[@name='{name}']")
    if existing is None:
        new_model = ET.SubElement(query_models_elem, 'query_model', name=name)
    else:
        new_model = existing
    
    prompt_elem = new_model.find('prompt_template')
    if prompt_elem is None:
        prompt_elem = ET.SubElement(new_model, 'prompt_template')
    prompt_elem.text = prompt_template
    
    req_params_elem = new_model.find('request_params')
    if req_params_elem is not None:
        new_model.remove(req_params_elem)
    req_params_elem = ET.SubElement(new_model, 'request_params')
    for key, value in request_params.items():
        ET.SubElement(req_params_elem, key).text = str(value)
    
    ET.indent(tree, space="  ")
    tree.write(config_file, encoding='utf-8', xml_declaration=True)
    return f"Query model '{name}' added/updated successfully"
