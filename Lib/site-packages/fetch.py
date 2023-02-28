import requests
import json
import random


class QuizQuestion():
            
            def questions():
                response_API = requests.get('https://the-trivia-api.com/api/questions?limit=1')
                data = response_API.text
                #print(response_API.status_code)
                #print(data)
               
                q_list = json.loads(data)
                z=q_list[0]

                right = z["correctAnswer"]
                q=z["question"]
                falseoption1=z["incorrectAnswers"][0]
                falseoption2=z["incorrectAnswers"][1]
                falseoption3=z["incorrectAnswers"][2]

                inanswers={"0":falseoption1,"1":falseoption2,"2":falseoption3}
                dict={}
                dict[0]=q
                dict[1]=right
                dict[2]=inanswers
                options=[]
                new_options=[]
            

                for i in range(0,len(q_list)):
                    
                    new_options.append(q_list[i]["correctAnswer"])
                    for n in range(0,3):
                        new_options.append(q_list[i]["incorrectAnswers"][n])

                    options.append(new_options)

                
                



            
            
                #print(f'{q_list[0]["question"]}')
                random.shuffle(options[0])
                l = []
                for n in range(0,4):
                    l.append(options[0][n])
                #print(f'A.{options[0][0]}\nB.{options[0][1]}\nC.{options[0][2]}\nD.{options[0][3]}')
                
                def ret(a,b):
                    if a == 'A':
                        return 0
                    elif a == 'B':
                        return 1
                    elif a == 'C':
                        return 2
                    else:
                        return 3
                    
                for n in range(0,4):      
                    if q_list[0]["correctAnswer"] == options[0][n]:
                        dict[3]=n+1
                

                dict[4]=options
                return dict

