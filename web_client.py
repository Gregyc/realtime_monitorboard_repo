import requests

json_data = {'MacAddress': '00000601',\
             'Owner': 'Old Men',\
             'Category':1,\
             'Timestamp':12345,\
             'MapName':'ACARE實驗室'
             }

r = requests.post("http://127.0.0.1:5000/getsos", json=json_data)

print('headers:')
print(r.headers)
print('text:')
print(r.text)


