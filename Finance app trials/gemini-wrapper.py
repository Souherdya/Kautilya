import google.generativeai as genai
import os
import matplotlib.pyplot as plt
import streamlit as st
import math
import json
import ast

genai.configure(api_key="AIzaSyDoUhhl2FMzvOUeMUvKudWKbZ9-azGey18")  # Securely load API key
model = genai.GenerativeModel("gemini-1.5-flash")

def advisory(risk):

    risk_options = {
        "Low" : ["Index Funds/ETFs","Large cap mutual funds","Dividend stocks"],
        "Medium" : ["Mid-cap stocks/Mutual funds","Sectoral/Thematic funds","Debt funds/bonds","Gold ETFs"],
        "High" : ["Small-cap funds/mutual funds","IPO investments","High-growth sector stocks","Cryptocurrency"]
    }

    choice_option = ""

    if risk in risk_options.keys():
        choice_option = ",".join(risk_options[risk])
    
    return choice_option


def growthCalculator(initial,goal,time):

    approximated_growth_percentage = (float(goal) - float(initial))/(float(initial)*float(time))
    return round(approximated_growth_percentage * 100, 2)


# Function to get outputs from Google Gemini API
def getOutputs(initial, goal, time, risk):
    approximated_growth_needed = growthCalculator(initial=initial,goal=goal,time=time)
    options = advisory(risk=risk)

    
    prompt = (
        f"You are a financial advisor. Given an expected yearly growth rate of {approximated_growth_needed} "
        f"provide financial advice on available options to buy in {options}, and also what percentage of my money to allocate to which"
        "Give shorter and concised points for better readability and understanding, also be specific with option names"
        "Only give names of the given options list and one explanatory sentence each. focus mainly on names"
    )
    
    response = model.generate_content(prompt)  # Correctly pass the prompt
    return response.text  # Return generated text


def codifyOutput(prompt):

    new_prompt = (
        f"In this given prompt {prompt}, we have investment options along with corresponding percentages"
        "I want to get a code-friendly array of arrays type format like [['option_name',30%],['option_name',30%],['option_name',40%]] with corresponding given percentages"
        "Give only one output as text in one line"
    )

    response = model.generate_content(new_prompt)
    return response.text

# Streamlit UI
def renderUI():
    st.title("Financial Advisory")

    # Create a form
    with st.form("user_input_form"):
        initial = st.text_input("Enter Initial amount (Lump-sum):")
        goal = st.text_input("Enter Goal amount:")
        time = st.text_input("Enter Time (years):")
        
        choice = st.radio(
            "How much risk are you willing to take?",
            ["High", "Medium", "Low"]
        )
        
        # Submit button
        submitted = st.form_submit_button("Submit")

    # Display output dynamically when form is submitted
    if submitted:
        st.subheader("Generated Output:")
        
        with st.spinner("Processing... Please wait ⏳"):
            output_sub = getOutputs(initial, goal, time, choice)
            output_main = codifyOutput(output_sub)
            output_main =  ast.literal_eval(output_main)
            print(output_main)
        # Display result after loading
        st.success("Done! ✅")
        with st.container():
            col1, col2, = st.columns(2)
            
            # Place widgets or content in the columns
            
            with col1:
                st.header(f"{output_main[0][0]}")
                st.subheader(f"{output_main[0][1]}% of your lumpsum")
                st.write("Approximated amount = ", round((float(initial)*output_main[0][1])/100 , 0))
                
            with col2:
                st.header(f"{output_main[1][0]}")
                st.subheader(f"{output_main[1][1]}% of your lumpsum")
                st.write("Approximated amount = ", round((float(initial)*output_main[1][1])/100 , 0))
                
        with st.container():
            col3,col4 = st.columns(2)
            with col3:
                st.header(f"{output_main[2][0]}")
                st.subheader(f"{output_main[2][1]}% of your lumpsum")
                st.write("Approximated amount = ", round((float(initial)*output_main[2][1])/100 , 0))
            with col4:
                st.header(f"{output_main[3][0]}")
                st.subheader(f"{output_main[3][1]}% of your lumpsum")
                st.write("Approximated amount = ", round((float(initial)*output_main[3][1])/100 , 0))
                

        with st.container():
            labels = []
            data = []
            for i in output_main:
                labels.append(i[0])
                data.append(i[1])
            
            st.write(output_main)

            # Create a pie chart
            fig, ax = plt.subplots()
            ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': "black", 'linewidth': 2},textprops={'color': 'white'})
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            fig.patch.set_alpha(0.0)
            # Display the pie chart
            st.pyplot(fig)

# Corrected main guard
if __name__ == "__main__":
    renderUI()