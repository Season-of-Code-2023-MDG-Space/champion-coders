import requests     
import json

class apiView():
        def apiCall():
            response_API = requests.get('https://the-trivia-api.com/api/questions?limit=1')
            data = response_API.text
            #print(response_API.status_code)
            print(data)
            q_list = json.loads(data)
            z=q_list[0]
            # corrans=data[0]
            # listAll=data[0][3]
                    #Testing for api
            a=z["correctAnswer"]
            b=z["incorrectAnswers"]
            ques=z["question"]
            rightans = z["correctAnswer"]
            b.append(a)
            dictTest=[a,b,ques]
            return dictTest
            
# listAll.append(corrans)