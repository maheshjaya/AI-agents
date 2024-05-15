import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
import requests
from bs4 import BeautifulSoup
import re

# Set environment variables
os.environ["OPENAI_API_KEY"] = 
os.environ["SERPER_API_KEY"] = 

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
        final_result = ""
        
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
            final_result += result  

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

# Initialize SerperDevTool
search_tool = SerperDevTool()

# Define services and criteria list
services = final_output
criteria_list = [
    'First name', 'Last name', 'Linkedin URL', 'Email', 'Work email', 'Phone number',
    'Job title', 'Departments', 'Country', 'State', 'City', 'Company Name',
    'Company domain', 'Company description', 'Company year founded', 'Company website',
    'Company number of employees', 'Company revenue', 'Total funding amount',
    'Total number of rounds', 'Last round/event amount', 'Last round/event type',
    'Last round/event date', 'Company Linkedin URL', 'Company city', 'Company state',
    'Company country', 'Company street', 'Company old industry', 'Company main industry',
    'Company sub industry', 'Company specialities', 'Company contact email'
]

# Define agents
web_navigator = Agent(
    role='Web Navigator',
    goal=f"Navigate through the internet to identify potential customers for any of the services in {services}",
    backstory=f"You are tasked with navigating through the internet to gather information about potential customers for any of the services in {services}",
    verbose=True,
    allow_delegation=False
)

information_extractor = Agent(
    role='Information Extractor',
    goal=f"Extract information from potential customers according to the criteria given in {criteria_list}",
    backstory=f"You are responsible for extracting information from potential customers according to the criteria given in {criteria_list}",
    verbose=True,
    allow_delegation=True,
)

# Define tasks
task1 = Task(
    description=f"Navigate through the internet to identify potential customers for any of the services in {services}",
    expected_output="List of potential customers",
    agent=web_navigator
)

task2 = Task(
    description=f"Extract information from potential customers according to the criteria given in {criteria_list}",
    expected_output=f"Information of each potential customer according to the criteria given in {criteria_list}",
    agent=information_extractor
)

# Instantiate crew
crew = Crew(agents=[web_navigator, information_extractor], tasks=[task1, task2], verbose=2)

# Get crew to work
result = crew.kickoff()

# Print result
print("######################")
print(result)
