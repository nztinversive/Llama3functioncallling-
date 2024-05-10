import streamlit as st
import requests
import json

st.title('AI Assistant Interaction')

# This function will interact with your Flask API
def ai_assistant_query(query):
    """Send a query to the AI Assistant Flask API and return the response."""
    url = f'https://nztinversive.github.io/Llama3functioncallling-/ask?query={query}'
    response = requests.get(url)
    if response.status_code == 200:
        return json.dumps(response.json(), indent=2)
    else:
        return json.dumps({"error": "API request failed", "status_code": response.status_code}, indent=2)

# Streamlit user interface
user_query = st.text_input("Enter your query:", help="Ask the AI Assistant anything you want to know.")

if user_query:
    # Call the function when the user enters a query
    response = ai_assistant_query(user_query)
    # Display the response from the AI Assistant API
    st.text_area("Response:", value=response, height=300)

st.markdown("## Virtual To-Do List Manager")
st.write("You can also manage your to-do list here by interacting with the respective API endpoints.")

# Interface for managing a to-do list through the API
task_action = st.selectbox("Choose action:", ["Add Task", "View Tasks", "Remove Task"])
task_description = st.text_input("Task Description:")

def manage_todo(action, description):
    """Manage to-do list via API calls."""
    url = 'https://nztinversive.github.io/Llama3functioncallling-/todo'
    if action == "Add Task":
        response = requests.post(url, json={"task": description})
    elif action == "Remove Task":
        response = requests.delete(url, params={"task": description})
    else:  # View Tasks
        response = requests.get(url)
    if response.status_code in [200, 201]:
        return json.dumps(response.json(), indent=2)
    else:
        return json.dumps({"error": "API request failed", "status_code": response.status_code}, indent=2)

if st.button("Execute Task Action"):
    todo_response = manage_todo(task_action, task_description)
    st.text_area("To-Do List Response:", value=todo_response, height=150)
