# python3  
# -*- coding: utf-8 -*-  
"""  
 @desc:  百度OCR
 @author: Steven  
 @contact: Steven2947@163.com   
 """

from aip import AipOcr


APP_ID = '10754178'
API_KEY = '2Fal6IyMGxn6VGt5vvQPtVb9'
SECRET_KEY = 'NKxzDGIk1rUnEy1fg4dvvD96Oor35Zjw'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

url = "http://www.hnstrip.com/info/uploads/allimg/170116/142P26013-0.png"

out = client.basicGeneralUrl(url)

print(out)