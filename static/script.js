document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const inputTextarea = document.getElementById('input-data');
    const inputTypeOptions = document.querySelectorAll('.input-type-option');
    const readerTypeRadios = document.getElementsByName('reader-type');
    const proficiencyInput = document.getElementById('proficiency');
    const jsonPreview = document.getElementById('json-preview');
    const sendButton = document.getElementById('send-button');
    const resultContainer = document.getElementById('result-container');
    const newspaperSection = document.getElementById('newspaper-section');
    const verificationSection = document.getElementById('verification-section');
    const linksSection = document.getElementById('links-section');
    
    // Example data
    const examples = {
        text: {
            it: {
                data: `Elon Musk's artificial intelligence startup, xAI, showed off the updated Grok-3 model, showcasing a version of the chatbot technology that the billionaire has said is the "smartest AI on Earth."
Across math, science and coding benchmarks, Grok-3 beats Alphabet's Google Gemini, DeepSeek's V3 model, Anthropic's Claude and OpenAI's GPT-4o, the company said via a live stream on Monday. Grok-3 has "more than 10 times" the computing power of its predecessor and completed pretraining in early January, Musk said in a presentation alongside three of xAI's engineers.

"We're continually improving the models every day, and literally within 24 hours, you'll see improvements," Musk said.`,
                proficiency: "Bachelor, smartest guy in the room, knows just about everything, AI girl with 1000B parameters is his future wife"
            },
            business: {
                data: `Trump repeats false claims over 2020 election loss, deflects responsibility for Jan. 6

By ERIC TUCKER
Updated 3:21 PM EET, September 11, 2024

WASHINGTON (AP) — Former President Donald Trump persisted in saying during the presidential debate that he won the 2020 election and took no responsibility for any of the mayhem that unfolded at the Capitol on Jan. 6, 2021, when his supporters stormed the building to block the peaceful transfer of power.

The comments Tuesday night underscored the Republican's refusal, even four years later, to accept the reality of his defeat and his unwillingness to admit the extent to which his falsehoods about his election loss emboldened the mob that rushed the Capitol, resulting in violent clashes with law enforcement. Trump's grievances about that election are central to his 2024 campaign against Democrat Kamala Harris, as he professes allegiance to the rioters.`,
                proficiency: "Master degree in Business, I know all math that is related to money, know how to use AI to make money, money, money, Always sunny in the rich man's world"
            }
        },
        url: {
            it: {
                data: "https://www.deepseek.com/",
                proficiency: "Bachelor, smartest guy in the room, knows just about everything, AI girl with 1000B parameters is his future wife"
            },
            business: {
                data: "https://www.bloomberg.com/news/articles/2025-03-06/trump-likely-to-defer-tariffs-on-goods-services-under-usmca",
                proficiency: "Master degree in Business, I know all math that is related to money, know how to use AI to make money, money, money, Always sunny in the rich man's world"
            }
        }
    };
    
    // Default input example
    inputTextarea.value = examples.text.it.data;
    proficiencyInput.value = examples.text.it.proficiency;
    
    // Set active input type
    let currentInputType = "text";
    let currentReaderType = "it"; // Track the current reader type
    
    // Input type selector
    inputTypeOptions.forEach(option => {
        option.addEventListener('click', function() {
            const type = this.getAttribute('data-type');
            
            // Only update if the type actually changed
            if (currentInputType !== type) {
                currentInputType = type;
                
                // Update active class
                inputTypeOptions.forEach(opt => opt.classList.remove('active'));
                this.classList.add('active');
                
                // Update placeholder based on input type
                if (type === 'text') {
                    inputTextarea.placeholder = "Paste your article text here...";
                } else {
                    inputTextarea.placeholder = "Enter a URL to a news article...";
                }
                
                // Update the input data to match the current reader type and new input type
                inputTextarea.value = examples[currentInputType][currentReaderType].data;
                
                // Update JSON preview
                updateJsonPreview();
            }
        });
    });
    
    // Example buttons
    document.getElementById('example-it').addEventListener('click', function() {
        currentReaderType = "it";
        const data = examples[currentInputType].it;
        inputTextarea.value = data.data;
        proficiencyInput.value = data.proficiency;
        document.getElementById('it').checked = true;
        updateJsonPreview();
    });
    
    document.getElementById('example-business').addEventListener('click', function() {
        currentReaderType = "business";
        const data = examples[currentInputType].business;
        inputTextarea.value = data.data;
        proficiencyInput.value = data.proficiency;
        document.getElementById('business').checked = true;
        updateJsonPreview();
    });
    
    // Update JSON preview whenever inputs change
    function updateJsonPreview() {
        const selectedReaderType = Array.from(readerTypeRadios)
            .find(radio => radio.checked).value;
        currentReaderType = selectedReaderType;
        
        const jsonData = {
            input_type: currentInputType,
            data: inputTextarea.value,
            reader_type: selectedReaderType,
            proficiency: proficiencyInput.value
        };
        
        jsonPreview.textContent = JSON.stringify(jsonData, null, 2);
    }
    
    // Add event listeners to update preview when inputs change
    inputTextarea.addEventListener('input', updateJsonPreview);
    proficiencyInput.addEventListener('input', updateJsonPreview);
    readerTypeRadios.forEach(radio => {
        radio.addEventListener('change', updateJsonPreview);
    });
    
    // Initialize the preview
    updateJsonPreview();
    
    // Handle form submission
    sendButton.addEventListener('click', function() {
        // Show loading state
        resultContainer.innerHTML = `
            <div class="loading-container">
                <div class="loading-bar">
                    <div class="loading-bar-progress"></div>
                </div>
                <div class="loading-text">Processing your request...</div>
            </div>
        `;
        
        // Get form data
        const selectedReaderType = Array.from(readerTypeRadios)
            .find(radio => radio.checked).value;
        
        const requestData = {
            input_type: currentInputType,
            data: inputTextarea.value,
            reader_type: selectedReaderType,
            proficiency: proficiencyInput.value
        };
        
        // Send API request
        fetch('/process-news', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log("Received data:", data); // Debug log
            // Display results
            displayResults(data);
        })
        .catch(error => {
            console.error("Error:", error); // Debug log
            resultContainer.innerHTML = `
                <div class="error-message">
                    <h3>Error</h3>
                    <p>${error.message}</p>
                </div>
            `;
        });
    });
    
    // Function to display results
    function displayResults(data) {
        // Create container for results
        resultContainer.innerHTML = `
            <div id="newspaper-section" class="result-section"></div>
            <div id="verification-section" class="result-section"></div>
            <div id="links-section" class="result-section"></div>
        `;
        
        // Get the newly created elements
        const newNewspaperSection = document.getElementById('newspaper-section');
        const newVerificationSection = document.getElementById('verification-section');
        const newLinksSection = document.getElementById('links-section');
        
        // Check for error
        if (data.error) {
            resultContainer.innerHTML = `
                <div class="error-message">
                    <h3>Error</h3>
                    <p>${data.error}</p>
                </div>
            `;
            return;
        }
        
        // Display newspaper description
        if (data.filtered_text) {
            newNewspaperSection.innerHTML = `
                <h3>Filtered Article</h3>
                <div class="newspaper">${data.filtered_text.replace(/\n/g, '<br>')}</div>
            `;
        }
        
        // Display verification report
        if (data.verification_report) {
            newVerificationSection.innerHTML = `
                <h3>Verification Report</h3>
                <div class="verification-report">${data.verification_report.replace(/\n/g, '<br>')}</div>
            `;
        }
        
        // Display links
        if (data.links && data.links.length > 0) {
            let linksHtml = '<h3>Reference Links</h3><ul class="links-list">';
            
            data.links.forEach(link => {
                if (link) {
                    linksHtml += `<li><a href="${link}" target="_blank">${link}</a></li>`;
                }
            });
            
            linksHtml += '</ul>';
            newLinksSection.innerHTML = linksHtml;
        }
    }
}); 