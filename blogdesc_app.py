import time #Iwish
import os
import json
import streamlit as st
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
import google.generativeai as genai


def main():
    # Set page configuration
    st.set_page_config(
        page_title="Alwrity",
        layout="wide",
    )
    # Remove the extra spaces from margin top.
    st.markdown("""
        <style>
                body {
                background-color: #333;
                color: #fff;
                }
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)
    st.markdown(f"""
      <style>
      [class="st-emotion-cache-7ym5gk ef3psqc12"]{{
            display: inline-block;
            padding: 5px 20px;
            background-color: #4681f4;
            color: #FBFFFF;
            width: 300px;
            height: 35px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            border-radius: 8px;’
      }}
      </style>
    """
    , unsafe_allow_html=True)

    # Hide top header line
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Hide footer
    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

    # Title and description
    st.title("✍️ Alwrity - AI Blog Meta Description Generator")
    
    # Input section
    with st.expander("**PRO-TIP** - Read the instructions below. 🚀", expanded=True):
        col1, col2, space = st.columns([5, 5, 0.5])
        with col1:
            keywords = st.text_input("🔑 Target Keywords (comma-separated):",
                                     placeholder="e.g., content marketing, SEO, social media, online business",
                                     help="Enter your target keywords, separated by commas. 📝")
            
            tone_options = ["Informative", "Engaging", "Humorous", "Intriguing", "Playful"]
            tone = st.selectbox("🎨 Desired Tone (optional):",
                                options=["General"] + tone_options,
                                help="Choose the overall tone you want for your meta description. 🎭")
        with col2:
            search_type = st.selectbox('🔍 Search Intent:', 
                                       ('Informational Intent', 'Commercial Intent', 'Transactional Intent', 'Navigational Intent'), 
                                       index=0)
            
            language_options = ["English", "Spanish", "French", "German", "Other"]
            language_choice = st.selectbox("🌐 Preferred Language:", 
                                           options=language_options,
                                           help="Select the language for your meta description. 🗣️")
            if language_choice == "Other":
                language = st.text_input("Specify Other Language:",
                                         placeholder="e.g., Italian, Chinese",
                                         help="Enter your preferred language. 🌍")
            else:
                language = language_choice

    # Generate Blog Title button
    if st.button('**✨ Generate Meta Description ✨**'):
        with st.spinner("Crafting your Meta descriptions... ⏳"):

            # Validate input fields
            if not keywords:
                st.error('**🫣 Blog Keywords are required!**')
            else:
                blog_metadesc = generate_blog_metadesc(keywords, tone, search_type, language)
                if blog_metadesc:
                    st.subheader('**🎉 Your SEO-Boosting Blog Meta Descriptions! 🚀**')
                    with st.expander("**Final - Blog Meta Description Output 🎆🎇**", expanded=True):
                        st.markdown(blog_metadesc)
                else:
                    st.error("💥 **Failed to generate blog meta description. Please try again!**")


# Function to generate blog metadesc
def generate_blog_metadesc(keywords, tone, search_type, language):
    """ Function to call upon LLM to get the work done. """
    prompt = f"""
        Craft 3 engaging and SEO-friendly meta descriptions for a blog post based on the following details:

        Blog Post Keywords: {keywords}
        Search Intent Type: {search_type}
        Desired Tone: {tone}
        Preferred Language: {language}

        Output Format:

        Respond with 3 compelling and concise meta descriptions, approximately 155-160 characters long, that incorporate the target keywords, reflect the blog post content, resonate with the target audience, and entice users to click through to read the full article.
    """
    with st.spinner("Calling Gemini to craft 3 Meta descriptions for you... 💫"):
        blog_metadesc = gemini_text_response(prompt)
    
    return blog_metadesc



@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def gemini_text_response(prompt):
    """ Common functiont to get response from gemini pro Text. """
    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    except Exception as err:
        st.error(f"Failed to configure Gemini: {err}")
    # Set up the model
    generation_config = {
        "temperature": 0.6,
        "top_p": 0.3,
        "top_k": 1,
        "max_output_tokens": 1024
    }
    # FIXME: Expose model_name in main_config
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash", generation_config=generation_config)
    try:
        # text_response = []
        response = model.generate_content(prompt)
        return response.text
    except Exception as err:
        st.error(response)
        st.error(f"Failed to get response from Gemini: {err}. Retrying.")



if __name__ == "__main__":
    main()
