import streamlit as st
from openai import AzureOpenAI
import os
import dotenv

dotenv.load_dotenv()  
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")  
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")  
  
# Set up the Azure OpenAI client  
client = AzureOpenAI(api_key=AOAI_KEY, azure_endpoint=AOAI_ENDPOINT, api_version="2024-05-01-preview")  

def get_gpt_response(prompt, model="gpt-35-turbo"):  
    response = client.chat.completions.create(  
        model="gpt-35-turbo",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant. For the resources include a section with resources to websites for the students in bullet points"},
            {"role": "user", "content": prompt}],
        max_tokens=150  
    )  
    return response.choices[0].message.content  

# Function to determine learning style based on questionnaire
def determine_learning_style(answers):
    learning_styles = {
        "Visual": 0,
        "Auditory": 0,
        "Reading/Writing": 0,
        "Kinesthetic": 0
    }
    
    # Example questions and corresponding learning style points
    questions = [
        ("When you are learning something new, you prefer to:", {"Visual": 1, "Auditory": 2, "Reading/Writing": 3, "Kinesthetic": 4}),
        ("You remember best when you:", {"Visual": 1, "Auditory": 2, "Reading/Writing": 3, "Kinesthetic": 4}),
        ("When you see the word 'cat', you:", {"Visual": 1, "Auditory": 2, "Reading/Writing": 3, "Kinesthetic": 4}),
        ("When solving a problem, you prefer to:", {"Visual": 1, "Auditory": 2, "Reading/Writing": 3, "Kinesthetic": 4})
    ]
    
    for i, answer in enumerate(answers):
        for style, points in questions[i][1].items():
            if answer == points:
                learning_styles[style] += 1

    return max(learning_styles, key=learning_styles.get)

# Function to store user data in session state
def store_user_data(name, learning_style):
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    st.session_state.user_data[name] = learning_style

# Streamlit form for user input
st.title("P.E.L.O - Personalized E-Learning Opportunities")

with st.form(key='survey_form'):
    name = st.text_input("Enter your name:")
    
    # Learning style questions
    answers = []
    answers.append(st.radio("When you are learning something new, you prefer to:",
        ["See diagrams and charts", "Listen to explanations", "Read and take notes", "Use hands-on activities"]))
    answers.append(st.radio("You remember best when you:",
        ["Visualize it", "Hear it", "Read it", "Do it"]))
    answers.append(st.radio("When you see the word 'cat', you:",
        ["Visualize a picture of a cat", "Hear the sound of a cat", "See the word 'cat' written", "Imagine a cat physically"]))
    answers.append(st.radio("When solving a problem, you prefer to:",
        ["Draw diagrams", "Discuss with others", "Write down steps", "Use physical objects"]))

    submitted = st.form_submit_button("Submit")

if submitted:
    # Determine learning style
    learning_style = determine_learning_style(answers)
    store_user_data(name, learning_style)
    st.write(f"Hello {name}, your learning style is {learning_style}.")

# Input field for math questions
if 'user_data' in st.session_state:
    st.header("Ask a Math Question")
    question = st.text_input("Enter your math question:")

    if st.button("Get Resource"):
        if question:
            # Retrieve the user's learning style
            user_learning_style = st.session_state.user_data.get(name, "Visual")
            # Create a prompt for GPT-4 based on the user's learning style and question
            prompt = f"Provide a {user_learning_style} learning style resource for the following math question: {question}"
            gpt_response = get_gpt_response(prompt)
            st.write(gpt_response)
        else:
            st.write("Please enter a math question.")