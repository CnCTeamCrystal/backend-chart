
# coding: utf-8

# In[ ]:



import pandas as pd
import numpy as np
import plotly.offline as offline 
import plotly.graph_objs as go 
from flask import Flask, render_template
from flask import request
import json
import plotly
from flask_cors import CORS
import sys

reload(sys)
sys.setdefaultencoding('utf-8')






def get_url(item_name ): 
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False) 
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code) 
    print("요청 URL = {}".format(url)) 
    return url


app = Flask(__name__)
CORS(app)
@app.route('/chart',methods=['POST','OPTIONS'])
def chart():
    item_name= request.form['name'].encode('utf8')
    url = get_url(item_name)

    df = pd.DataFrame()  

    for page in range(1, 21): 
        pg_url = '{url}&page={page}'.format(url=url, page=page) 
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True) 


    df = df.dropna()
    df.columns = ['date','close', 'diff', 'open', 'high', 'low', 'volume']
    df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'], ascending=True)

#df.head()

    offline.init_notebook_mode(connected=True)
    trace = go.Scatter( x=df.date, y=df.close, name=item_name) 
    data = [trace]

    layout = dict( title='{}의 종가(close) Time Series'.format(item_name), xaxis=dict( rangeselector=dict( buttons=list([ dict(count=1, label='1m', step='month', stepmode='backward'), dict(count=3, label='3m', step='month', stepmode='backward'), dict(count=6, label='6m', step='month', stepmode='backward'), dict(step='all') ]) ), rangeslider=dict(), type='date' ) ) 
    fig = go.Figure(data=data, layout=layout) 
 #   offline.iplot(fig)
    
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#    return render_template('layouts/index.html', graphJSON=graphJSON)
#    return "helloworld"
    return app.response_class(response=graphJSON , status=200,mimetype='application/json')

if __name__=='__main__':
    global code_df 
    code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
    code_df.columns=['name' , 'code' , 'a' , 'b' , 'c' , 'd' , 'e', 'f' ,'g']
    code_df.code = code_df.code.map('{:06d}'.format)
    app.run(host='0.0.0.0' , port=8080)






