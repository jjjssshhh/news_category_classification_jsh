
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
# okt_x_stem = okt.morphs(X[0], stem=True)
# print(okt_x_stem) # 기댈 -> 기대다. 문자를 배울께 많으니까 원형으로 바꾸는것이다. stem = True
# exit()
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
    pickle.dump(encoder, f) # int로 저장 형변환이 필요없다. 문자열아니면 pickle로 저장한다.

onehot_y = to_categorical(labeled_y)
print(onehot_y[:5])

# 한자, 영어 버린다.

# cleaned_x = re.sub('[^가-힣]',' ', X[0]) # 한글을 제외하고 ' '으로 sub(빼기)하기
# print(X[0])
# print(cleaned_x)
okt = Okt()

X = list(X)

for i in range(len(X)): # len(X), 100
    X[i] = re.sub('[^가-힣]', ' ', X[i]) # 변환
    X[i] = okt.morphs(X[i], stem=True) # 원형 변환
    if i % 1000 == 0:
        print(i)

print(X[:5])

for idx, sentence in enumerate(X): #X[:5]
    words = []
    for word in sentence:
        if len(word) > 1:
            words.append(word) # 2글자 이상이어야만 추가 한글자는 삭제
    X[idx] = ' '.join(words) # 한 문장으로 연결

print(X[:5])

# 숫자로 바꿔줘야 한다.
# tokenizer
# ===============================
# tokenizer = Tokenizer()
# tokenizer.fit_on_texts(X)
# tokened_x = tokenizer.texts_to_sequences(X[:5])
# print(tokened_x[:5])
# exit()
# ===============================
# 숫자화 tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)
tokened_x = tokenizer.texts_to_sequences(X)
print(tokened_x)
wordsize = len(tokenizer.word_counts) + 1
print('wordsize',wordsize) # 형태소의 갯수

max = 0
for sentence in tokened_x:
    if max < len(sentence):
        max = len(sentence)
print('max',max)

with open('./data/tokenizer_max{}.pkl'.format(max),'wb') as f:
    pickle.dump(tokenizer, f)

x_pad = pad_sequences(tokened_x, maxlen=max) # 패딩!!!
print(x_pad[:5]) # 앞에 0이 붙여진것을 알 수 있다.


x_train, x_test, y_train, y_test = train_test_split(x_pad, onehot_y, test_size=0.1)
print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)

np.save('./data/x_train_wordsize{}.npy'.format(wordsize), x_train)
np.save('./data/y_train_wordsize{}.npy'.format(wordsize), y_train)
np.save('./data/x_test_wordsize{}.npy'.format(wordsize), x_test)
np.save('./data/y_test_wordsize{}.npy'.format(wordsize), y_test)


# 입력 사이즈가 일정해야 한다. 현재는 문장의 길이가 다르다.
# 가장 큰 형태소길이만큼 작은 녀석에 앞에 0을 채운다.(zero-padding) LSTM




