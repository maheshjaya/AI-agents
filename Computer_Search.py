import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
import requests
from bs4 import BeautifulSoup
import random

os.environ["OPENAI_API_KEY"] = 
os.environ["SERPER_API_KEY"] = 

search_tool = SerperDevTool()

# Function to scrape services from computer.com
def scrape_services(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        services = [service.text.strip() for service in soup.find_all('li')]
        return services
    except Exception as e:
        print(f"Error scraping services: {e}")
        return []

# Define your agents with roles and goals
web_navigator = Agent(
    role='Web Navigator',
    goal='Navigate through computer.com and list its services',
    backstory="""You are tasked with navigating through computer.com to gather information about its services.""",
    verbose=True,
    allow_delegation=False
)

internet_searcher = Agent(
    role='Internet Searcher',
    goal='Search the internet for potential customers matching the services of computer.com',
    backstory="""You are responsible for searching the internet to find potential customers whose needs match the services provided by computer.com.""",
    verbose=True,
    allow_delegation=True,
    tools=[search_tool]
)

# Create tasks for your agents
task1 = Task(
    description="""Navigate through computer.com and list its services""",
    expected_output="List of services provided by computer.com",
    agent=web_navigator
)

task2 = Task(
    description="""Search the internet for potential customers matching the services of computer.com""",
    expected_output="List of potential customers",
    agent=internet_searcher
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[web_navigator, internet_searcher],
    tasks=[task1, task2],
    verbose=2
)

# Get your crew to work!
result = crew.kickoff()

# Check if result is a dictionary
if isinstance(result, dict) and 'task_results' in result:
    # Check if the first task was successful
    if result['task_results'][0]['success']:
        # Extract the services from the result
        computer_services = result['task_results'][0]['output']
        # Print the services
        print("Services provided by computer.com:")
        for service in computer_services:
            print("-", service)
    else:
        print("Failed to scrape services from computer.com")
else:
    print("Invalid result format:", result)

# Simulate potential customers based on the services (you can replace this with actual logic to find customers)
def find_potential_customers(services, num_customers):
    potential_customers = []
    interests = ["Gaming", "Programming", "Graphic Design", "Business", "Education"]
    for _ in range(num_customers):
        interest = random.choice(interests)
        # Generate random contact details
        contact_details = {
            "name": "Customer Name",
            "email": f"customer{_ + 1}@example.com",
            "phone": f"+1 (123) 456-789{_ + 1}",
            "interest": interest
        }
        potential_customers.append(contact_details)
    return potential_customers

# If the first task was successful, simulate potential customers
if isinstance(result, dict) and 'task_results' in result and result['task_results'][0]['success']:
    computer_services = result['task_results'][0]['output']
    # Simulate potential customers based on the services
    potential_customers = find_potential_customers(computer_services, 10000)
    # Print the first few potential customers
    print("\nPotential customers:")
    for customer in potential_customers[:5]:
        print("Name:", customer["name"])
        print("Email:", customer["email"])
        print("Phone:", customer["phone"])
        print("Interest:", customer["interest"])
        print()
        
print("######################")
print(result)