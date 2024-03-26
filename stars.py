import json,requests


with open("database.json",'r') as f:
    data=json.load(f)

s=len(data)
#print(s)

X=2
dict={}
while X<s:
    try :
        Question=data[X]["message"]
        Answer=data[X+1]["message"]
        dict.__setitem__(Question,Answer)
        X=X+2
    except IndexError:
        break
    

#print(dict)


headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMjk3MWJiNjItODgyNy00MDdlLTk5MWEtMjU1ZjVhZWU3ZTY3IiwidHlwZSI6ImFwaV90b2tlbiJ9.J08Nu3TJhFvo88oOdyFO21XSgHLbIn6OXywQ6iGctkg"}

url = "https://api.edenai.run/v2/text/chat"
i=0
for key in dict.keys():
    payload = {
        "providers": "openai",
        "openai":"gpt-4",
        # "text": '''Question :Great! Let's begin the technical questions. Can you elaborate on your experience with Python and how you have used it in your software development projects? 
        #             Answer : I have good experience in Python.I have been working with python for last 3 years and i have gained many experience in it
        #                     .I had used python in many of my ML projects as python supports many ML libraries.Also i have used python for creating 
        #                        web appliction s using its web framework like Flask.   ''',
        "text": f'''Question:{key}
                    Answer: {dict[key]}
                    ''',
        "chatbot_global_action": '''
                                    you have a task to give rating to pair of question answer on the scale of 1 to 10 based on 
                                    relevance,quality,accuracy of answer depending upon the question.If the question's answer is based on past experience or
                                    dependent on each person view's the you cna give it a rating of 5 and if the answer is totally wrong then give it a 0 rating.Also provide a model asnwer to that question assuming yourslef
                                    in that position.
                                ''',
        "previous_history": [],
        "temperature": 0.9,
        "max_tokens": 1000,
        "fallback_providers": ""
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    text=result['openai']['generated_text']
    print(text)
    i=i+1






