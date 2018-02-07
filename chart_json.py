
# coding: utf-8

# In[ ]:


import time
from flask import Flask
from flask import request
import json
from flask import jsonify
#import request
from six.moves import urllib
from bs4 import BeautifulSoup

app = Flask(__name__)
@app.route('/chart', methods=['GET'])
def chart():
    stockItem = '005930'

    url = 'http://finance.naver.com/item/sise_day.nhn?code='+ stockItem
    html = urllib.request.urlopen(url)
    source = BeautifulSoup(html.read(), "html.parser")
    maxPage=source.find_all("table",align="center")
    mp = maxPage[0].find_all("td",class_="pgRR")
    #mpNum = int(mp[0].a.get('href')[-3:])
    mpNum = 5
    result = []
    for page in range(1, mpNum+1):
    #    print (str(page) )
        url = 'http://finance.naver.com/item/sise_day.nhn?code=' + stockItem +'&page='+ str(page)
        html = urllib.request.urlopen(url)
        source = BeautifulSoup(html.read(), "html.parser")
        srlists=source.find_all("tr")
        isCheckNone = None

   # if((page % 1) == 0):
   #     time.sleep(1.50)
   #len(srlists)-1
        for i in range(1,len(srlists)-1):
            if(srlists[i].span != isCheckNone):
                srlists[i].td.text
#                print(srlists[i].find_all("td",align="center")[0].string)
                srlist ={'center':srlists[i].find_all("td",align="center")[0].string,'num':srlists[i].find_all("td",class_="num")[0].string}
                result.append(srlist)
    jsf = json.dumps(result, ensure_ascii=False)
    return app.response_class(response=jsf , status=200,mimetype = 'application/json')
#    return "hello world"

if __name__ == '__main__':
    app.run(host="0.0.0.0" , port=int("8080"))

