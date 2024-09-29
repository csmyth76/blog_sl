
# 💍 Wedding Blog Post Generator

## Overview

The Wedding Blog Post Generator is a Streamlit-based web application designed to help wedding photographers create SEO-optimized blog posts about weddings they've photographed. This tool streamlines the process of creating engaging, personalized content that can attract potential clients and improve the photographer's online presence.

## Key Features

1. **User-Friendly Interface**: Utilizes Streamlit for an intuitive, easy-to-use web interface.
2. **Customizable Inputs**: Collects detailed information about the wedding, couple, and photographer.
3. **AI-Powered Content Generation**: Leverages OpenAI's GPT models to create unique, high-quality blog posts.
4. **SEO Optimization**: Incorporates user-defined keywords for better search engine visibility.
5. **Permalink Generation**: Automatically creates SEO-friendly URLs for each blog post.
6. **Test Mode**: Allows quick testing and demonstration with pre-filled sample data.
7. **Download Option**: Enables users to download the generated blog post as an HTML file.

## System Architecture

The application is structured into several modules, each responsible for a specific function:

1. **main.py**: The entry point of the application, orchestrating the overall flow.
2. **input_handling.py**: Manages user input collection through the Streamlit interface.
3. **data_processing.py**: Processes and prepares user inputs for content generation.
4. **blog_generation.py**: Interacts with the OpenAI API to generate the blog post content.
5. **permalink_generation.py**: Creates SEO-friendly permalinks for the blog posts.
6. **output_display.py**: Handles the presentation of the generated content and permalink.
7. **config.py**: Stores configuration data like sample inputs and available AI models.


## Technical Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.11+
- **AI Integration**: OpenAI API (GPT-3.5 and GPT-4 models)
- **Additional Libraries**: 
  - `unidecode`: For handling non-ASCII characters in permalinks
  - `openai`: For interacting with the OpenAI API

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/wedding-blog-post-generator.git
   cd wedding-blog-post-generator
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   - Create a `.streamlit/secrets.toml` file in the project root
   - Add your API key to this file:
     ```
     api_key = "your-openai-api-key-here"
     ```

5. Run the application:
   ```
   streamlit run streamlit_app.py
   ```

## Usage Guide

1. **Input Wedding Details**: Fill in the required fields about the wedding, couple, and photographer.
2. **Set Blog Post Goals**: Choose the desired tone and enter SEO keywords.
3. **Generate Content**: Click the "Generate Blog Post" button to create the blog post.
4. **Review and Download**: Review the generated content and download the HTML file if satisfied.

## Development Workflow

1. **Feature Development**: Create a new branch for each feature or bug fix.
2. **Testing**: Thoroughly test new features using the test mode.
3. **Code Review**: Submit a pull request for code review before merging into the main branch.
4. **Documentation**: Update this README and any other relevant documentation as needed.
