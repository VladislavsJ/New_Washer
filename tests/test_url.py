import requests
import json

def test_url_input():
    url = "http://127.0.0.1:5000/process-news"
    payload = {
        "input_type": "url",
        "data": "https://www.deepseek.com/",
        "reader_type": "Business",
        "proficiency": "Master degree in Business, I know all math that is related to money, know how to use AI to make money, money, money, Always sunny in the rich man's world"
        # ABBA Will damage promt for sure, but it's just for testing, and I am not promt engineer at all =/
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    print("=== Test URL Input ===")
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

if __name__ == "__main__":
    test_url_input()
