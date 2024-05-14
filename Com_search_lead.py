import os
from crewai import Agent, Task, Crew
import requests
from bs4 import BeautifulSoup
import re

os.environ["OPENAI_API_KEY"] = 

# URL of the website to scrape
url = "https://computer.com"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract text from the entire webpage
    webpage_text = soup.get_text()
    
    # Define service keywords
    service_keywords = ["service", "services"]
    
    # Extract phrases containing the keywords
    service_phrases = []
    for keyword in service_keywords:
        # Find all sentences containing the keyword
        matches = re.findall(r'[^.]*?{}[^.]*\.'.format(keyword), webpage_text, re.IGNORECASE)
        service_phrases.extend(matches)
    
    # Initialize output variable
    output = ""
    
    # Concatenate extracted phrases into the output variable
    if service_phrases:
        print("Extracted the phrases containing service keywords")
        for phrase in service_phrases:
            output += phrase.strip() + "\n"  # Concatenate phrases with a newline character
        #print(output)  # Print all extracted phrases
        
        # Define the Crew AI agent and task
        content_reader = Agent(
            role='content reader',
            goal="Identify computer-related services",
            backstory="Identify computer-related services",
            verbose=True,
            allow_delegation=False
        )

        # Split the output into chunks to stay within token limit
        output_chunks = [output[i:i + 8192] for i in range(0, len(output), 8192)]

        # Initialize output variable
        final_result=""
        # Iterate over each chunk and process it separately
        for chunk in output_chunks:
            content_reader.goal = f"Identify computer-related services from {chunk}"
            content_reader.backstory = f"Identify computer-related services from {chunk}"
            
            task1 = Task(
                description=f"Identify computer-related services from {chunk} and prepare them as a list without number them",
                expected_output="List of services",
                agent=content_reader,
            )

            crew = Crew(
                agents=[content_reader],
                tasks=[task1],
                verbose=2
            )

            result = crew.kickoff()
            final_result+=result  
            
            #print(result)
         
    else:
        print("No phrases containing service keywords found on the website.")
    
else:
    print("Failed to retrieve the webpage.")
    

    
#print(final_result)


# Define the Crew AI agent and task
inspector = Agent(
    role='inspector',
    goal="Remove similar computer-related services",
    backstory="Remove similar computer-related services",
    verbose=True,
    allow_delegation=False
)

task2 = Task(
    description=f"Remove similar computer-related services from {final_result} and prepare a refined list",
    expected_output="Refined list. Do not mention the removed items",
    agent=inspector,
)
            
crew = Crew(
    agents=[inspector],
    tasks=[task2],
    verbose=2
)

final_output = crew.kickoff()

#print(final_output)