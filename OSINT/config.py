from random import choice

proxies = {'https' : "socks5h://x5200535:GTyKPFX6Po@109.201.154.247:1080",
    'http' : "socks5h://x5200535:GTyKPFX6Po@109.201.154.247:1080"}

UserAgent =  [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    ]

headers = {"user-Agent": choice(UserAgent),'referer':'https://www.google.com/',"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp",}

cookies={}

DorkList = {
    'InstaText' : 'https://www.google.com/search?q=intext%3A%27{}%27+site%3A%27www.instagram.com%27',
    'GlobalUrl' : 'https://www.google.com/search?q=inurl%3A%27{}%27',
    'GlobalText' : 'https://www.google.com/search?q=intext%3A%27{}%27'
}
