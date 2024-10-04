# Meeting Reporter

## Overview

Meeting Reporter is a Streamlit application that generates high-quality news articles based on the transcripts of commission meetings. It uses AI-powered assistants to analyze meeting transcripts, identify important stories, and produce well-structured, informative articles.

## Features

- Extracts transcripts from YouTube videos of commission meetings
- Utilizes AI to identify key stories from the meeting
- Generates headlines and detailed articles for each important topic
- Performs fact-checking and name verification through web searches
- Provides a user-friendly interface via Streamlit

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/meeting-reporter.git
   cd meeting-reporter
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv reporter_env
   source reporter_env/bin/activate  # On Windows, use `reporter_env\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `secrets.toml` file in the `.streamlit` directory:
   ```
   mkdir .streamlit
   touch .streamlit/secrets.toml
   ```

2. Add your API keys to the `secrets.toml` file:
   ```toml
   anthropic_key = "your_anthropic_api_key"
   serp_api_key = "your_serpapi_key"
   ```

## Usage

1. Ensure your virtual environment is activated.

2. Run the Streamlit app:
   ```
   streamlit run reporter.py
   ```

3. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

4. Paste the YouTube link of the commission meeting in the input field and press Enter.

5. Wait for the AI to process the transcript and generate the articles.

## Project Structure

- `reporter.py`: Main application file containing the Streamlit interface and AI logic
- `requirements.txt`: List of Python package dependencies
- `.streamlit/secrets.toml`: Configuration file for API keys (not included in repository)

## Contributing

Contributions to improve Meeting Reporter are welcome. Please feel free to submit a Pull Request.

## License

[Specify your license here, e.g., MIT, GPL, etc.]

## Disclaimer

This tool is for informational purposes only. Always verify the generated content against official sources before publication or distribution.