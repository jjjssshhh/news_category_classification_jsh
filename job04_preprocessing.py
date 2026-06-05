
# 자연어 전처리

import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt, Komoran
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import re


df = pd.read_csv('./data/news_titles.csv')
df.info()
print(df.head())
print(df.category.value_counts())

X = df.titles
Y = df.category
# ===================================
# print(X[0])
#
# okt = Okt() # okt가 형태소분리하는 패키지인데 자바로 되어있다. 이녀석이 실행되려면 자바 버추얼머신이 동작해야 한다.
# # sudo apt install -y openjdk-17-jdk # 설치
#
# okt_x = okt.morphs(X[0])
# print(okt_x)
#
# komoran = Komoran()
# komoran_x = komoran.morphs(X[0])
# print(komoran_x)
# # okt와 komoran은 서로 좀 다르다.
# # nlpy는 영어를 잘라준다.
# ===================================

encoder = LabelEncoder()
labeled_y = encoder.fit_transform(Y)
print(labeled_y[:5])
label = encoder.classes_
print(label)
with open('./data/encoder.pkl','wb') as f:
    pickle.dump(label, f) # int로 저장 형변환이 필요없다. 문자열아니면 pickle로 저장한다.

onehot_y = to_categorical(labeled_y)
print(onehot_y[:5])

