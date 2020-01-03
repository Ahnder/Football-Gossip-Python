import requests
import urllib.request
import bs4
import json
from datetime import datetime

# USER_ID, USER_SECRET 가져오기
with open('secretConfig.json', 'r') as f:
    config = json.load(f)    
USER_ID = config['SECRET']['USER_ID']
USER_SECRET = config['SECRET']['USER_SECRET']

# 번역 함수(인공신경망 기반)
def get_nmt_translate(context):
    try:
        url = "https://openapi.naver.com/v1/papago/n2mt"
        headers= {"X-Naver-Client-Id": USER_ID, "X-Naver-Client-Secret": USER_SECRET}
        params = {"source": "en", "target": "ko", "text": context}
        response = requests.post(url, headers=headers, data=params)
        res = response.json()
        return res['message']['result']['translatedText']
    except:
        return "번역 실패"

# 번역 함수(통계기반)
def get_smt_translate(context):
    try:
        url = "https://openapi.naver.com/v1/language/translate"
        headers= {"X-Naver-Client-Id": USER_ID, "X-Naver-Client-Secret": USER_SECRET}
        params = {"source": "en", "target": "ko", "text": context}
        response = requests.post(url, headers=headers, data=params)
        res = response.json()
        return res['message']['result']['translatedText']
    except:
        return "번역 실패"        

# gossip 내용과 링크를 가져오는 함수 (함수 안에서 번역함수 사용)
def getGossipTranslateList(lis):
    p_list = lis.text
    link = lis.find("a").get("href")
    papagoList = get_nmt_translate(p_list)
    p_list_json = {"Gossip": papagoList, "srcText":p_list ,"link": link}
    return p_list_json

url = "https://www.bbc.com/sport/football/gossip"
html = urllib.request.urlopen(url)

bs_obj = bs4.BeautifulSoup(html, "html.parser")

# gossip본문 
aticle_class = bs_obj.find("article", {"class":"component"})

# today gossip 타이틀
headline = aticle_class.find("h1", {"class":"story-headline"}).text

p_lists = aticle_class.select('div.story-body > p')

# 날짜
now = datetime.now().strftime("%Y-%m-%d")

print(now)
print("Today " + headline)

json_result_lists = [getGossipTranslateList(lis) for lis in p_lists ]
json_lists = { headline: json_result_lists }
result_json = json.dumps(json_lists, ensure_ascii=False, indent="\t")    

# JSON 파일로 저장
f = open("./json/" + now + "_TodayFootballGossipTranslate.json", 'w', encoding='utf-8')
f.write(result_json)
f.close()
