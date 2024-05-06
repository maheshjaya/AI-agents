Can you prepare lecture notes for a Quantum computing introductory course including
mathematical expressions definition ? Search for course materials related to the
quantum computing introductory course. Gather relevant textbooks, PDF files from
university websites, online resources, and lecture materials. Particularly give a more
emphasis during the search to seek lecture materials freely available on the internet.
From the search results, identify a set of subtopics that should be included in the lecture
materials. These subtopics must be relevant to the quantum computing introductory
course. Prepare an outline for the lecture notes, including the identified subtopics. Give
further elaboration for each subtopic in the outline of the lecture note given . For each
subtopic, a detailed explanation is required, incorporating additional mathematical
equations and definitions where applicable. Each subtopic should be expanded to fill at
least one A4 sheet in length. When presenting mathematical expressions, provide the
meaning of each symbol immediately after its inclusion. If the available research
materials are insufficient for any subtopic, conduct a targeted search to gather more
information for expanding the subtopic.



import os
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew, Process

# Set API keys (if necessary)
os.environ["OPENAI_API_KEY"] = 
os.environ["SERPER_API_KEY"] = 


def display_menu(options):
    print("Select an option:")
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")

def get_user_choice(options):
    while True:
        display_menu(options)
        choice = input("Enter your choice (1-{0}): ".format(len(options)))
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        else:
            print("Invalid choice. Please enter a number between 1 and {0}.".format(len(options)))

# Define the list of options
options = ["Introductory", "Intermediate", "Advanced"]

# Get the user's choice
chosen_option = get_user_choice(options)

# Define agents
search_agent = Agent(
    role='Search Agent',
    goal='Search for subject-specific materials, definitions, and equations on a given topic',
    backstory='You are skilled at finding relevant subject materials, definitions, and equations quickly.',
    verbose=True
)

classifier_agent= Agent(
    role='Text classifier',
    goal='Classify the content in the search results according to their similarity.',
    backstory="""You are experienced in classifying similar content in the subject materials of the search results.""",
    verbose=True
)

note_agent = Agent(
    role='Note Preparation Agent',
    goal='Create lecture notes with subject-specific materials, definitions, and equations based on the search results',
    backstory="""You are experienced in organizing subject materials and creating structured lecture notes 
    with definitions and equations.""",
    verbose=True
)


# Prompt user for topic
topic = input('Enter the topic for lecture notes: ')
#specifications = int(input('Enter the number of sub-topics to include: '))

# Define tasks
search_task = Task(
    description=f""" 
    Search for course materials related to the {topic} and {chosen_option}. 
    Gather relevant textbooks, PDF files from university websites, online resources, and lecture materials. 
    Particularly give a more emphasize during the search to seek lecture materials freely available on the internet.
    """,
    expected_output='Search results (e.g., articles, papers, websites, pdf files)',
    agent=search_agent
)

classifier_task = Task(
    description=f"""  
    From the search results, identify a set of subtopics that should be included in the lecture materials. 
    These subtopics must be relevant to the {topic} and the {chosen_option}. 
    Prepare an outline for the lecture notes, including the identified subtopics.
    """,
    expected_output='Outline of the lecture notes including the suitable subtopics',
    agent=classifier_agent
)

note_task = Task(
    description=f"""
    Give further elaboration for each subtopic in the outline of the lecture note given by the classifier_agent.  . 
    For each subtopic, a detailed explanation is required, incorporating additional mathematical equations and definitions where applicable. 
    Each subtopic should be expanded to fill at least one A4 sheet in length. 
    When presenting mathematical expressions, provide the meaning of each symbol immediately after its inclusion. 
    If the available research materials are insufficient for any subtopic, prompt the search_agent to conduct 
    a targeted search to gather more information for expanding the subtopic.
    """,
    expected_output='Structured lecture notes with subject-specific materials, definitions, and equations',
    agent=note_agent
)


# Establishing the crew with a hierarchical process and additional configurations
project_crew = Crew(
    tasks=[search_task, classifier_task, note_task],
    agents=[search_agent, classifier_agent, note_agent],
    manager_llm=ChatOpenAI(temperature=0, model="gpt-4"),  # Mandatory for hierarchical process
    process=Process.hierarchical,  # Specifies the hierarchical management approach
    memory=True,  # Enable memory usage for enhanced task execution
)

# Start the crew's task execution
lecture_notes = project_crew.kickoff()

# Display the result
print('\n\nLecture notes preparation completed successfully.')
print('Here are the lecture notes:')
print(lecture_notes)

