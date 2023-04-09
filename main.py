# app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA

# YahooニュースのRSSフィードから記事のURLを取得する関数
def get_news_links_rss(feed_url):
    response = requests.get(feed_url)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.findAll('item')
    links = []
    for item in items:
        link = item.find('link').text
        links.append(link)
    return links

# 記事の本文を取得する関数
def get_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = []
    for p in soup.find_all('p'):
        text.append(p.text)
    return ' '.join(text)

# Streamlitアプリケーションのレイアウト
def app():
    st.title('Yahooニュースの記事トピック分析アプリ')

    # ユーザーが選択したトピックを入力として受け取る
    topic = st.text_input('トピックを入力してください（例：ビジネス、エンタメ、スポーツ）')

    # ユーザーがトピックを入力した場合に記事を収集し、LDAによるトピック分析を実行する
    if topic:
        # YahooニュースのRSSフィードから記事のURLを取得する
        rss_url = f"https://news.yahoo.co.jp/rss/{topic.lower()}-tpc.xml"
        news_links = get_news_links_rss(rss_url)

        # 各記事の本文を取得する
        texts = []
        for link in news_links:
            text = get_article_text(link)
            texts.append(text)

        # 取得した記事の本文をCountVectorizerにかけ、単語の出現頻度をベクトル化する
        vectorizer = CountVectorizer(stop_words='english')
        X = vectorizer.fit_transform(texts)

        # LDAによるトピック分析を実行する
        lda = LDA(n_components=3, random_state=42)
        lda.fit(X)

        # テキストデータをトピック分布のベクトルに変換する
        topic_distributions = lda.transform(X)

        # トピック分布の平均値を計算する
        topic_means = np.mean(topic_distributions, axis=0)

        # トピック分布の平均値をグラフで表示する
        fig, ax = plt.subplots()
        ax.bar(np.arange(len(topic_means)), topic_means)
        ax.set_xticks(np.arange(len(topic_means)))
        ax.set_xticklabels([f"Topic {i+1}" for i in range(len(topic_means))])
        ax.set_ylabel('Topic distribution')
        st.pyplot(fig)

        # トピックごとに記事のタイトルを表示する
        st.subheader('トピックごとの記事のタイトル')
        for i in range(len(topic_means)):
            st.write(f"Topic {i+1}")
            top_n = 5 # 各トピックから表示する記事の数
            top_indices = topic_distributions[:, i].argsort()[::-1][:top_n]
            for j in top_indices:
                st.write(news_links[j])
    else:
        st.write('トピックを入力してください')

if __name__ == '__main__':
   app()
