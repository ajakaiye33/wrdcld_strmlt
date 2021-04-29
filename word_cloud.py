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
import streamlite as st

# pd.set_option("display.max_rows",1000)


our_data = pd.read_json(
    'https://raw.githubusercontent.com/ajakaiye33/ngrnewscorpus/main/data/testy.jsonl', lines=True)


today = datetime.now()


def todays_headline(df, col):
    get_date = today.strftime("%m/%d/%Y")
    filter_today = df[col] == get_date
    filter_keyword = df.iloc[:, 0]
    show_keywords_today = filter_keyword[filter_today].unique()
    return show_keywords_today


todays_headline(our_data, 'published')

# current day published news


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


todayz = todays_keywords(our_data, 'scraped_date')


# all published news
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


all_time = alltime_keywords(our_data, 'scraped_date')

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


viz_word(todayz)
