from flask import Flask
import requests as r, re
from flask import request
import json

app = Flask(__name__)
 
@app.route('/')
def home():
    return "ONLINE"
 
@app.route('/postjson', methods = ['POST'])
def postJsonHandler():
    print (request.is_json)
    content = request.get_json()
    req = r.get(content['url'])
    sd = re.search('sd_src:"(.+?)"', req.text).group(1)
    hd = re.search('hd_src:"(.+?)"', req.text).group(1)
    js = {
    "results":{
    "link-downloads":{
        "sd-quality":sd,
        "hd-quality":hd
     }
     }
     }
    return js
  

@app.route('/bot', methods=['GET'])
def fb():
    url = request.args.get('url')
    req = r.get(url)
    sd = re.search('sd_src:"(.+?)"', req.text).group(1)
    hd = re.search('hd_src:"(.+?)"', req.text).group(1)
    js = {
    "results":{

        "original-url" : url,

    "link-downloads":{

        "sd-quality":sd,

        "hd-quality":hd 
     }

       }
    
       }
    return js

@app.route('/ig')
def ig():
    url = request.args.get('video_id')
    req = r.get('https://instagram.com/p/'+url+'?__a=1')
    jss = req.json()['graphql']['shortcode_media']['video_url']
    js = {
    "results":{
        "original-url" : 'https://instagram.com/p/'+url,
    "link-downloads":{
        "url":jss,
      }
      }
     }  
    return js

@app.route('/simi')
def simi():
    us = request.args.get('text')
    url = 'https://wsapi.simsimi.com/190410/talk/'
    body = {
      'utext': us, 
      'lang': 'id',
      'country': ['ID'],
      'atext_bad_prob_max': '0.7'
     }
    headers = {
      'content-type': 'application/json', 
      'x-api-key': 'RCxkgGt_JnYs6sOFx6bqOSXQV17BDlDQjC4CHkVc'
      }
    qq = r.post(url, data=json.dumps(body), headers=headers)
    js = qq.json()['atext']
    jsp = {
     "results":{
         "status" : 'ok',
     "response":{
         "text":js,
      }
      }
     }  
    return jsp
    
if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
