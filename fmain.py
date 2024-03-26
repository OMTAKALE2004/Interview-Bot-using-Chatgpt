from flask import Flask,request,render_template
import requests,json
import playsound,os,speech_recognition,gtts


headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMjk3MWJiNjItODgyNy00MDdlLTk5MWEtMjU1ZjVhZWU3ZTY3IiwidHlwZSI6ImFwaV90b2tlbiJ9.J08Nu3TJhFvo88oOdyFO21XSgHLbIn6OXywQ6iGctkg"}

app=Flask(__name__)

@app.route("/",methods=["GET", "POST"])
@app.route("/talk",methods=["GET", "POST"])

def talk():
    if request.method == "POST":
        if request.form["action"] == "start":
            speech_text=speech_to_text()
            gpt=chatgpt(speech_text)
            text_to_speech(gpt)

    return render_template("form2.html")



#Funtions
def cv_extracter():
    url = "https://api.edenai.run/v2/ocr/resume_parser"
    data = {
        "providers": "affinda",
        "fallback_providers": ""
    }
    files = {'file': open("image-1652441755690.jpg", 'rb')}

    response = requests.post(url, data=data, files=files, headers=headers)
    result = json.loads(response.text)
    result=result['affinda']['extracted_data']
    Interviwee_info=''
    #extracting Useful data from result
    try:
        raw_name=result['personal_infos']['name']['raw_name']
        self_summary=result['personal_infos']['self_summary']
        education=result['education']['entries']
        college=education[0]['establishment']
        gpa=education[0]['gpa']
        if gpa==None:
            gpa="Good"
        degree_name=education[0]['accreditation']
        skills=result['skills']
        skill_1=[]
        for skill in skills:
            skill_1.append(skill["name"])
        certificates=result['certifications']
        certificates_1=[]
        for certif in certificates:
            certificates_1.append(certif['name'])

        Interviwee_info=f'''My name is {raw_name} and had done {degree_name} from {college} college with a {gpa} 
                    gpa.I have following {skill_1} and I have also done courses like {certificates_1}.
                        I'm here to give technical Interview and this is my self summary {self_summary}'''

    except IndexError:
        Interviwee_info=f'''{result}'''

    return Interviwee_info




def speech_to_text():
    recognizer=speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Say something!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    #convert listened file to wav format
    with open("microphone-results.wav", "wb") as f:
        f.write(audio.get_wav_data())

    filename="microphone-results.wav"
    current_directory = os.getcwd()
    absolute_path = os.path.join(current_directory, filename)

    url = "https://api.edenai.run/v2/audio/speech_to_text_async"
    data1 = {
        "providers": "openai",
        "language": "en-US",
    }

    files = {'file': open(absolute_path, 'rb')}

    response = requests.post(url, data=data1, files=files, headers=headers)
    result = json.loads(response.text)
    
    #print(result['results']['openai']['text'])
    return result['results']['openai']['text']



Interviwee_info=cv_extracter()
url = "https://api.edenai.run/v2/text/chat"

payload = {
    "providers": "openai",
    "openai":"gpt-4",
    "text": " ",
    "chatbot_global_action": '''
                        Task: act as a smart and intelligent interviewer
                        Topic: Technical Questions
                        Style: Formal
                        Tone: Professional
                        Audience: 25-30 year old
                        Word Count: 20 words
                        Format: Text
                            ''',
    "previous_history": [{'role':'user','message':Interviwee_info}],
    "temperature": 0.9,
    "max_tokens": 1000,
    "fallback_providers": ""
}
history=[{'role':'user','message':Interviwee_info}]


def chatgpt(speech_text):
    payload["text"]=speech_text
    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    text=result['openai']['generated_text']

    for i in result['openai']['message']:
            #payload["previous_history"].append(i)
            history.append(i)

    save_data()



    return text



def text_to_speech(gpt):
        text=gpt
        sound=gtts.gTTS(text,lang="en")
        sound.save("interview_bot.mp3")
        playsound.playsound("interview_bot.mp3")
        os.remove("interview_bot.mp3")

def save_data():
        payload["previous_history"].extend(history[-4:])
   
        with open("database.json",'w') as f:
                    json.dump(history,f,indent=2)



if __name__ == '__main__':
   app.run(debug = True)
   