import streamlit as st
import openai
import os
import time

from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key=os.getenv("API_key")
)

context = """This app utilizes advanced AI algorithms to analyze and interpret users' dreams, 
providing insightful explanations based on symbolism, psychology, and cultural references. 
Please provide details about your dream, and the app will generate a personalized interpretation for you."""

async def generate_response(question, context):
    model = "gpt-3.5-turbo"
    completion = await client.chat.completions.create(model=model, 
        messages=[{"role": "user", "content": question}, 
                {"role": "system", "content": context}])
    return completion.choices[0].message.content

async def app():
    if "current_form" not in st.session_state:
        st.session_state["current_form"] = 1    

    if "description" not in st.session_state:
        st.session_state["description"] = None

    if "current_life" not in st.session_state:
        st.session_state["current_life"] = None
    
    if "selected_genre" not in st.session_state:
        st.session_state["selected_genre"] = None
        
    # Display the appropriate form based on the current form state
    if st.session_state["current_form"] == 1:
        await display_description_form1()
    elif st.session_state["current_form"] == 2:
        await display_interpretation3()

async def display_description_form1():
    form1 = st.form("Introduction")
    form1.subheader("Dream Interpreter")
    
    text = """Cherry Mirra Calisnao     BSCS 3A \n
    CCS 229 - Intelligent Systems \n
    Final Project in Intelligent Systems \n
    College of Information and Communications Technology
    West Visayas State University"""
    form1.text(text)

    form1.image("dreaming.jpg", caption="Dream Interpreter App", use_column_width=True)
    text = """An AI-driven dream interpreter designed to help users explore the meanings and symbolism behind their dreams, 
    offering insights and explanations based on psychological principles and cultural references."""
    form1.write(text)
    
    # Prompt user for description
    description = form1.text_input("Describe what happened in your dream, specifying the details", key="description")

    current_life = form1.number_input("What are your current life circumstances/feelings/thoughts that can be associated with your dream?", key="current_life")
    
    # Display possible genres
    possible_genre = [
        "Adventure",
        "Nightmare",
        "Fantasy",
        "Surreal",
        "Romance",
        "Action",
        "Sci-fi",
        "Mystery",
        "Historical",
        "Comedy",
        "Other",
    ]

    selected_genre = form1.selectbox("Select the genre of your dream:", options=possible_genre)

    submit1 = form1.form_submit_button("Submit")

    if submit1:
        if description:
            st.session_state["description"] = description
            st.session_state["current_life"] = current_life
            
            if selected_genre == "Other":
                st.session_state["current_form"] = 2  # Skip to interpretation form directly
            else:
                st.session_state["selected_genre"] = selected_genre
                st.session_state["current_form"] = 2  # Move to the interpretation form
            await display_interpretation3(possible_genre, description, current_life)  # Call the interpretation form
        else:
            form1.warning("Please enter the details or description of your dream.")       

async def display_interpretation3():
    form3 = st.form("Dream Interpretation")
    
    description = st.session_state["description"]
    current_life = st.session_state["current_life"]
    selected_genre = st.session_state["selected_genre"]
    
    form3.write(f"Description: {description}")
    form3.write(f"Current Life: {current_life}")
    form3.write(f"Selected Genre: {selected_genre}")
    
    question = f"Provide insights and explanations based on the {description} of the dream, {current_life} circumstances, and {selected_genre}. Interpret the symbolism, psychology, and cultural references within the dream."
    progress_bar = form3.progress(0, text="The AI co-pilot is processing the request, please wait...")
    response = await generate_response(question, context)
    form3.write("Dream Interpretation:")
    form3.write(response)

    # update the progress bar
    for i in range(100):
        # Update progress bar value
        progress_bar.progress(i + 1)
        # Simulate some time-consuming task (e.g., sleep)
        time.sleep(0.01)
    # Progress bar reaches 100% after the loop completes
    form3.success("Dream interpretation completed!") 

    done = form3.form_submit_button("Done")  # Add the submit button
    if done:
        st.session_state["current_form"] = 1  # Return to the main screen

# Run the app
if __name__ == "__main__":
    import asyncio
    asyncio.run(app())
