from urllib.request import getproxies
from bs4 import BeautifulSoup as bs
from collections import Counter
from OSINT.lib.colors import *
from OSINT.lib.GoogleDorks import *
from random import choice
from OSINT.lib.utils import *
from time import sleep
import datetime as dt
from OSINT.config import *
import itertools
import requests
import signal
import json
import sys
import os
import re

def GetStories(username,user_id):
    
    # π­πππ πΌπππ π¨ππππ ππ πππππ πππππππ πππ ππππ-πππππ πππππ

    UnofficialHeaders = {"user-agent" : "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)"}

    r = requests.get('https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={}'.format(user_id),cookies=cookies,headers=UnofficialHeaders)
    data = r.json()
    if data['reels']:
        try:
            for i,val in enumerate(data['reels'][user_id]['items']):
                if "video_versions" in val:
                    FileExtension = ".mp4"
                    url = val['video_versions'][0]['url']
                else:
                    FileExtension = ".jpg"
                    url = val['image_versions2']['candidates'][0]['url']
                with open("Stories_{}_{}_{}".format(username,i,FileExtension),"wb") as f:
                    story = requests.get(url)
                    f.write(story.content)
                f.close()
            ret['Story'] = "Stories_{}.*".format(username)
        except:
            fail('[x] Error while downloading story...')
    else:
        ret['Story'] = "No_Story_Available"

def AnalyzePosts(username,NofPostAvailable,InfosPosts,NofPostToAnalyze,NofPostToDownload,OptCom):
    
    global PostResult,TaggedUsersInPics
    PostResult,TaggedUsersInPics = [],[]
    index = 0
    ret['Posts'] = []

    if int(NofPostAvailable.replace(",","")) >= NofPostToAnalyze:
        LimIndex = NofPostToAnalyze
    else:
        LimIndex = int(NofPostAvailable.replace(",",""))

    # π³πππ πππππππππ πππππππ πππ ππππ πππππ

    while index < LimIndex:
        ret['Posts'].append({})
        Details = OptCom
        IsCaptionAvailable = True

        ret['Posts'][index]['timestamp'] = InfosPosts[index]['node']['taken_at_timestamp']
        ret['Posts'][index]['LikesNumber']= int(str(InfosPosts[index]['node']['edge_liked_by']['count']).replace(",",""))

        if InfosPosts[index]['node']['location'] != None:
            ret['Posts'][index]['Location'] = InfosPosts[index]['node']['location']['name']

        if InfosPosts[index]['node']['comments_disabled'] is True or InfosPosts[index]['node']['edge_media_to_comment']['count'] == 0 :
            ret['Posts'][index]['CommentsNumber'] = False
            Details = False
        else:
            ret['Posts'][index]['CommentsNumber'] = int(str(InfosPosts[index]['node']['edge_media_to_comment']['count']).replace(",",""))

        # π«ππππππππππ πππππ

        if NofPostToDownload > 0:
            if 'edge_sidecar_to_children' in InfosPosts[index]['node']:
                for i,j in enumerate(InfosPosts[index]['node']['edge_sidecar_to_children']['edges']):
                    if j['node']['is_video'] is True:
                        GetPicsAndVid(j['node']['video_url'],"Post{}_{}_{}.mp4".format(username,index + 1,i + 1))
                        ret['Posts'][index]['VidMultiParts'] = "Post{}_{}_X.mp4".format(username,index + 1)
                    else:
                        GetPicsAndVid(j['node']['display_url'],"Post{}_{}_{}.jpg".format(username,index + 1,i + 1))
                        ret['Posts'][index]['PicMultiParts'] = "Post{}_{}_X.jpg".format(username,index + 1)
            else:
                if InfosPosts[index]['node']['is_video'] is True:
                    GetPicsAndVid(InfosPosts[index]['node']['video_url'],"Post{}_{}.mp4".format(username,index + 1))
                    ret['Posts'][index]['Vid'] = "Post{}_{}_.mp4".format(username,index + 1)
                else:
                    GetPicsAndVid(InfosPosts[index]['node']['display_url'],"Post{}_{}.jpg".format(username,index + 1))
                    ret['Posts'][index]['Pic'] = "Post{}_{}_.mp4".format(username,index + 1)
            NofPostToDownload -= 1

        # πͺππππππ πΊππππππͺππππππ() ππ ππππππππ πππ πππππππππ πππ πππππ ππ ππππ

        if Details is True :
            if ScrapeComments(username,InfosPosts[index]['node']['shortcode'],"{}_Comments_{}.txt".format(username,index),Commenters) is False:
                with open("Error.txt","w") as LogError:
                    LogError.write("[Error while downloading comments]")
                LogError.close()
            else:
                ret['Posts'][index]['Comments'] = "{}_Comments_{}.txt".format(username,index)
            
        # π·ππππππ πππππππ ππ πππππππ π―ππππ»πππ πππ ππππππ ππππ πππ πππ ππππ ππ πππ πππππ

        if InfosPosts[index]['node']['edge_media_to_caption']['edges']:
            InfosCaption = InfosPosts[index]['node']['edge_media_to_caption']['edges'][0]['node']['text']
            HashTagsList.append(ExtractThroughCaption('#',InfosCaption))
            TaggedUsers.append(ExtractThroughCaption('@',InfosCaption))
        else:
            IsCaptionAvailable = False

        if InfosPosts[index]['node']['edge_media_to_tagged_user']['edges']:
            for tu in InfosPosts[index]['node']['edge_media_to_tagged_user']['edges']:
                TaggedUsersInPics.append(tu['node']['user']['username'])

        index += 1
    return True

