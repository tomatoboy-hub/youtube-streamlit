import streamlit as st
from googleapiclient.discovery import build
from textblob import TextBlob
from translate import Translator
import matplotlib.pyplot as plt

def get_video_comments(video_id, api_key):
    comments = []
    youtube = build('youtube', 'v3', developerKey=api_key)
    results = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText"
    ).execute()

    while results:
        for item in results["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        if "nextPageToken" in results:
            token = results["nextPageToken"]
            results = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                pageToken=token
            ).execute()
        else:
            break

    return comments

def main():
    st.title("YouTube Comment Sentiment Analysis App")
    st.markdown("#### **Enter your details:**")
    api_key = st.text_input("YouTube API Key")
    video_id = st.text_input("YouTube Video URL")[-11:]

    origin = st.radio("Select the language of the comments",("English","Japanese"))

    if origin == "Japanese":
        translator = Translator(from_lang = "ja", to_lang = "en")
    else:
        translator = Translator(from_lang = "en", to_lang = "en")

    show_comments = st.checkbox('Show comments')
    translate_comments = st.checkbox('Translate comments')

    if st.button("Analyze Comments"):
        with st.spinner('Fetching and analyzing comments...'):
            try:
                comments = get_video_comments(video_id, api_key)
                scores = []
                positive, negative = 0, 0
                translated_comments = []
                for comment in comments:
                    translated_comment = translator.translate(comment)
                    blob = TextBlob(translated_comment)
                    sentiment_score = blob.sentiment.polarity
                    if sentiment_score != 0.0:
                        scores.append(sentiment_score)
                        if sentiment_score > 0:
                            positive += 1
                        else:
                            negative += 1
                    if show_comments:
                        if translate_comments:
                            st.markdown(f"{comment} (translated: {translated_comment}): Sentiment Score  {sentiment_score}")
                        else:
                            st.markdown(f"{comment}: Sentiment Score - {sentiment_score}")
                st.markdown("### Analysis Results")
                st.write("Average Sentiment Score: ", sum(scores) / len(scores))
                plt.pie([positive, negative], labels=["Positive", "Negative"], autopct='%1.1f%%', startangle=90)
                plt.axis('equal')
                st.pyplot(plt.gcf())
            except Exception as e:
                st.error("Error: " + str(e))

if __name__ == "__main__":
    main()
