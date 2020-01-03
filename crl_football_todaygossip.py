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

# 본문 내용과 링크를 가져오는 함수
def getGossipList(lis):
    p_list = lis.text
    link = lis.find("a").get("href")
    p_list0 = p_list.split('(')[0]
    p_list1 = p_list.split('(')[1].strip(')')
    p_list_json = {"Gossip": p_list0, "Press": p_list1, "Link": link}
    return p_list_json

url = "https://www.bbc.com/sport/football/gossip"
html = urllib.request.urlopen(url)

bs_obj = bs4.BeautifulSoup(html, "html.parser")

aticle_class = bs_obj.find("article", {"class":"component"})

headline = aticle_class.find("h1", {"class":"story-headline"}).text
row_headline = {"headline": headline}

# 밑 2줄의 코드는 select를 이용한 코드로 대체
#aticle_body_lists = aticle_class.find("div", {"class":"story-body"})
#p_lists = aticle_body_lists.findAll("p")

p_lists = aticle_class.select('div.story-body > p')

# 날짜
now = datetime.now().strftime("%Y-%m-%d")

print(now)
print("Today " + headline)

json_result_lists = [ getGossipList(lis) for lis in p_lists ]
json_lists = { headline: json_result_lists }
result_json = json.dumps(json_lists, ensure_ascii=False, indent="\t")

# JSON 파일로 저장
f = open("./json/" + now + "_TodayFootballGossip.json", 'w', encoding='utf-8')
f.write(result_json)
f.close()

# 콘솔 출력 확인용
for lis in p_lists:
    result_list = getGossipList(lis)
    Gossip_list = result_list['Gossip']
    print(Gossip_list)

# 타입검사
#print(type(json_lists))
#print(json_result_lists)