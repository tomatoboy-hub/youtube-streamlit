
import streamlit as st
from googleapiclient.discovery import build
from textblob import TextBlob
from translate import Translator

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
    
    origin = st.radio("コメントの言語を選んでください",("日本語","英語"))
    if origin == "日本語":
        translator = Translator(from_lang = "ja", to_lang = "en")
    else:
        translator = Translator(from_lang = "en", to_lang = "ja")

    if_trans = st.checkbox('コメントを翻訳する')

    # コメントの取得と解析
    if st.button("コメントを解析"):
        try:
            # YouTube APIを使用してコメントを取得
            comments = get_video_comments(video_id, api_key)
            st.write(f"コメント数:{len(comments)}")
            scores = 0
            count = 0
            enflag = True #元言語が英語
            # 取得したコメントを解析
            st.write("解析結果：")
            if origin == "日本語":
                enflag = False
            for comment in comments:
                origin_comment = comment
                if enflag == False:
                    comment = translator.translate(comment)
                blob = TextBlob(comment)
                sentiment_score = blob.sentiment.polarity
                if sentiment_score != 0.0:
                    scores += sentiment_score
                    count += 1
                if show_comments:
                    st.markdown(f"{origin_comment}: :blue[{sentiment_score}]")
                    if if_trans:
                        translated = translator.translate(comment)
                        st.markdown(f"{translated}")
            st.write("平均値:",scores/count)
            st.write("1に近いほどポジティブ、-1に近いほどネガティブ")
        
        except Exception as e:
            st.write("エラー： " + str(e))

if __name__ == "__main__":
    main()
