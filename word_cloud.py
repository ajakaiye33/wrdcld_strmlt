#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
from wordcloud import WordCloud, ImageColorGenerator
from PIL.Image import core as _imaging
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image
import random
import streamlit as st

# pd.set_option("display.max_rows",1000)


st.title("News Headlines and Keyword Visualization")


@st.cache
def load_data():
    our_data = pd.read_json(
        'https://raw.githubusercontent.com/ajakaiye33/ngrnewscorpus/main/data/testy.jsonl', lines=True)
    return our_data


# load_data_state = st.text("Loading data ...")
data = load_data()


today = datetime.now()


def todays_headline(df, col):
    get_date = today.strftime("%m/%d/%Y")
    filter_today = df[col] == get_date
    filter_keyword = df.iloc[:, 0]
    show_keywords_today = filter_keyword[filter_today].unique()
    return show_keywords_today


# load_healine = st.text("Loading News Headlines ...")


current_headline = todays_headline(data, 'scraped_date')


st.sidebar.title("Current News Healines Across the Country")
if st.sidebar.checkbox("Show todays Headline News"):

    st.subheader("Headlines ... loaded")
    st.write(current_headline)


# filter current keywords

def todays_keywords(df, col):
    all_keyword_today = []
    get_date = today.strftime("%m/%d/%Y")
    filter_today = df[col] == get_date
    filter_keyword = df.iloc[:, -1]
    show_keywords_today = filter_keyword[filter_today]
    for news in show_keywords_today:
        for key_words in news:
            all_keyword_today.append(key_words)
    today_text = ",".join(all_keyword_today)
    return today_text


todayz = todays_keywords(data, 'scraped_date')


# filter all published news
def alltime_keywords(df, col):
    all_keyword_alltime = []
    get_date = today.strftime("%m/%d/%Y")
    filter_today = df[col] != get_date
    filter_keyword = df.iloc[:, -1]
    show_keywords_today = filter_keyword[filter_today]
    for news in show_keywords_today:
        for key_words in news:
            all_keyword_alltime.append(key_words)
    full_text = ",".join(all_keyword_alltime)
    return full_text


all_time = alltime_keywords(data, 'scraped_date')

st.set_option('deprecation.showPyplotGlobalUse', False)

# visualize the keyword via word cloud


def viz_word(period):
    png = ['./img/nig-flag.png', './img/map-nig2.png']
    path_png = random.choices(png, k=1)[0]
    background = np.array(Image.open(path_png))
    wrdcld = WordCloud(width=50, height=50, background_color='white',
                       mode='RGBA', mask=background).generate(period)
    image_col = ImageColorGenerator(background)
    plt.figure(figsize=[20, 20])
    plt.imshow(wrdcld.recolor(color_func=image_col), interpolation='bilinear')
    plt.axis("off")
    return plt.show()


today_keys = viz_word(todayz)

all_keys = viz_word(all_time)


st.sidebar.title("Visualized Keywords in the News")

if st.sidebar.checkbox("Show wordcloud for current News"):
    st.subheader("Word cloud of current news")
    st.pyplot(today_keys)


st.sidebar.title("Visualized All time Keywords")
if st.sidebar.checkbox("Show word cloud for all time News"):
    st.subheader("Word cloud of all time News")
    st.pyplot(all_keys)
