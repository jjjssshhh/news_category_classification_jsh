

import numpy as np
import matplotlib.pyplot as plt
from keras.models import *
from keras.layers import *

x_train = np.load('./data/x_train_wordsize9718.npy',allow_pickle=True)
y_train = np.load('./data/y_train_wordsize9718.npy',allow_pickle=True)
x_test = np.load('./data/x_test_wordsize9718.npy',allow_pickle=True)
y_test = np.load('./data/y_test_wordsize9718.npy',allow_pickle=True)
print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

# 의미 학습
# 형태소 갯수차원의 의미학습이다.
#      지위
# 아빠       여자
# 모든 형태소를 의미연산좌표계에 놓으면
# 여자벡터 여왕벡터, 아빠, 왕이 있다.
# 여왕 - 여자 + 아빠 = 왕인 공간이 의미 공간이다.

# 문장안에 들어간 형태소 벡터의 총합이 가리키는 곳에 정답이 있다.
# 또는
# 오늘 저녁은 치킨이다. 오늘 저녁은 피자이다.
# 라는 단어가 있다면 같은 벡터에 다른 단어들은 '비슷한'의미를 가지므로 비슷한 값의 벡터를 가진다.

# 형태소중 여자 차원에서 각각의 형태소에 의미좌표를 부여할 수 있다.(연관성....)
# 아바좌표에서 모든 형태소에 의미좌표, 엄마 좌표에서 모든 형태소의 의미좌표....로 의미공간상에 벡터화를 하면
# 연산이 된다.

model = Sequential()
model.add(Embedding(9718,300)) # wordsize 차원을 만든다.
model.build(input_shape=(None,26)) # max값 문장길이
model.summary()
model.add(Conv1D(32,5,padding='same',activation='relu')) # 1차원? 입력데이터가 배열형태라서 그런듯
# Conv2D를 1D로 이미지를 처리하면 2차원 이미지의 위치관계를 학습할수 없게 된다.
# 문장은 1차원 순서가 중요하다.
model.add(MaxPooling1D(1))
model.add(LSTM(128,activation='tanh', return_sequences=True))
# Long Short-Term Memory
# 장기기억, 단기기억 RNN의 특수한 한종류이다.
# 전달되는 기억이 2개있다.
# Short Term ; 입력이 다단계로 들어가면서 한 단계마다 0.x가 곱해져서 결과가 도출된다.
# 따라서 마지막으로 들어간 데이터가 가장 크게 보이게 되는 효과를 가진다.
# Long Term : 장기 기억용으로 첫데이터도 끝까지 결과에 영향을 줄수 있다.
# 시계열 데이터에서 주효하다.(과거를 기록하는 데이터)

# tanh 하이퍼볼릭 탄젠트 시그모이드와 유사하게 생겼다.
# 핵심은 음수가 있다는것이다. -1 ~ 1까지
# relu는 0 ~ 1

model.add(Dropout(0.2))
model.add(LSTM(64,activation='tanh', return_sequences=True))
# return sequence
# LSTM이 2단인 경우 1단의 최종결과에서 2단으로 들어가면 안되므로
# 1단의 순환마다 값을 매번 저장한다. n단만큼 저장하고 이걸 2단 LSTM에 전달
# 이걸 허용시키는 것이 return sequence=true
# false이면 결과하나만 출력된다.
model.add(Dropout(0.2))
model.add(LSTM(64,activation='tanh', return_sequences=True))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(64,activation='relu'))
model.add(Dense(6,activation='softmax'))
model.summary()

# RNN
# 되먹임이 있는 구조
# 오늘 저녁은 햄버거이다.
#        오늘      -> cell -> res1
# res1 + 저녁은     -> cell -> res2
# res2 + 햄버거이다. -> cell -> result

# CNN은 2차원 위치관계가 있을때 사용
# Dense 조밀한 구조
# RNN 순서가 있는 시계열데이터에 잘 동작함 LSTM

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
fit_hist = model.fit(x_train,y_train,batch_size=128,epochs=10,validation_data=(x_test, y_test), verbose=1)
score = model.evaluate(x_test,y_test,verbose=0)
print('Test loss:',score[0])
print('Test accuracy:',score[1])

model.save('./models/news_section_classifier{:.4f}.h5'.format(score[1]))
plt.plot(fit_hist.history['val_accuracy'], label='val_accuracy')
plt.plot(fit_hist.history['accuracy'], label='train accuracy')
plt.legend(loc='lower right')
plt.show()

