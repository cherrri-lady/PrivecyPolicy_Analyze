import streamlit as st
import openai
import re

# Azure OpenAI Setup
endpoint = "https://i24b-m4vuvytn-swedencentral.cognitiveservices.azure.com/"
deployment = "gpt-35-turbo-16k"
api_key = "AIM9tWzz3sM5Hj1ZO0kBlg07oI27FBONn5vyZHmbEqYkuTp4QsT9JQQJ99ALACfhMk5XJ3w3AAAAACOGOj2l"  # Replace with your Azure OpenAI API key

# Configure OpenAI with Azure settings
openai.api_type = "azure"
openai.api_base = endpoint  # Azure endpoint
openai.api_version = "2024-08-01-preview"
openai.api_key = api_key  # Azure API key

# Streamlit App
st.title("Privacy Policy Analyzer")
st.markdown("Interact with Azure OpenAI GPT models directly from this app.")

# Input box for user query
user_input = st.text_area("Enter the privacy policy text:", placeholder="Paste privacy policy here...", height=200)

# Button to send the request
if st.button("Analyze"):
    if user_input.strip():
        # Enhanced check for privacy policy-related text using regex and keywords
        keywords = [
            "privacy policy", "personal information", "cookies", "data protection", 
            "information collected", "third-party", "opt-out", "terms of service", "confidentiality"
        ]
        # Check if the input text contains multiple privacy policy-related terms
        if any(re.search(r"\b" + keyword + r"\b", user_input, re.IGNORECASE) for keyword in keywords):
            # Prepare the prompt for summarizing, classifying, and rating the privacy policy
            chat_prompt = [
                {"role": "system", "content": "You are an assistant that summarizes and classifies privacy policy text. Highlight the risks related to data privacy in the policy and return each risk in a human-readable format. For each risk, rate it on a scale of 1 to 10 (1 being low risk, 10 being high risk). Clearly label each risk and its corresponding rating."},
                {"role": "user", "content": user_input}
            ]

            try:
                # Send request to Azure OpenAI
                completion = openai.ChatCompletion.create(
                    engine=deployment,  # Use 'engine' for deployment name in Azure
                    messages=chat_prompt,
                    max_tokens=800,
                    temperature=0.7,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0
                )

                # Extract and display the response
                response = completion.choices[0].message["content"]

                # Post-process the response to ensure it's split into separate lines properly
                # Add new lines before labels like "Company:", "Potential data leak:", etc.
                formatted_response = re.sub(r"([A-Za-z ]+:)", r"\n\1", response)  # Add newline before labels

                # Ensure the rating appears clearly for each risk
                st.subheader("Summarize, Classify and Rate Risk:")
                st.write(formatted_response.strip())

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            # If the input is not related to privacy policy, inform the user
            st.warning("Sorry, I can only summarize and classify privacy policies. I cannot process other types of requests like general questions or programming queries.")
    else:
        st.warning("Please enter the privacy policy text.")

# Footer
st.caption("Powered by Azure OpenAI and Streamlit.")
