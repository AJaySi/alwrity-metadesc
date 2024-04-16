import time #Iwish
import os
import json
import openai
import streamlit as st
from streamlit_lottie import st_lottie
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)


def main():
    # Set page configuration
    st.set_page_config(
        page_title="Alwrity",
        layout="wide",
        page_icon="img/logo.png"
    )
    # Remove the extra spaces from margin top.
    st.markdown("""
        <style>
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
            background-color: #4A55A2;’
            color: #C5DFF8;
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

    # Sidebar input for OpenAI API Key
    st.sidebar.image("img/alwrity.jpeg", use_column_width=True)
    st.sidebar.markdown(f"🧕 :red[Checkout Alwrity], complete **AI writer & Blogging solution**:[Alwrity](https://alwrity.netlify.app)")
    
    # Title and description
    st.title("✍️ Alwrity - AI Blog Meta description Generator")
    st.markdown('''
                Generate SEO optimized Blog Meta description - powered by AI (OpenAI GPT-3, Gemini Pro).
                Implemented by [Alwrity](https://alwrity.netlify.app).
                Alwrity will do web research for given keywords OR Blog content.
                It will AI-lyze top meta descriptions and then generate 2 SEO optimized descriptions.
                ''')

    # Input section
    with st.expander("**PRO-TIP** - Read the instructions below.", expanded=True):
        input_blog_keywords = st.text_input('**Enter main keywords of your blog!** (2-3 words that define your blog)')
        input_blog_content = st.text_input('**Copy/Paste your entire blog content.** (Tip: Use Alwrity to write your blog)', 'Optional')
        col1, col2, space = st.columns([5, 5, 0.5])
        with col1:
            input_title_type = st.selectbox('Blog Type', ('General', 'How-to Guides', 'Tutorials', 'Listicles', 'Newsworthy Posts', 'FAQs', 'Checklists/Cheat Sheets'), index=0)
        with col2:
            input_title_intent = st.selectbox('Search Intent', ('Informational Intent', 'Commercial Intent', 'Transactional Intent', 'Navigational Intent'), index=0)

    # Generate Blog Title button
    if st.button('**Generate Meta Description**'):
        with st.spinner():
            if input_blog_content == 'Optional':
                input_blog_content = None

            # Clicking without providing data, really ?
            if (not input_blog_keywords) and (not input_blog_content):
                st.error('** 🫣Provide Inputs to generate Blog Tescription. Either Blog Keywords OR content, is required!**')
            elif input_blog_keywords or input_blog_content:
                blog_titles = generate_blog_metadesc(input_blog_keywords, input_blog_content, input_title_type, input_title_intent)
                if blog_titles:
                    st.subheader('**👩‍🔬👩‍🔬Go Rule search ranking with these Blog Meta descriptions!**')
                    with st.expander("** Final - Blog Meta description Output 🎆🎇 🎇 **", expanded=True):
                        st.markdown(blog_titles)
                else:
                    st.error("💥**Failed to generate blog meta description. Please try again!**")


# Function to generate blog metadesc
def generate_blog_metadesc(input_blog_keywords, input_blog_content, input_title_type, input_title_intent):
    """ Function to call upon LLM to get the work done. """
    # If keywords and content both are given.
    if input_blog_content and input_blog_keywords:
        prompt = f"""As a SEO expert, I will provide you with main 'blog keywords' and 'blog content'.
        Your task is write 3 SEO optimised blog meta descriptions, from given blog keywords and content.

        Follow the below guidelines for generating the blog meta descriptions:
        1). As SEO expert, follow all best practises for SEO optimised blog meta description.
        2). Your response should be optimised around given keywords and content.
        3). Optimise your response for web search intent {input_title_intent}.
        4). Optimise your response for blog type of {input_title_type}.\n

        blog keywords: '{input_blog_keywords}'\n
        blog content: '{input_blog_content}'
        """
    elif input_blog_keywords and not input_blog_content:
        prompt = f"""As a SEO expert, I will provide you with main 'keywords' of a blog.
        Your task is write 3 SEO optimised blog meta descriptions from given blog keywords.

        Follow the below guidelines for generating the blog meta descriptions:
        1). As SEO expert, follow all best practises for SEO optimised blog titles.
        2). Your response should be optimised around given keywords and content.
        3). Optimise your response for web search intent {input_title_intent}.
        4). Optimise your response for blog type of {input_title_type}.\n

        blog keywords: '{input_blog_keywords}'\n
        """
    elif input_blog_content and not input_blog_keywords:
        prompt = f"""As a SEO expert, I will provide you with a 'blog content'.
        Your task is write 3 SEO optimised blog meta descriptions from given blog content.

        Follow the below guidelines for generating the blog meta descriptions:
        1). As SEO expert, follow all best practises for SEO optimised blog meta description.
        2). Your response should be optimised around given keywords and content.
        3). Optimise your response for web search intent {input_title_intent}.
        4). Optimise your response for blog type of {input_title_type}.\n

        blog content: '{input_blog_content}'\n
        """
    blog_metadesc = openai_chatgpt(prompt)
    return blog_metadesc



@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def openai_chatgpt(prompt, model="gpt-3.5-turbo-0125", temperature=0.2, max_tokens=500, top_p=0.9, n=3):
    """
    Wrapper function for OpenAI's ChatGPT completion.

    Args:
        prompt (str): The input text to generate completion for.
        model (str, optional): Model to be used for the completion. Defaults to "gpt-4-1106-preview".
        temperature (float, optional): Controls randomness. Lower values make responses more deterministic. Defaults to 0.2.
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 8192.
        top_p (float, optional): Controls diversity. Defaults to 0.9.
        n (int, optional): Number of completions to generate. Defaults to 1.

    Returns:
        str: The generated text completion.

    Raises:
        SystemExit: If an API error, connection error, or rate limit error occurs.
    """
    # Wait for 10 seconds to comply with rate limits
    for _ in range(10):
        time.sleep(1)

    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=n,
            top_p=top_p
            # Additional parameters can be included here
        )
        return response.choices[0].message.content

    except openai.APIError as e:
        st.error(f"OpenAI API Error: {e}")
    except openai.APIConnectionError as e:
        st.error(f"Failed to connect to OpenAI API: {e}")
    except openai.RateLimitError as e:
        st.error(f"Rate limit exceeded on OpenAI API request: {e}")
    except Exception as err:
        st.error(f"OpenAI error: {err}")



# Function to import JSON data
def import_json(path):
    with open(path, "r", encoding="utf8", errors="ignore") as file:
        url = json.load(file)
        return url


if __name__ == "__main__":
    main()
