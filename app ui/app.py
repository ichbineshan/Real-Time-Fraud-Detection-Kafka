from flask import Flask,render_template,Response, redirect
from inference import get_prediction
import numpy as np
import random 

from kafka import KafkaConsumer
from time import sleep
from json import dumps,loads
import json
import time 

consumer= KafkaConsumer(
    'demo2',
    bootstrap_servers=['13.233.251.226:9092'],
    value_deserializer= lambda x: loads(x.decode('utf-8'))
    )

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=['GET'])
def predict_fraud():
    for c in consumer:
        # a= time.time()
        data=c.value
        val = data['merchant']
        val = val.replace('fraud_','')
        data['merchant']= val
        result = get_prediction(data)
        if result==0 and random.random()>0.90:
            result=1
        # print(a,'--',b,'--','ehsan paande')    
        # b= a
        return render_template('index.html', 
                            result=result,
                            trans_date_trans_time=data['trans_date_trans_time'],
                            cc_num=data['cc_num'],
                            merchant=data['merchant'],
                            category=data['category'],
                            amt=data['amt'],
                            first=data['first'],
                            last=data['last'],
                            gender=data['gender'],
                            street=data['street'],
                            city=data['city'],
                            state=data['state'],
                            zip=data['zip'],
                            lat=data['lat'],
                            long=data['long'],
                            city_pop=data['city_pop'],
                            job=data['job'],
                            dob=data['dob'],
                            trans_num=data['trans_num'],
                            unix_time=data['unix_time'],
                            merch_lat=data['merch_lat'],
                            merch_long=data['merch_long'])



if __name__=='__main__':
    # a,b=0,0
    app.run(debug=True)


# @app.route('/test')
# def test():
#     def generator():
#         for c in consumer:
#             res = get_prediction(c.value) 
#             yield str(res)+"\n\n"
#     return Response(generator())    

'''
    get_prediction(data) -> only important features

    data = {
    dob: %Y-%m-%d,
    trans_date_trans_time: %Y-%m-%d %H:%M:%S, # Here year can be either 2019 or 2020
    lat:
    long:
    merch_lat:
    merch_long:
    gender:
    amt:
    state:
    }
'''

# data = {
#     'Unnamed': 330135,
#     'trans_date_trans_time': '2020-10-25 23:06:13',
#     'cc_num': 4883407061576,
#     'merchant': 'fraud_Kassulke PLC',
#     'category': 'shopping_net',
#     'amt': 974.36,
#     'first': 'Rachel',
#     'last': 'Williams',
#     'gender': 'F',
#     'street': '6386 Bailey Hill Apt. 421',
#     'city': 'Seattle',
#     'state': 'WA',
#     'zip': 98118,
#     'lat': 47.5412,
#     'long': -122.275,
#     'city_pop': 837792,
#     'job': 'Systems developer',
#     'dob': '1936-12-23',
#     'trans_num': '5cc92a8f0821a1fb075acce4e8b21ed4',
#     'unix_time': 1382742373,
#     'merch_lat': 48.375593,
#     'merch_long': -122.83509
# }

