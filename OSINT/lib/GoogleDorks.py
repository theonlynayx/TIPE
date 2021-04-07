from bs4 import BeautifulSoup as bs
import requests
import threading
from OSINT.lib.colors import *
from OSINT.lib.utils import *
from OSINT.config import *
import json
import sys
import re

def GetPostOwner(shortcode,username):

    req = requests.get(f"https://www.instagram.com/p/{shortcode}/",headers=headers,cookies=cookies)
    if req.status_code == 404:
         fail("[!] Error while dorking...")
    PostSoup = bs(req.text, 'html.parser')
    PostSoup.encode('utf-8')
    if "Login • Instagram" in str(PostSoup.find('title')):
        fail("[!] Error: Filouteries have been detected, try later or use a proxy!")
    post = PostSoup.find_all('script', attrs={'type': 'text/javascript'})
    if cookies:
        Infos = json.loads(post[14].get_text()[str(post[14].get_text()).find("{\"graphql"):].strip(');'))
        owner = Infos['graphql']['shortcode_media']['owner']
    else:
        Infos = json.loads(post[3].get_text()[str(post[3].get_text()).find("{\"config"):].strip(';'))
        owner = Infos['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']
    return owner['username']

def DorkRequest(username,dork,UrlList):
    request_result=requests.get( dork.format(username),headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.63','referer':'https://google.com/',"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp"}) 
    soup = bs(request_result.text,"html.parser")
    result = soup.find_all('div',attrs = {'class': 'yuRUbf'})
    for i in result:
        try:
            finding = re.search('https://(.*)',str(i.find('a',href = True)['href']))
            UrlList.append(finding.group(1))
        except:
            pass    

def UseGoogleDorks(username,ret):

    RespAllUrl = []
    RespAllText = []
    RespInstaText = []
    AccountList = []
    PostList = []
    
    Tlist = [
        threading.Thread(target=DorkRequest,args=(username,DorkList['GlobalUrl'],RespAllUrl)),
        threading.Thread(target=DorkRequest,args=(username,DorkList['GlobalText'],RespAllText)),
        threading.Thread(target=DorkRequest,args=(username,DorkList['InstaText'],RespInstaText)),
        ]

    Devent = threading.Event()
    Dload = threading.Thread(target=loading,args=(Devent,))
    Dload.start()

    [t.start() for t in Tlist]
    [t.join() for t in Tlist]

    # 𝑹𝒆𝒈𝒊𝒔𝒕𝒆𝒓𝒊𝒏𝒈 𝒕𝒉𝒆 𝒇𝒊𝒓𝒔𝒕 𝒅𝒐𝒓𝒌 : 𝑰𝒏𝒔𝒕𝒂𝑻𝒆𝒙𝒕

    for i in RespInstaText:
        if username in i or 'instagram.com' not in i:
            continue
        elif "/p/" in i:
            UrlContent = re.search('/p/(.*)',i)
            shortcode = (UrlContent.group(1) + '/')[:UrlContent.group(1).find('/')]
            PostOwner = GetPostOwner(shortcode,username)
            if PostOwner and PostOwner != username:
                PostList.append((shortcode,PostOwner))
        else:
            UrlContent = re.search('www.instagram.com/(.*)/',i)
            AccountList.append(UrlContent.group(1))

    Devent.set()

    if PostList:
        for j in list(dict.fromkeys(PostList)):
            ret['Dorks']['InstaText'].append("{} ~ {}".format(j[0],j[1]))
            
    if AccountList:
        for i in list(dict.fromkeys(AccountList)):
            ret['Dorks']['AccountList'].append(i)

    # 𝑹𝒆𝒈𝒊𝒔𝒕𝒆𝒓𝒊𝒏𝒈 𝒕𝒉𝒆 𝒔𝒆𝒄𝒐𝒏𝒅 𝒅𝒐𝒓𝒌 : 𝑮𝒍𝒐𝒃𝒂𝒍𝑼𝒓𝒍

    for i in list(RespAllUrl):
        if 'www.instagram.com' in i:
            RespAllUrl.remove(i)

    if RespAllUrl:
        for j in RespAllUrl:
            ret['Dorks']['RespAllUrl'].append(j)
    
    # 𝑹𝒆𝒈𝒊𝒔𝒕𝒆𝒓𝒊𝒏𝒈 𝒕𝒉𝒆 𝒕𝒉𝒊𝒓𝒅 𝒅𝒐𝒓𝒌 : 𝑮𝒍𝒐𝒃𝒂𝒍𝑻𝒆𝒙𝒕
    
    for i in list(RespAllText):
        if 'www.instagram.com' in i:
            RespAllText.remove(i)
            
    if RespAllText:
        for j in RespAllText:
            ret['Dorks']['RespAllText'].append(j)
