from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
import requests
from config import Config
from mysql_connection import get_connection
from mysql.connector import Error


class ChineseResource(Resource):
    def post(self):

        data = request.get_json()

        # 네이버의 파파고 API를 호출하여 결과를 가져온다.
        # 파이썬 라이브러리(포스트맨 리퀘스트 직접 불러오는 라이브러리)
        # 파파고 API의 문서를 보고 어떤 데이터를 보내야하는지 파악하여
        # requests의 get, put, post, delete 등의 함수를 이요하여 호출하면 된다. 
        
        req_data = {
                        "source" : "ko",
                        "target" : "zh-CN",
                        "text" : data['sentence']
                    }
        
        req_header = { 
                        "X-Naver-Client-Id" : Config.NaverClientId,
                        "X-Naver-Client-Secret" : Config.NaverClientSecret
                    }
        
        response = requests.post('https://openapi.naver.com/v1/papago/n2mt',
                      req_data,
                      headers=req_header)
        
        # 데이터를 파파고 서버로 부터 받아왔으니 
        # 우리가 필요한 데이터만 뽑아내면 된다.
        
        print(response)

        # 원하는 데이터를 뽑기위해서 json으로 먼저 만들어놔야 한다.
        response = response.json()

        print()
        print(response)

        # 클라이언트에게 보여줄 결과물(리스트내의 딕셔너리, 데이터 액세스)
        chinese = response['message']['result']['translatedText']


        return {"result":chinese}, 200 
    


class NewsResource(Resource):
    def get(self):

        query = request.args.get('query')

        # 네이버 뉴스 검색 API를 호출

        query_string = {'query':query,
                        'display':30,
                        'sort':'date'}

        req_header = { 
                        "X-Naver-Client-Id" : Config.NaverClientId,
                        "X-Naver-Client-Secret" : Config.NaverClientSecret
                    }

        response = requests.get('https://openapi.naver.com/v1/search/news.json',
                      params=query_string,
                      headers=req_header)

        # reponse는 json으로 해줘야한다.
        response = response.json()

        print(response)

        return {"result":"success", 
                "items":response['items'],
                "count":len(response['items'])}, 200
    