import requests

url = 'https://104.28.2.6:443/sszhfx/'
headers = {
    ':authority': 'doub.io',
    ':method': 'GET',
    ':path': '/sszhfx/',
    ':scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'cookie': '__cfduid=d933123518c554704a77dec3b639e62191529377820',
    'pragma': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
res = requests.get(url=url, headers=headers).text
print(res)

