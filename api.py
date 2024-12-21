import streamlit as st
import openai

# Fetch the API key securely from secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Azure OpenAI Setup
endpoint = "https://i24b-m4vuvytn-swedencentral.cognitiveservices.azure.com/"
deployment = "gpt-35-turbo-16k"

openai.api_type = "azure"
openai.api_base = endpoint  # Azure endpoint
openai.api_version = "2024-08-01-preview"
openai.api_key = api_key  # Azure API key

# Streamlit App
st.title("Privacy Policy Analyzer")
#st.markdown("Interact with Azure OpenAI GPT models directly from this app.")

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
        if any(keyword.lower() in user_input.lower() for keyword in keywords):
            chat_prompt = [
                {"role": "system", "content": "You are an assistant that summarizes and classifies privacy policy text. Highlight the risks related to data privacy in the policy and return each risk in a human-readable format. For each risk, rate it on a scale of 1 to 10 (1 being low risk, 10 being high risk). Clearly label each risk and its corresponding rating."},
                {"role": "user", "content": user_input}
            ]
            try:
                # Correct syntax for new OpenAI API
                response = openai.ChatCompletion.create(
                    deployment_id=deployment,  # Use 'deployment_id' for Azure
                    messages=chat_prompt,
                    max_tokens=800,
                    temperature=0.7,
                    top_p=0.95
                )
                # Display the response
                st.subheader("Summarize, Classify and Rate Risk:")
                st.write(response['choices'][0]['message']['content'].strip())

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Sorry, I can only summarize and classify privacy policies.")
    else:
        st.warning("Please enter the privacy policy text.")
