from flask import Flask, render_template, request
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
app = Flask(__name__)

# Replace 'YOUR_API_KEY' with your actual YouTube Data API key
API_KEY = 'YOUR_API_KEY'

# Define the headers variable
headers = {"Authorization": "Bearer YOUR_HUGGING_FACE_KEY"}



# Initialize the sentiment analyzer
sid = SentimentIntensityAnalyzer()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search_query')
    
    # Call YouTube Data API to get video data
    videos = get_youtube_videos(search_query)

    return render_template('index.html', videos=videos)

def get_youtube_videos(query):
    base_url = 'https://www.googleapis.com/youtube/v3/search'
    
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': 10,
        'key': API_KEY,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    videos = []
    for item in data['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        thumbnail_url = item['snippet']['thumbnails']['medium']['url']

        videos.append({
            'video_id': video_id,
            'title': title,
            'thumbnail_url': thumbnail_url,
        })

    return videos
@app.route('/youtube_analytics/<video_id>')
def youtube_analytics(video_id):
    # Fetch video details using the YouTube Data API
    video_details = get_video_details(video_id)

    # Apply sentiment analysis on the comments
    for comment in video_details['top_comments']:
            sentiment = sid.polarity_scores(comment['textDisplay'])
            if sentiment['compound'] > 0.05:
                comment['sentiment'] = 'positive'
            elif sentiment['compound'] < -0.05:
                comment['sentiment'] = 'negative'
            else:
                comment['sentiment'] = 'neutral'
    # Summarize the transcript
    summarized_transcript = summarize_transcript(video_details['transcript'])

    # Add summarized transcript to video details
    video_details['summarized_transcript'] = summarized_transcript
    # Get the video context for the chatbot
    context_data=f"title:,{video_details['title']} , description: ,{video_details['description']} , transcript :,{video_details['transcript']}"
  

    return render_template('youtube_analytics.html', video_details=video_details, context_data=context_data)
def get_video_details( video_id):
    # Function to retrieve video details
    API_KEY = 'AIzaSyDsj4Uwp-6m6b3Lc5UpOXHojuM8aFhG7r4'
    def get_video_info(video_id):
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        video_response = youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=video_id
        ).execute()
        return video_response['items'][0] if 'items' in video_response else None

    # Function to extract transcript in English
    def get_transcript(video_id, language_code='en'):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id,languages=[language_code])
            full_transcript = ' '.join(entry['text'] for entry in transcript)
            
            return full_transcript.replace('[Music]', '')
        except Exception as e:
            print(f"Error getting transcript: {e}")
            return ""

    # Function to load top comments with most likes 
    def get_top_comments(video_id):
        try:
            comments_response = requests.get(
                f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={API_KEY}&order=relevance&maxResults=100"
            ).json()
            top_comments = []

            for item in comments_response.get('items', []):
                comment_data = item['snippet']['topLevelComment']['snippet']
                top_comments.append({
                    'author': comment_data['authorDisplayName'],
                    'textDisplay': comment_data['textDisplay'],
                    'likeCount': comment_data['likeCount']
                })

            return top_comments

        except HttpError as e:
            print(f"Error getting top comments: {e}")
            return []

    # Main function to get video details, transcript, and top comments
    try:
        video_info = get_video_info(video_id)
        if video_info:
            # Video details
            title = video_info['snippet']['title']
            thumbnail_url = video_info['snippet']['thumbnails']['default']['url']
            description = video_info['snippet']['description']
            likes = video_info['statistics']['likeCount']
            views = video_info['statistics']['viewCount']
            uploaded_date = video_info['snippet']['publishedAt']

            # Transcript
            transcript = get_transcript(video_id)
            print(transcript)

            # Top comments
            top_comments = get_top_comments(video_id)

            # Return a dictionary with all information
            result = {
                'video_id': video_id,
                'title': title,
                'thumbnail_url': thumbnail_url,
                'description': description,
                'likes': likes,
                'views': views,
                'uploaded_date': uploaded_date,
                'transcript': transcript,
                'top_comments': top_comments
            }

        else:
            result = {"error": "Video not found."}

    except HttpError as e:
        result = {"error": f"An error occurred: {e}"}


    
  
    return result

def query_api(model_url, payload):
    try:
        response = requests.post(model_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying model {model_url}: {str(e)}")
        return None

def summarize_with_models(input_text):
    model_urls = [
        "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
        "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6",
        "https://api-inference.huggingface.co/models/philschmid/bart-large-cnn-samsum",
    ]

    for model_url in model_urls:
        output = query_api(model_url, {"inputs": input_text})

        if output and 'summary_text' in output[0]:
            return output[0]['summary_text']

    return "Unable to generate summarization with any model."
def summarize_transcript(transcript):
    return summarize_with_models(transcript)

# Chatbot models
qa_models = [
    {"api_url": "https://api-inference.huggingface.co/models/distilbert-base-uncased-distilled-squad", "name": "DistilBERT"},
    {"api_url": "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2", "name": "RoBERTa"},
    {"api_url": "https://api-inference.huggingface.co/models/deepset/bert-large-uncased-whole-word-masking-squad2", "name": "BERT"},
]

def query_question_answering(payload):
    for model in qa_models:
        response = requests.post(model["api_url"], headers=headers, json=payload)
        try:
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            output = response.json()
            if 'answer' in output:
                return output['answer']
        except requests.exceptions.RequestException as e:
            print(f"Error querying model {model['name']}: {str(e)}")
    return "Unable to generate an answer with any model."

# Chatbot route
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    context = request.args.get('context')
    transcript_available = True if context else False

    if request.method == 'POST':
        user_question = request.form.get('user_question')
        if transcript_available:
            # Query the chatbot with the user's question
            answer = query_question_answering({"context": context, "question": user_question})
        else:
            answer = "Sorry, no transcript available."

        return render_template('chatbot.html', context=context, user_question=user_question, answer=answer)

    return render_template('chatbot.html', context=context, transcript_available=transcript_available)


if __name__ == '__main__':
    app.run(debug=True)
