import requests
import json

# Define the API URL
url = "http://127.0.0.1:5000/process-news"

# Define the payload (same as your curl request)
payload = {
    "input_type": "text", 
    "data": """Trump repeats false claims over 2020 election loss, deflects responsibility for Jan. 6

By  ERIC TUCKER
Updated 3:21 PM EET, September 11, 2024
Share
WASHINGTON (AP) — Former President Donald Trump persisted in saying during the presidential debate that he won the 2020 election and took no responsibility for any of the mayhem that unfolded at the Capitol on Jan. 6, 2021, when his supporters stormed the building to block the peaceful transfer of power.

The comments Tuesday night underscored the Republican’s refusal, even four years later, to accept the reality of his defeat and his unwillingness to admit the extent to which his falsehoods about his election loss emboldened the mob that rushed the Capitol, resulting in violent clashes with law enforcement. Trump’s grievances about that election are central to his 2024 campaign against Democrat Kamala Harris, as he professes allegiance to the rioters.

In 2020, Democrat Joe Biden won 306 electoral votes to Trump’s 232, and there was no widespread fraud, as election officials across the country, including Trump’s then-attorney general, William Barr, have confirmed. Republican governors in Arizona and Georgia, crucial to Biden’s victory, vouched for the integrity of the elections in their states. Nearly all the legal challenges from Trump and his allies were dismissed by judges, including two tossed by the Supreme Court, which includes three Trump-nominated justices.

An Associated Press review of every potential case of voter fraud in the six battleground states disputed by Trump found fewer than 475. Biden took Arizona, Georgia, Michigan, Nevada, Pennsylvania and Wisconsin and their 79 electoral votes by a combined 311,257 votes out of 25.5 million ballots cast for president. The disputed ballots represent just 0.15% of his victory margin in those states.

More election coverage
Arizona Democratic Gov. Katie Hobbs gives the State of the State address in the House of Representatives at the Capitol Monday, Jan. 13, 2025, in Phoenix. (AP Photo/Ross D. Franklin)
Arizona’s Democratic governor faces uphill battle as Republicans control Legislature
President Joe Biden waits to speak about foreign policy at the State Department in Washington, Monday, Jan. 13, 2025. (AP Photo/Susan Walsh)
Biden says he’s leaving Trump with a ‘strong hand to play’ in world conflicts
West Virginia Governor Patrick Morrisey and his wife, Denise, greet people following his swearing-in at the state capitol in Charleston, W.Va., on Monday, Jan. 13, 2025. (AP Photo/Chris Jackson)
West Virginia’s conservative shift could sharpen under its new governor
In the ABC debate, Trump was asked twice if he regretted anything he did on Jan. 6, when he told his supporters to march to the Capitol and exhorted them to “fight like hell.” On the Philadelphia stage, Trump first responded by complaining that the questioner had failed to note that he had encouraged the crowd to behave “peacefully and patriotically.” Trump also noted that one of his backers, Ashli Babbitt, was fatally shot inside the building by a Capitol Police officer.


Trump suggested that protesters who committed crimes during the 2020 racial injustice protests were not prosecuted. But an AP review in 2021 of documents in more than 300 federal cases stemming from the protests sparked by George Floyd’s death found that more than 120 defendants across U.S. pleaded guilty or were convicted at trial of federal crimes including rioting, arson and conspiracy.

When the question about his actions on Jan. 6 arose again, Trump replied: “I had nothing to do with that other than they asked me to make a speech. I showed up for a speech.”

But he ignored other incendiary language he used throughout the speech, during which he urged the crowd to march to the Capitol, where Congress was meeting to certify Biden’s victory. Trump told the crowd: “If you don’t fight like hell, you’re not going to have a country anymore.” That’s after his lawyer, Rudy Giuliani, declared: “Let’s have trial by combat.”

Trump didn’t appeal for the rioters to leave the Capitol until more than three hours after the assault began. He then released a video telling the rioters it was time to “go home,” but added: “We love you. You’re very special people.”

He also repeated an oft-stated false claim that then-House Speaker Nancy Pelosi, D-Calif., “rejected” his offer to send “10,000 National Guard or soldiers” to the Capitol. Pelosi does not direct the National Guard. As the Capitol came under attack, she and then-Senate Majority leader Mitch McConnell, R-Ky. called for military assistance, including from the National Guard.

Harris pledged to “turn the page” from Jan. 6, when she was in the Capitol as democracy came under attack.

“So for everyone watching, who remembers what January 6th was, I say, ‘We don’t have to go back. Let’s not go back. We’re not going back. It’s time to turn the page.”

Though Trump had seemed to acknowledge in a recent podcast interview that he had indeed “lost by a whisker,” he insisted Tuesday night that that was a sarcastic remark and resumed his boasts about the election.

“I’ll show you Georgia, and I’ll show you Wisconsin, and I’ll show you Pennsylvania,” he said in rattling off states where he claimed, falsely, that he had won. “We have so many facts and statistics.”



""",
    "reader_type": "IT",
    "proficiency": "Bachelor, smartest guy in the room, knows just about everything, AI girl with 1000B parameters is his future wife"

}

# Set headers
headers = {
    "Content-Type": "application/json"
}

# Send POST request
response = requests.post(url, data=json.dumps(payload), headers=headers)

# Print the response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
