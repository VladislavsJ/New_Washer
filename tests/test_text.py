import requests
import json

def test_text_input():
    url = "http://127.0.0.1:5000/process-news"
    payload = {
        "input_type": "text",
        "data": (
            """Elon Musk’s artificial intelligence startup, xAI, showed off the updated Grok-3 model, showcasing a version of the chatbot technology that the billionaire has said is the "smartest AI on Earth.”
Across math, science and coding benchmarks, Grok-3 beats Alphabet’s Google Gemini, DeepSeek’s V3 model, Anthropic’s Claude and OpenAI’s GPT-4o, the company said via a live stream on Monday. Grok-3 has "more than 10 times” the computing power of its predecessor and completed pretraining in early January, Musk said in a presentation alongside three of xAI’s engineers.

"We’re continually improving the models every day, and literally within 24 hours, you’ll see improvements,” Musk said.

The company introduced a new smart search engine with Grok-3, calling it DeepSearch. DeepSearch is a reasoning chatbot that expresses its process of understanding a query and how it plans its response. It includes options for research, brainstorming and data analysis, the demonstration showed.

Grok-3 is rolling out to Premium+ subscribers on social media platform X immediately. The company is starting a new subscription called SuperGrok for the Grok mobile app and Grok.com website.

The new chatbot appears to put Grok ahead of OpenAI’s latest ChatGPT and ramps up an increasingly bitter rivalry between the two companies. Musk launched xAI in 2023 as an alternative to OpenAI, which he’s publicly criticized for its plans to restructure as a for-profit business.

The billionaire filed two lawsuits against OpenAI for allegedly straying from its founding principles and offered to buy OpenAI’s nonprofit arm for $97.4 billion in a bid that was rejected last week. OpenAI Chief Executive Officer Sam Altman classified the bid as a tactic to "slow us down.” Musk was involved in OpenAI’s founding but has been critical of the company since leaving the board in 2018.

AI powerhouses such as OpenAI and xAI have raised funds at a rapid clip with valuations soaring. Musk’s xAI is reportedly in talks to raise about $10 billion in a funding round that would value the company at roughly $75 billion. The company was last valued at about $51 billion, according to data compiled by PitchBook.

OpenAI is in talks to raise as much as $40 billion in a round that would push its valuation to up to $300 billion.

These businesses are also capital-intensive. SoftBank Group, OpenAI, Oracle and Abu Dhabi-backed MGX jointly announced a program in January to deploy $100 billion, with the goal of eventually spending $500 billion, for the construction of data centers and other infrastructure for AI in the U.S..

Dell Technologies is at an advanced stage of securing a deal worth more than $5 billion to provide xAI with servers optimized for AI.

But rival technologies are emerging that could challenge this model and make it easier for new competitors to emerge. Last month, Chinese AI company DeepSeek released a new open-source AI model, called R1, that matched or beat leading U.S. competitors on a range of industry benchmarks. The company said it built the model for a fraction of the cost of its U.S. counterparts."""
        ),
        "reader_type": "IT",
        "proficiency": "Bachelor, smartest guy in the room, knows just about everything, AI girl with 1000B parameters is his future wife"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    print("=== Test Text Input ===")
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

if __name__ == "__main__":
    test_text_input()