def ScrapeComments(username,shortcode,filename,commenters):

    # π΄πππππ πππππππ ππ πππ ππππ πππ πππππ πππ πππππππππ

    req = requests.get(f"https://www.instagram.com/p/{shortcode}/",headers=headers,cookies=cookies)
    if req.status_code == 404:
        fail("[!] Post not found")
    PostSoup = bs(req.text, 'html.parser')
    PostSoup.encode('utf-8')
    if "Login β’ Instagram" in str(PostSoup.find('title')):
        fail("[!] Error: Filouteries have been detected, try later or use a proxy!")

    try:
        Comment = PostSoup.find_all('script', attrs={'type': 'text/javascript'})
        if cookies:
            InfoComment = json.loads(Comment[14].get_text()[str(Comment[14].get_text()).find("{\"graphql"):].strip(');'))
            CommentSection = InfoComment['graphql']['shortcode_media']
        else:
            InfoComment = json.loads(Comment[3].get_text()[str(Comment[3].get_text()).find("{\"config"):].strip(';'))
            CommentSection = InfoComment['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        with open(filename,"wb+") as f:
            for i in CommentSection['edge_media_to_parent_comment']['edges']:
                if i['node']['owner']['username'] != username:
                    commenters.append(i['node']['owner']['username'])
                f.write((i['node']['owner']['username'] + ": " + i['node']['text'] + "\n").encode('utf-8'))
            f.close()
        if CommentSection['edge_media_to_caption']['edges']:
            InsertLines(filename,0,"__Caption__ : " + CommentSection['edge_media_to_caption']['edges'][0]['node']['text'])

    except:
        return False
    return True

def GetInsta(username):

    # π±πΊπΆπ΅ ππππππ πππππ

    global ret
    ret = {
        'Profile' : {},
        'Posts' : [],
        'Stats' : {},
        'Dorks' : {},
        'Story' : ""
    }

    # paramΓ¨tres Γ  implΓ© plus tard

    NofPostToAnalyze = 5
    NofPostToDownload = 1
    OptCom = True
    UseDork = True
    DownloadStory = True

    # π΄πππππ πππππππ ππ πππ ππππ π°ππππππππ ππππ

    WebPage = requests.get(f"https://www.instagram.com/{username}/",headers=headers,cookies=cookies)
    if WebPage.status_code == 404:
        fail("[!] Account not found")
    Sousoupe = bs(WebPage.text, 'html.parser')
    Sousoupe.encode('utf-8')
    if "Login β’ Instagram" in str(Sousoupe.find('title')):
        fail("[!] Filouteries have been detected, try later, connect to an account or use a proxy...")
    elif "Content Unavailable" in str(Sousoupe.find('title')):
        fail("[!] The account has been blocked by user, try using without account...")

    # π©πππππππ π·ππππππ'π ππππππ

    ret['path'] = CreateFolder(username)

    # π·ππππππ πππππ πππ ππππππ :)
    
    try:
        Main = Sousoupe.find_all('meta', attrs={'property' : 'og:description'})
        Profile = Sousoupe.find_all('script', attrs={'type': 'text/javascript'})
        InfosMain = Main[0].get('content').split()
    except IndexError:
        print("ERROR ERROR ERROR")
        with open("log.txt","w") as f:
            f.write(WebPage.text)
            os._exit()
    InfosProfile = json.loads(Profile[3].get_text()[str(Profile[3].get_text()).find("{\"config"):].strip(';'))
    InfosUser = InfosProfile['entry_data']['ProfilePage'][0]['graphql']['user']    
    InfosPosts = InfosProfile['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
    UserId = InfosUser['id']
    
    try:
        ProfileName = re.search('from (.*) \(@',Main[0].get('content')).group(1)
    except AttributeError:
        ProfileName = None
        ret['Profile']['Profile Name'] = False

    if ProfileName:
        ret['Profile']['Profile Name'] = ProfileName

    ret['Profile']['Followers'] = InfosMain[0]
    ret['Profile']['Following'] = InfosMain[2]
    ret['Profile']['Posts'] = InfosMain[4]
        
    with open("Biography_{}.txt".format(username),"wb") as f:
        f.write(InfosUser['biography'].encode('UTF-8'))
        f.close()

    ret['Profile']['Biography'] = "Biography_{}.txt".format(username)

    if GetPicsAndVid(InfosUser['profile_pic_url_hd'],"ProfilePic_{}.jpg".format(username)) is False:
        fail("[!] Error while downloading profile picture")
    else:
        convertImg("ProfilePic_{}.jpg".format(username))
        ret['Profile']['ProfilePic'] = "ProfilePic_{}.png".format(username)

    # π¬ππππππ πππππππ ππππππππππππ

    ret['Profile']['Private'] = InfosUser['is_private']
    ret['Profile']['Joined Recently'] = InfosUser['is_joined_recently']
    ret['Profile']['IsBusiness'] = InfosUser['is_business_account']
    ret['Profile']['Verified'] = InfosUser['is_verified']
    ret['Profile']['Username'] = username

    # π¬ππππππ ππππππππ ππππππππππππ

    if ret['Profile']['IsBusiness']:
        ret['Profile']['Category'] = InfosUser['business_category_name']

    if InfosUser['external_url']:
        ret['Profile']['Url'] = InfosUser['external_url']

    if InfosUser['connected_fb_page']:
        ret['Profile']['FaceBook Page'] = InfosUser['connected_fb_page']

    # π°π ππππ'π πππππππ ππ ππππππ _@_Β°\/Β°

    if InfosUser['is_private'] == False or cookies and InfosUser['followed_by_viewer'] == True:

        # π?πππππ πππππππππ πππ πππππ πππππππππ ππππ

        global HashTagsList
        global Commenters
        global TaggedUsers

        HashTagsList = []
        Commenters = []
        TaggedUsers = []

        AnalyzePosts(username,InfosMain[4],InfosPosts,NofPostToAnalyze,NofPostToDownload,OptCom)

        FinalHTList = list(itertools.chain.from_iterable(HashTagsList))

        FinalTUList = list(itertools.chain.from_iterable(TaggedUsers))
        FinalTUList += TaggedUsersInPics
                
        if Commenters:
            ret['Stats']['Commenters'] = sorting(Commenters)

        if FinalHTList:
            FinalHTListSorted = sorting(FinalHTList)
            with open("Hashtags_{}.txt".format(username),"wb") as Htlog:
                Htlog.write(("\n".join(FinalHTListSorted)).encode('utf-8'))
            Htlog.close()
            ret['Stats']['HashTags'] = FinalHTListSorted

        if FinalTUList:
            FinalTUListSorted = sorting(FinalTUList)
            with open("TaggedUsers_{}.txt".format(username),"wb") as Tulog:
                Tulog.write(("\n".join(FinalTUListSorted)).encode('utf-8'))
            Tulog.close()
            ret['Stats']['TaggedUsers'] = FinalTUListSorted
            
    if DownloadStory is True and cookies:
        GetStories(username,UserId)
        
    # πΌππππ π?πππππ πππππππ

    if UseDork is True:
        """
        ret['Dorks']['RespAllUrl'] = []
        ret['Dorks']['InstaText'] = []
        ret['Dorks']['RespAllText'] = []
        ret['Dorks']['AccountList'] = []
        """

        UseGoogleDorks(username,ret)

    return ret
            
def main(username,xavier):

    RetData = GetInsta(username)
    with open("{}.json".format(username),'w') as f:
        json.dump(RetData,f,sort_keys=True,indent=4)
        f.close()

    xavier.set()
    return RetData
