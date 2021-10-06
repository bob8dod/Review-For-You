import numpy as np
import pandas as pd
import matplotlib.font_manager as fm
from PIL import Image
from wordcloud import WordCloud
import random
from random import randint
from datetime import date, timedelta
import matplotlib.pyplot as plt
font = fm.FontProperties(fname='./210Black.ttf')
mask = Image.open('./cloud.png')
mask = np.array(mask)

def make_charts(data):
    prev_year = date.today()- timedelta(days=90)
    time_x =[prev_year + timedelta(days = i) for i in range(90)]
    n, a = 10, []
    for _ in range(90):
        a.append(max(0,n + randint(-10,10)))
        n = a[-1]

    fig, ax = plt.subplots(figsize=(15,8),facecolor="black")
    ax.patch.set_facecolor('black')
    plt.plot(time_x,a, lw =3, color = 'white')
    plt.tick_params(axis='x', colors='#F5E9F5',labelsize=15)
    plt.tick_params(axis='y', colors='#F5E9F5',labelsize=15) 
    plt.xlabel("", color = 'white', fontsize=20)
    ax.grid(True,alpha=0.4)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    plt.savefig("./static/image/line_chart.png")

    fig, ax = plt.subplots(figsize=(15,8),facecolor="black")
    ax.patch.set_facecolor('black')
    fig.patch.set_alpha(0.2)
    bar_data = sorted(data.items(), key= lambda x : x[1],reverse=True)
    if len(bar_data) >=15:
        bar_data = bar_data[:15]
    plt.bar(x=[*map(lambda x : x[0], bar_data)], height=[*map(lambda x : x[1], bar_data)],alpha=0.7, color = 'white')
    plt.xticks(font=font,fontsize=20,color ="white",rotation =30)
    plt.yticks(font=font,fontsize=20,color ="white")
    plt.tick_params(axis='x', colors='#F5E9F5',labelsize=15)
    plt.savefig("./static/image/bar_chart.png")


    wc = WordCloud(font_path = '210Black.ttf',width=1000, height=600,
                background_color="#000000", random_state=0,mask = mask)
    plt.figure(figsize=(20,10),facecolor='#000000')
    plt.imshow(wc.generate_from_frequencies(data))
    wc.to_file('./static/image/wordcloud.jpg')