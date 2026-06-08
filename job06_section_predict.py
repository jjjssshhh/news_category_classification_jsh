
import pickle
import pandas as pd
import numpy as np
from keras.utils import to_categorical
from konlpy.tag import Okt
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import re
#
from sklearn.preprocessing import LabelEncoder


df = pd.read_csv('./data/naver_headline_news_20260605')
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
print(df.head())
df.info()
print(df.category.value_counts())

X = df.titles
Y = df.category

# ==========================
# 기존 사용 코드 job4에서 encoder가 아니라 label로 저장해서 아래처럼 하는것임
# with open('./data/encoder.pkl', 'rb') as f:
#     encoder = pickle.load(f)
# ==========================

# 새로운데이터로 정확도 확인할 것임 그전에 전처리가 필요하다.
# 만약 새롭게 발견된 형태소가 있다면 0으로 처리된다.
# 토크나이저도 만들었던 대로

encoder = LabelEncoder()
labeled_y = encoder.fit_transform(Y)
print(labeled_y[:5])
label = encoder.classes_
print(label)
with open('./data/encoder.pkl', 'wb') as f:
    pickle.dump(encoder, f)  # int로 저장 형변환이 필요없다. 문자열아니면 pickle로 저장한다.
# ==========================
onehot_y = to_categorical(labeled_y)
print(onehot_y[:5])

okt = Okt()
X = list(X)
for i in range(len(X)):
    X[i] = re.sub('[^가-힣]', ' ', X[i])
    X[i] = okt.morphs(X[i])
print(X)

for idx,sentence in enumerate(X):
    words = []
    for word in sentence:
        if len(word) > 1:
            words.append(word)
    X[idx] = ' '.join(words)

print(X[:10])

# 토큰 가져오고
# wb사용해서 ran out 에러시 토큰파일이 비어있다는 것으로 job04의 토큰만들기까지만(exit()) 다시 돌려야 한다.
with open('./data/tokenizer_max26.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

tokend_x = tokenizer.texts_to_sequences(X)
print(tokend_x[:10])

# 길이맞추기
# 새로 가져온데이터길이는 18보다 클수 있다. 어쩔수 없이 잘라야 한다.

for i in range(len(tokend_x)):
    if len(tokend_x[i]) > 26:
        tokend_x[i] = tokend_x[i][:26] # 18까지만으로 자른다.

x_pad = pad_sequences(tokend_x, maxlen=26)
print(tokend_x[:10])

model = load_model('./models/news_section_classifier0.6604.h5')
score = model.evaluate(x = x_pad, y=onehot_y, verbose=0)
print('accuracy:', score[1]) # 39%...40%...
# 정화도 하락의 원인은?
# 없던 형태소가 많은 경우이다.
# 데이터가 많으면 많을수록 정확도가 상승한다.

# preds = model.predict(x_pad)
# print(preds)


# 무엇을 틀리는지 확인해보자
preds = model.predict(x_pad) # 오늘뉴스를 주고 예측했고
predict_section = []
# print(preds)
for pred in preds:
    most = label[np.argmax(pred)]
    pred[np.argmax(pred)] = 0
    second = label[np.argmax(pred)]
    predict_section.append([most,second])
    # predict_section.append(most)

df['predict'] = predict_section # 예측컬럼을 하나 더 만들었다.
print(df.head(30)) # 맞춘것과 틀린것모두 보자.

# Politics -> Social이 굉장히 많다.

df['OX'] = 0
for i in range(len(df)):
    if df.loc[i,'category'] in df.loc[i,'predict']:
        df.loc[i,'OX'] = 1 # 예측이라도 맞추면 정답처리

print(df.OX.mean())
# 62% 많이 올라간다!

