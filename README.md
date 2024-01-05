# YouTube Analytics Project

## Overview

The YouTube Analytics project is a web application built to search for YouTube videos, retrieve analytics and sentiment analysis for selected videos, and provide a chatbot interface for user interaction. It leverages Flask for the backend, various APIs for YouTube data retrieval, and includes features such as sentiment analysis, summarization, and a chatbot.

## Project Structure

The project is organized into the following main components:

- **`app.py`**: The Flask application handling the backend logic and routes.
- **`templates/`**: HTML templates for the frontend, including search results and analytics views.


## Features

1. **YouTube Video Search:** Allows users to search for YouTube videos.
2. **Analytics View:** Provides detailed analytics for selected videos, including likes, views, and sentiment analysis of top comments.
3. **Summarization:** Summarizes video transcripts using various models.
4. **Chatbot Interface:** Enables users to interact with a chatbot based on video context.

## Getting Started

To run the project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/Swastik-Dubey/youtube_analytics.git
   cd youtube_analytics
   
2.Install dependencies:
   ```bash
    pip install -r requirements.txt
```
## Configuration

Before running the application, you need to configure your YouTube Data API key. Follow the steps below:

1. **Get YouTube Data API Key:**
   - Go to the [Google Cloud Console](https://console.developers.google.com/).
   - Create a new project or select an existing one.
   - Navigate to the "APIs & Services" > "Dashboard" and click on the "+ ENABLE APIS AND SERVICES" button.
   - Search for "YouTube Data API v3" and enable it for your project.
   - Once enabled, go to "Credentials" and create an API key.

2. **Replace 'YOUR_API_KEY' in `app.py`:**
   - Open the `app.py` file.
   - Locate the line with `API_KEY = 'YOUR_API_KEY'`.
   - Replace 'YOUR_API_KEY' with the API key you obtained from the Google Cloud Console.

```python
# Replace 'YOUR_API_KEY' with your actual YouTube Data API key
API_KEY = 'YOUR_ACTUAL_API_KEY'
```
### Hugging Face Access Key

To use Hugging Face models for summarization and question-answering, you need to obtain an access key from Hugging Face. Follow the steps below:

Get Hugging Face Access Key:

Go to Hugging Face.
- Sign in or create a new account.
- Once logged in, go to your settings page.
- Copy the API key.
  
Replace 'YOUR_HUGGING_FACE_KEY' in app.py:
- Open the app.py file.
- Locate the line with headers = {"Authorization": "Bearer YOUR_HUGGING_FACE_KEY"}.
- Replace 'YOUR_HUGGING_FACE_KEY' with the access key you obtained from Hugging Face.
# Define the headers variable
 ```bash
headers = {"Authorization": "Bearer YOUR_HUGGING_FACE_KEY"}
```

3.Run the Flask application:
 ```bash
python app.py
```
4.Access the application at http://localhost:5000 in your browser.


## Dependencies

- Flask
- requests
- nltk
- youtube_transcript_api
- google-api-python-client
    
## Contributing

Feel free to contribute to the project by opening issues or submitting pull requests. Follow the CONTRIBUTING.md guidelines.

## License

This project is licensed under the MIT License.

## Acknowledgments

Acknowledge any third-party libraries, APIs, or services used in the project.
For more details, visit the GitHub repository.     





