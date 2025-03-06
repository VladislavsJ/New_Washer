#!/usr/bin/env python3


import requests
import json
import config

def generate_llm_prompt(article: str, connected_data: list) -> str:
    """
    Generates an LLM prompt by inserting the newspaper article and external sources.
    
    Parameters:
        article (str): The full text of the newspaper article.
        connected_data (list): A list of tuples in the format (query, link, scraped_data).
    
    Returns:
        str: The prompt to be sent to the LLM.
    """
    prompt_lines = [
        "You are provided with a newspaper article and several external sources on the same topic.",
        "Your task is to verify the key numerical claims in the article by comparing them against the information in the external sources.",
        "For crucial claims in the article, determine if the extrnal source contradict then mention it,",
        "if the external source confirms the claim, then write summary, does source are abble to verify the claim or not.",
        "make it short and concise, maximum 200 words.",
        "Newspaper Article:",
        article,
        "",
        "External Sources:"
    ]
    
    for idx, (query, link, scraped_data) in enumerate(connected_data, start=1):
        source_info = [
            f"Source {idx}:",
            f"Query: {query}",
            f"Link: {link}",
            "Content (Markdown):",
            scraped_data,
            ""
        ]
        prompt_lines.extend(source_info)
    
    prompt_lines.append("Please analyze the above information and provide your assessment for each numerical claim in the article.")
    
    return "\n".join(prompt_lines)

def call_llm(prompt: str) -> str:
    """
    Calls the LLM with the given prompt and returns the generated output.
    
    Parameters:
        prompt (str): The prompt to send to the LLM.
    
    Returns:
        str: The response from the LLM.
    """
    model = config.LLM_MODEL_COMPARISON
    api_key = config.LLM_API_KEY_COMPARISON
    temperature = 0.25
    top_k = 25
    top_p = 0.95
    max_tokens = 1000
    
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
            result_text = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return result_text
        else:
            return f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error making API request: {str(e)}"
def get_verification_report(article: str, connected_data: list) -> str:
    """
    Generates a verification report by comparing the article with the external sources.
    """
    prompt = generate_llm_prompt(article, connected_data)
    result = call_llm(prompt)
    return result
