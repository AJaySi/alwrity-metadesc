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
import io


def main():
    # Set page configuration
    st.set_page_config(
        page_title="Alwrity AI Meta description Generator",
        layout="wide",
    )
    # Remove the extra spaces from margin top.
    st.markdown("""
        <style>
                ::-webkit-scrollbar-track {
        background: #e1ebf9;
        }

        ::-webkit-scrollbar-thumb {
            background-color: #90CAF9;
            border-radius: 10px;
            border: 3px solid #e1ebf9;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #64B5F6;
        }

        ::-webkit-scrollbar {
            width: 16px;
        }
        div.stButton > button:first-child {
            background: #1565C0;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 2px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            font-weight: bold;
        }
        </style>
    """
    , unsafe_allow_html=True)

    # Hide top header line
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Hide footer
    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

    # Tool title and description at the top
    st.markdown('<h1 style="display:flex;align-items:center;font-size:2.5rem;gap:0.5rem;">🪄 Alwrity Meta Description Generator</h1>', unsafe_allow_html=True)
    st.markdown('<div style="color:#1976D2;font-size:1.2rem;margin-bottom:1.5rem;">Create SEO-optimized, click-worthy meta descriptions in seconds.</div>', unsafe_allow_html=True)

    # --- API Key Input Section (SERPER/Exa/Metaphor) ---
    with st.expander("API Configuration 🔑", expanded=False):
        st.markdown('''If the default Gemini API key is unavailable or exceeds its limits, you can provide your own API key below.<br>
        <a href="https://aistudio.google.com/app/apikey" target="_blank">Get Gemini API Key</a> | 
        <a href="https://serper.dev" target="_blank">Get SERPER API Key</a> | 
        <a href="https://docs.exa.ai/reference/getting-started" target="_blank">Get Exa/Metaphor API Key</a>
        ''', unsafe_allow_html=True)
        user_gemini_api_key = st.text_input("Gemini API Key", type="password", help="Provide your Gemini API Key if the default key is unavailable.")
        user_serper_api_key = st.text_input("SERPER API Key (for competitor research)", type="password", help="Optional: For researching competitor meta descriptions.")
        user_metaphor_api_key = st.text_input("Exa/Metaphor API Key (for competitor research)", type="password", help="Optional: For researching competitor meta descriptions.")

    # --- Research competitor meta descriptions toggle ---
    research_competitors = st.checkbox("Research competitor meta descriptions for my keyword", value=False, help="If enabled, the tool will research top-ranking pages for your keyword and use their meta descriptions as inspiration.")

    # --- User can provide blog content or URL ---
    st.markdown('<h3 style="margin-top:2rem;">2️⃣ Enter Your Details</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        keywords = st.text_input("🔑 Target Keywords", placeholder="e.g., content marketing, SEO, social media", help="Enter your target keywords, separated by commas.")
        tone = st.selectbox("🎨 Tone", options=["General", "Informative", "Engaging", "Humorous", "Intriguing", "Playful"], help="Choose the overall tone for your meta description.")
        blog_content = st.text_area("📝 Paste your blog content (optional)", placeholder="Paste your full blog post here if you want the meta description to be based on it.")
    with col2:
        search_type = st.selectbox('🔍 Search Intent', ('Informational Intent', 'Commercial Intent', 'Transactional Intent', 'Navigational Intent'), index=0)
        language_choice = st.selectbox("🌐 Language", ["English", "Spanish", "French", "German", "Other"], help="Select the language for your meta description.")
        if language_choice == "Other":
            language = st.text_input("Specify Language", placeholder="e.g., Italian, Chinese", help="Enter your preferred language.")
        else:
            language = language_choice
        page_url = st.text_input("🔗 URL of existing page (optional)", placeholder="https://yourpage.com/article", help="Paste the URL of your existing page to rewrite its meta description.")

    # --- User can choose number of meta descriptions ---
    num_meta = st.slider("How many meta descriptions do you want to generate?", min_value=1, max_value=10, value=5, help="Choose between 1 and 10 meta descriptions.")

    # --- Step 3: Generate Button ---
    st.markdown('<h3 style="margin-top:2rem;">3️⃣ Generate Meta Descriptions</h3>', unsafe_allow_html=True)
    if st.button('✨ Generate Meta Description'):
        with st.spinner("Crafting your Meta descriptions... ⏳"):
            if not keywords and not blog_content and not page_url:
                st.error('Please enter your target keywords, blog content, or a page URL!')
            else:
                gemini_api_key = user_gemini_api_key or os.getenv('GEMINI_API_KEY')
                serper_api_key = user_serper_api_key or os.getenv('SERPER_API_KEY')
                metaphor_api_key = user_metaphor_api_key or os.getenv('METAPHOR_API_KEY')
                competitor_meta = ""
                if research_competitors and (serper_api_key or metaphor_api_key) and keywords:
                    competitor_meta = fetch_competitor_meta_descriptions(keywords, serper_api_key, metaphor_api_key)
                page_meta = ""
                if page_url:
                    page_meta = fetch_page_meta_description(page_url)
                blog_metadesc = generate_blog_metadesc(keywords, tone, search_type, language, gemini_api_key, blog_content, competitor_meta, page_meta, num_meta)
                if blog_metadesc:
                    st.subheader('**🎉 Your SEO-Boosting Blog Meta Descriptions! 🚀**')
                    with st.expander("**Final - Blog Meta Description Output 🎆🎇**", expanded=True):
                        st.markdown(blog_metadesc)
                        # --- Download as Excel ---
                        import pandas as pd
                        meta_list = [desc.strip() for desc in blog_metadesc.split('\n') if desc.strip()]
                        df = pd.DataFrame({"Meta Description": meta_list})
                        output = io.BytesIO()
                        df.to_excel(output, index=False, engine='openpyxl')
                        output.seek(0)
                        st.download_button(
                            label="Download as Excel for AB Testing",
                            data=output,
                            file_name="meta_descriptions.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                else:
                    st.error("Failed to generate blog meta description. Please try again!")


# Function to generate blog metadesc
def generate_blog_metadesc(keywords, tone, search_type, language, gemini_api_key, blog_content=None, competitor_meta=None, page_meta=None, num_meta=5):
    """ Function to call upon LLM to get the work done. """
    prompt = f"""
You are an expert SEO copywriter. Write {num_meta} unique, engaging, and SEO-optimized meta descriptions for a blog post using the details below.\n"""
    if keywords:
        prompt += f"Blog Post Keywords: {keywords}\n"
    if search_type:
        prompt += f"Search Intent Type: {search_type}\n"
    if tone:
        prompt += f"Desired Tone: {tone}\n"
    if language:
        prompt += f"Preferred Language: {language}\n"
    if blog_content:
        prompt += f"\nBlog Content: {blog_content}\n"
    if competitor_meta:
        prompt += f"\nCompetitor Meta Descriptions (for inspiration):\n{competitor_meta}\n"
    if page_meta:
        prompt += f"\nCurrent Meta Description from the page (rewrite this):\n{page_meta}\n"
    prompt += f"""
Follow these SEO best practices:
- Each meta description must be between 150 and 160 characters.
- Clearly summarize the blog post content and match the user's search intent.
- Naturally include the target keywords without keyword stuffing.
- Make each description unique, compelling, and action-oriented to encourage clicks.
- Ensure each description accurately reflects the page content and is not misleading.
- Avoid using quotation marks.
- Write in a clear, natural, and human-friendly style.
- If space allows, you may include a brand mention at the end.

Output Format:
Respond with {num_meta} numbered meta descriptions, each on a new line, and do not include any explanations or extra text.
"""
    with st.spinner(f"Calling Gemini to craft {num_meta} Meta descriptions for you... 💫"):
        blog_metadesc = gemini_text_response(prompt, gemini_api_key)
    return blog_metadesc


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def gemini_text_response(prompt, api_key):
    """ Common functiont to get response from gemini pro Text. """
    try:
        genai.configure(api_key=api_key)
    except Exception as err:
        st.error(f"Failed to configure Gemini: {err}")
    # Set up the model
    generation_config = {
        "temperature": 0.6,
        "top_p": 0.3,
        "top_k": 1,
        "max_output_tokens": 1024
    }
    # Use Gemini 2.0 Flash model
    model = genai.GenerativeModel(model_name="models/gemini-2.0-flash", generation_config=generation_config)
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as err:
        st.error(f"Failed to get response from Gemini: {err}. Retrying.")

    st.markdown('<div class="footer">Made with ❤️ by Alwrity | <a href="https://www.alwrity.com/" style="color:#1976D2;">Support</a></div>', unsafe_allow_html=True)


def fetch_competitor_meta_descriptions(keywords, serper_api_key, metaphor_api_key):
    """Fetch meta descriptions from top competitors using SERPER or Metaphor API."""
    # Placeholder: In production, call the actual API and parse meta descriptions
    # For now, return a string with example meta descriptions
    return "Competitor 1: Example meta description.\nCompetitor 2: Example meta description.\nCompetitor 3: Example meta description."


def fetch_page_meta_description(url):
    """Fetch the meta description from a given URL."""
    # Placeholder: In production, fetch and parse the page's meta description
    # For now, return a string with an example meta description
    return "Current meta description from the page."


if __name__ == "__main__":
    main()
