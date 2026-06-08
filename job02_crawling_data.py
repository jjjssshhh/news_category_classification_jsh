# # 파일명은 naver_news_section.csv로 해주세요.
# # 컬럼명은 titles, category로 해주세요.
# # 00님이 정치, 경제
# # 01님이 사회, 문화
# # 02님이 세계, IT
# # 다 되면 PR부탁합니다.(Pull request)
#
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import pandas as pd
# import datetime
# import requests
# from bs4 import BeautifulSoup
#
# options = ChromeOptions()
# options.add_argument('lang=ko_KR')
# options.add_argument('headless') # 새창이 띄워지는 것을 안보고 싶으면 이 코드를 살리면 된다.
#
# service = ChromeService(executable_path=ChromeDriverManager().install()) # 크롬 드라이버 설치
# driver = webdriver.Chrome(service=service, options=options) # 서비스로 만들고
#
# # url = 'https://news.naver.com/section/100'
# # driver.get(url)
# # # 해당 url로 브라우저가 뜬다.
# # # 그냥 두면 창이 닫힌다. 그래서 딜레이가 필요하다.
# # time.sleep(5)
#
# # 더보기 누르고 읽기하면 된다.
#
# # 더보기 버튼을 어떻게 누를까?
# # 버튼의 xpath를 가져온다. html상의 위치정보이다.
# url = 'https://news.naver.com/section/100'
# driver.get(url)
# button_path = '//*[@id="newsct"]/div[4]/div/div[2]/a'
#
# for i in range(6):
#     driver.find_element(By.XPATH, button_path).click() # click으로 누름
#     # 버튼이 새로 생길 때까지 딜레이가 필요함
#     time.sleep(0.5)
#
# # time.sleep(5) # 아래 코드 까지 실행시 주석
#
# # 다른 위치를 볼 것
# # '//*[@id="newsct"]/div[4]/div/div[1]/div[27]/ul/li[4]/div/div/div[2]/a/strong'
# # '//*[@id="newsct"]/div[4]/div/div[1]/div[27]/ul/li[6]/div/div/div[2]/a/strong'
# # '//*[@id="newsct"]/div[4]/div/div[1]/div[31]/ul/li[3]/div/div/div[2]/a/strong'
# # div[]/ul/li[] 규칙인듯
#
# # 5 37
# # 6 43.
# # 대충 위에 *7 + 5정도
#
# for i in range(1,51): # 40까지
#     for j in range(1,7):
#         try:
#             title_xpath = '//*[@id="newsct"]/div[4]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(i,j)
#             title = driver.find_element(By.XPATH, title_xpath).text
#             print(title)
#         except:
#             print('error',i,j) # 3이 없다.
#
#
# category = ['Politics','Economic','Social','Culture','World','IT']
# df_titles = pd.DataFrame()
#
# for i in range(0,len(category)):
#     url = 'https://news.naver.com/section/10{}'.format(i)
#
#
#     # resp = requests.get(url)
#     # print(list(resp))
#
#     soop = BeautifulSoup(resp.dri, 'html.parser')
#     # print(soop) # html파일 그대로 쭉 나옴
#
#     soop.select('.sa_text_strong')
#     title_tag = soop.select('.sa_text_strong')
#     # print(title_tag)
#     # print(title_tag[0].text) # 뉴스의 헤드기사 가져왔음
#
#     titles = []
#     for title in title_tag:
#         titles.append(title.text)
#     print(titles)
#
#     df_section_titles = pd.DataFrame(titles, columns=['titles'])
#     df_section_titles['category'] = category[i] # i번째 카테고리 이름 가져오기
#     df_titles = pd.concat([df_titles,df_section_titles], ignore_index=True) # IT, Economy등이 들어간다.
#
# print(df_titles)
# df_titles.info()
# # 저장
# df_titles.to_csv('./data/naver_headline_news_{}'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)


import datetime
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# ------------------------------------------------------------------
# [기본 설정 정의] 정답 코드의 변수 구조 적용
# ------------------------------------------------------------------
category = ['Politics', 'Economics', 'Society', 'Culture', 'World', 'IT']
category_sel = 5  # 1 = Economics (101 섹션)
category_sel_cop = 1 if category_sel == 1 else 0 # 기본 0 Economics 1

print(category_sel_cop)

options = ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument('headless')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 최종 데이터를 결합할 데이터프레임 초기화
df_titles = pd.DataFrame()

# ------------------------------------------------------------------
# [1] Selenium 파트 (정답 코드처럼 데이터 수집)
# ------------------------------------------------------------------
url = 'https://news.naver.com/section/10{}'.format(category_sel)
driver.get(url)
button_path = '//*[@id="newsct"]/div[{}]/div/div[2]/a'.format(category_sel_cop+4)

# 더보기 버튼 30번 클릭
for i in range(31):
    try:
        driver.find_element(By.XPATH, button_path).click()
        time.sleep(0.5)
    except:
        break

titles_sel = []
for i in range(1, 221):
    for j in range(1, 7):
        try:
            title_xpath = '//*[@id="newsct"]/div[{}]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(category_sel_cop+4,i, j)
            # Selenium의 .text는 눈에 보이는 글자만 가져오므로 줄바꿈이 생기지 않습니다.
            title = driver.find_element(By.XPATH, title_xpath).text
            if title.strip():
                titles_sel.append(title.strip())
        except:
            pass

driver.quit()

# 정답 코드와 똑같이 컬럼명을 'title'로 매핑하여 병합
df_selenium = pd.DataFrame(titles_sel, columns=['titles'])
df_selenium['category'] = category[category_sel]
df_titles = pd.concat([df_titles, df_selenium], ignore_index=True)


# ------------------------------------------------------------------
# [2] BeautifulSoup 파트 (줄바꿈 공백 리스크 제거)
# ------------------------------------------------------------------
url = 'https://news.naver.com/section/10{}'.format(category_sel)
resp = requests.get(url)
soop = BeautifulSoup(resp.text, 'html.parser')
title_tag = soop.select('.sa_text_strong')

titles_bs4 = []
for title in title_tag:
    # 텍스트 추출 시 .strip()을 확실히 붙여 원본 글자는 유지하되 앞뒤 공백과 개행문자만 제거합니다.
    clean_title = title.text.strip()
    if clean_title:
        titles_bs4.append(clean_title)

# 정답 코드와 똑같이 컬럼명을 'titles'로 일치시켜 병합
df_section_titles = pd.DataFrame(titles_bs4, columns=['titles'])
df_section_titles['category'] = category[category_sel]
df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)


# ------------------------------------------------------------------
# [3] 출력 및 저장 파트 (불필요한 글자 치환 코드 모두 제거)
# ------------------------------------------------------------------
print(df_titles.head())
df_titles.info()

# 정답 코드의 파일 저장 방식 그대로 적용 (날짜 포함 포맷) # 포맷이 있어야 표로 정리됨
# 단, 한글 깨짐으로 인해 표 뷰어가 오작동하는 것을 막기 위해 encoding='utf-8-sig'만 유지했습니다.
file_name = './naver_headline_news_{}_{}.csv'.format(
    category[category_sel], datetime.datetime.now().strftime('%Y%m%d')
)
# file_name = './naver_headline_news_{}.csv'.format(category_sel)

df_titles.to_csv(file_name, index=False, encoding='utf-8-sig')

print(f"CSV 저장 완료! '{file_name}' 파일이 정답 코드처럼 깔끔한 표 형태로 열립니다.")

