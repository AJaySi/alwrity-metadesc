# Alwrity AI MetaDesc Generator tool

**AI Blog Meta Description App**

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Overview

Alwrity MetaDesc is an AI-powered application designed to generate optimized meta descriptions for blogs and articles. Writing meta descriptions manually can be time-consuming and prone to errors. This app uses natural language processing (NLP) techniques to create concise, engaging, and SEO-friendly meta descriptions, ensuring your content is better indexed by search engines and attracts more readers.

---

## Features

- **AI-Powered Meta Description Generation**: Automatically generate meta descriptions for blogs and articles using advanced machine learning models.
- **Gemini 2.0 Flash Model**: Upgraded to the Gemini 2.0 Flash model for state-of-the-art content generation.
- **User Input for API Keys**: Users can now input their API keys for Gemini, SERPER, and Exa/Metaphor directly in the UI.
- **Clickable Links for API Keys**: Provided clickable links in the UI for users to easily obtain the required API keys.
- **Competitor Meta Description Research**: Utilize SERPER or Exa/Metaphor API keys to analyze competitor meta descriptions.
- **Flexible Input Options**: Users can now provide either full blog content or a URL to rewrite meta descriptions.
- **Multiple Meta Descriptions**: Option to generate 1–10 meta descriptions per request, giving users flexibility and choice.
- **Excel Export for AB Testing**: Download generated meta descriptions as an Excel file for easy AB testing.
- **Improved UI/UX**: Enhanced user interface for clarity and ease of use, ensuring a seamless experience.
- **Batch Processing**: Process multiple articles at once, saving time for content creators and marketers.
- **SEO Optimization**: Ensure descriptions are concise, keyword-rich, and within the recommended character limits for better search engine visibility.

---

## Installation

Follow these steps to set up the project on your local machine:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AJaySi/alwrity-metadesc.git
   ```
2. **Navigate to the Project Directory**
   ```bash
   cd alwrity-metadesc
   ```
3. **Create a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   - **Note**: Make sure `openpyxl` is installed for Excel export functionality.
5. **Run the Application**
   ```bash
   streamlit run meta_desc.py
   ```

---

## Usage

1. Launch the application using the installation steps above.
2. Enter the blog content or provide a URL to rewrite the meta description.
3. Input your API keys for Gemini, SERPER, and Exa/Metaphor in the designated fields (links are provided to obtain these keys).
4. Customize the parameters:
   - Select 1–10 meta descriptions to generate.
   - Adjust the tone, length, or focus keywords as needed.
5. Use the competitor analysis feature (optional) to research meta descriptions using SERPER or Exa/Metaphor APIs.
6. Click the "Generate Meta Description" button to receive optimized outputs.
7. Export generated meta descriptions to an Excel file for AB testing.
8. Copy and paste the generated meta description(s) into your blog or CMS.

---

## Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add feature description"
   ```
4. Push to your forked repository:
   ```bash
   git push origin feature-name
   ```
5. Create a pull request, and we’ll review it as soon as possible.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Contact

If you have any questions, suggestions, or feedback, feel free to reach out:

- **GitHub**: @uniqueumesh

---
