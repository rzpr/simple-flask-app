from flask import Flask, request
import requests
from bs4 import BeautifulSoup as bs
import json, base64

app = Flask(__name__)

@app.route('/')
def home():
    a = {
    'Contoh-Penggunaan':{'lirik': 'sdsd', 'facebook-downloader':'sadsd', 'nulis-bot':'sdsdsd', 'instagram-downloader': 's'}
    }
    return a

@app.route('/bot', methods=['GET'])
def fb():
    url = request.args.get('url')
    req = requests.get(url)
    sd = re.search('sd_src:"(.+?)"', req.text).group(1)
    hd = re.search('hd_src:"(.+?)"', req.text).group(1)
    js = {
    "results-hd": hd,
    "results-sd": sd
    }
    return js

@app.route('/nulis', methods=['GET'])
def tulis():
    from nulis import tulis
    text = request.args.get('text')
    tulis=tulis(text)
    for i in tulis.tulis():
        i.save('gambar.jpg')
        image = open('gambar.jpg', 'rb')
        image_read = image.read()
        image_64_encode = base64.encodebytes(image_read)
        url = 'https://api.imgbb.com/1/upload'
        par = {
         'key':'b76b9a5f05dafad41987044532b9e400',
         'image':image_64_encode,
         'name':'nulis',
         'expiration': 60
         }
        headers = {
         'Accept': 'application/json'
         }
        req = requests.post(url,data=par, headers=headers)
        p = req.json()['data']['display_url']
        js = {
         "results":p
         }
        return js

@app.route('/ig', methods=['GET'])
def ig():
    url = request.args.get('video_id')
    req = requests.get('https://instagram.com/p/'+url+'?__a=1')
    jss = req.json()['graphql']['shortcode_media']['video_url']
    js = {
    "results":jss
    }
    return js


@app.route('/lirik')
def lirik():
    res = []
    par= request.args.get('search')
    req = requests.get(f'https://www.google.com/search?q=lirik%20lagu%20{par}',headers={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'})
    soup = bs(req.text, 'html.parser')
    for i in soup.find_all('span',jsname='YS01Ge'):
        res.append(i.text)
    data = ''.join(res)
    js = {
    'resut': data
    }
    return json.dumps(js)

if __name__ == '__main__':
    app.run()
