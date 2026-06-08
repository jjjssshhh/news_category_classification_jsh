import pandas as pd
# df = pd.read_csv('./data/naver_news_section.csv')
# print(df.head())
#
# # df_temp = pd.read_csv('./data/naver_news_section_p.csv')
# # df = pd.concat([df, df_temp])
#
# df_temp = pd.read_csv('./data/naver_headline_news_Culture_20260604.csv')
# df = pd.concat([df, df_temp])
#
#
# df_temp = pd.read_csv('./data/naver_news_section_social.csv')
# df = pd.concat([df, df_temp])
#
# df_temp = pd.read_csv('./data/naver_news_world_20260604.csv')
# df = pd.concat([df, df_temp])
#
# df_temp = pd.read_csv('./data/naver_news_IT_Science_20260604.csv')
# df = pd.concat([df, df_temp]) # 붙이기

# 6.8추가
df = pd.read_csv('./naver_headline_news_Culture_20260608.csv')
# df = pd.concat([df, df_temp])
df_temp = pd.read_csv('./naver_headline_news_Economics_20260608.csv')
df = pd.concat([df, df_temp])
df_temp = pd.read_csv('./naver_headline_news_IT_20260608.csv')
df = pd.concat([df, df_temp])
df_temp = pd.read_csv('./naver_headline_news_Politics_20260608.csv')
df = pd.concat([df, df_temp])
df_temp = pd.read_csv('./naver_headline_news_Society_20260608.csv')
df = pd.concat([df, df_temp])
df_temp = pd.read_csv('./naver_headline_news_World_20260608.csv')
df = pd.concat([df, df_temp])

# print(df.category.value_counts())
# print(df.isnull().sum())

df = df.drop_duplicates() # 중복제거

print(df.category.value_counts())
print(df.isnull().sum())
# null값 생김
df.info()

df.to_csv('./data/news_titles.csv', index=False)

# 분류는 했는데
# 문장부호 제거, 형태소로 쪼개야 한다.
# 불용어 제거
