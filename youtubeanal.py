import streamlit as st
from googleapiclient.discovery import build
from textblob import TextBlob

# YouTube APIを使用して、指定されたビデオのコメントを取得する関数
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

# メインのStreamlitアプリケーション
def main():
    # アプリケーションタイトル
    st.title("YouTubeコメント解析アプリ")

    # YouTube APIキーの入力
    api_key = st.text_input("YouTube APIキーを入力してください")

    # ビデオIDの入力
    video_id = st.text_input("URLを入力してください")[-11:]

    show_comments = st.checkbox('コメントを表示する')

    # コメントの取得と解析
    if st.button("コメントを解析"):
        try:
            # YouTube APIを使用してコメントを取得
            comments = get_video_comments(video_id, api_key)
            st.write(f"コメント数:{len(comments)}")
            scores = 0
            count = 0
            # 取得したコメントを解析
            st.write("解析結果：")
            for comment in comments:
                blob = TextBlob(comment)
                sentiment_score = blob.sentiment.polarity
                if sentiment_score != 0.0:
                    scores += sentiment_score
                    count += 1
                if show_comments:
                    st.markdown(f"{comment}: :blue[{sentiment_score}]")
            st.write("平均値:",scores/count)
        
        except Exception as e:
            st.write("エラー： " + str(e))

if __name__ == "__main__":
    main()
