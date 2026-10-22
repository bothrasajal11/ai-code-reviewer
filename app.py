import streamlit as st
import time
from google import genai
from google.genai.errors import APIError

# Page Configuration
st.set_page_config(page_title="AI Code Reviewer", page_icon="🤖", layout="wide")

st.title("🤖 AI-Driven Code Review & Refactoring Bot")
st.markdown("Paste your code below to detect hidden bugs, security risks, and get optimized code instantly.")

# Settings Sidebar
st.sidebar.header("🔐 Settings & Access")
user_email = st.sidebar.text_input("Student/Developer Email", placeholder="you@college.edu")
api_key_input = st.sidebar.text_input("Gemini API Key", type="password", placeholder="Paste key here")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Input Code")
    language = st.selectbox("Select Language", ["Python", "JavaScript", "Java", "C++", "C#"])
    code_input = st.text_area("Paste your source code here:", height=300, placeholder="def add(a, b):\n    return a + b")
    analyze_btn = st.button("🚀 Run Code Review", type="primary")

with col2:
    st.subheader("🔍 Review & Analysis Report")
    
    if analyze_btn:
        if not user_email:
            st.warning("⚠️ Please enter your email in the sidebar.")
        elif not code_input.strip():
            st.warning("⚠️ Please paste some code to review.")
        elif not api_key_input.strip():
            st.error("❌ Please paste your Gemini API Key in the sidebar.")
        else:
            api_key = api_key_input.strip()
            
            with st.spinner("Connecting to Gemini AI Engine... 🧠"):
                try:
                    # Client initialize
                    client = genai.Client(api_key=api_key)
                    
                    prompt = f"""
                    You are an expert senior software engineer and security auditor. 
                    Review the following {language} code snippet. Provide your analysis in clear Markdown format with these exact sections:
                    1. 🐛 **Bug Detection & Logic Errors**: Identify syntax, runtime, or logical flaws.
                    2. 🔒 **Security Vulnerabilities**: Point out security risks.
                    3. ⚡ **Performance & Best Practices**: Suggest efficiency improvements.
                    4. ✨ **Refactored Code**: Provide the clean, corrected, and optimized version of the code inside a code block.

                    Code to review:
                    ```{language.lower()}
                    {code_input}
                    ```
                    """
                    
                    # Call API with retry mechanism for 503 high traffic handling
                    response = None
                    max_retries = 3
                    
                    for attempt in range(max_retries):
                        try:
                            response = client.models.generate_content(
                                model='gemini-3.8-flash',
                                contents=prompt,
                            )
                            break # Request successful! Break loop
                        except APIError as e:
                            if "503" in str(e) and attempt < max_retries - 1:
                                st.info("Server busy, retrying in 2 seconds... ⏳")
                                time.sleep(2)
                            else:
                                raise e
                    
                    if response and response.text:
                        st.success(f"Review completed successfully for: {user_email}")
                        st.markdown(response.text)
                        
                except Exception as e:
                    st.error(f"Execution Error: {e}")