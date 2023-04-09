import streamlit as st
from googleapiclient.discovery import build
from textblob import TextBlob

# YouTube Data APIのキー
API_KEY = 'AIzaSyDJT2DjO4fG7h1re-WLtBbEEmLBCZPWGC4'

# YouTube Data APIを使って動画情報を取得する関数
def get_video_info(video_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    response = youtube.videos().list(
        part='snippet,statistics',
        id=video_id
    ).execute()
    return response['items'][0]

# 動画のコメントを取得して、感情分析を行う関数
def analyze_comments(video_id):
    youtube = build('youtube', 'v3', key=API_KEY)
    comments = []
    next_page_token = None
    while True:
        response = youtube.commentThread().list(
            part='snippet',
            videoId=video_id,
            pageToken=next_page_token
        ).execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        if 'nextPageToken' in response:
            next_page_token = response['nextPageToken']
        else:
            break
    sentiment_scores = []
    for comment in comments:
        blob = TextBlob(comment)
        sentiment_scores.append(blob.sentiment.polarity)
    return sentiment_scores

# Streamlitアプリの定義
def main():
    st.title('YouTube Comment Analysis')
    video_id = st.text_input('Enter YouTube Video ID:')
    if video_id:
        try:
            video_info = get_video_info(video_id)
            st.write('Title:', video_info['snippet']['title'])
            st.write('Channel:', video_info['snippet']['channelTitle'])
            st.write('Views:', video_info['statistics']['viewCount'])
            st.write('Likes:', video_info['statistics']['likeCount'])
            st.write('Dislikes:', video_info['statistics']['dislikeCount'])
            sentiment_scores = analyze_comments(video_id)
            st.write('Sentiment Scores:', sentiment_scores)
            st.write('Average Sentiment Score:', sum(sentiment_scores)/len(sentiment_scores))
        except:
            st.write('Invalid Video ID')

if __name__ == '__main__':
    main()
