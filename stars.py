import json,requests,time
from fpdf import FPDF


title="Interview Bot"
class PDF(FPDF):
    def header(self):
        # Rendering logo:
        self.image("gen ai logo.jpeg", 10, 8, 25)
        # Setting font: helvetica bold 15
        self.set_font("helvetica", "BIU", 25)
        # Moving cursor to the right:
        self.cell(80)
        width = self.get_string_width(title) + 6
        doc_w=self.w
        self.set_x((doc_w - width) / 2)
        # Printing title:
        self.cell(width, 10, title, border=0, align="C")
        # Performing a line break:
        self.ln(40)
        pdf.line(x1=4,y1=40,x2=206,y2=40)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}", align="C")



pdf = PDF()
pdf.add_page()

pdf.add_font('Dosis','B',r'Dosis\static\Dosis-Bold.ttf',uni=True)

pdf.add_font('Dosis','',r'Dosis\static\Dosis-Regular.ttf',uni=True)
#pdf.add_font('Dosis','',r'Dosis\Dosis-VariableFont_wght.ttf',uni=True)
#pdf.set_font("Times", size=12)
# global i
# i=0
# def pdf_question():
#     pdf.set_font("Times",'B',12)
    
    
def pdf_style(i):
        # i=i+1
        pdf.rect(4,4,202,290)
        pdf.set_font("Dosis",style='B',size=13)
        pdf.multi_cell(0, 10, f"Question {i}:", new_x="LMARGIN", new_y="NEXT",align="L")

        pdf.set_font("Dosis",style='B')
        pdf.multi_cell(0, 10, f"{key}", new_x="LMARGIN", new_y="NEXT",align="L")
        pdf.ln(0.5)

        pdf.set_font("Dosis",style='B',size=13)
        pdf.multi_cell(0, 10, f"Answer:", new_x="LMARGIN", new_y="NEXT",align="L")

        pdf.set_font("Dosis",style='')
        pdf.multi_cell(0, 10, f"{dict[key]}", new_x="LMARGIN", new_y="NEXT",align="L")
        pdf.ln(0.5)

        pdf.set_font("Dosis",style='B',size=13)
        pdf.multi_cell(0, 10, f"Model Answer and Rating:", new_x="LMARGIN", new_y="NEXT",align="L")

        pdf.set_font("Dosis",style='')
        pdf.multi_cell(0, 10, f"{text}", new_x="LMARGIN", new_y="NEXT",align="L")
        pdf.ln(0.5)
        pdf.ln(1)
        
    



with open("database.json",'r') as f:
    data=json.load(f)

s=len(data)
print(s)

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

    except UnicodeEncodeError:
        break
    

#print(dict)


headers = {"Authorization": "Bearer //api_key//"}

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
        # "chatbot_global_action": '''
        #                             you have a task to give rating to pair of question answer on the scale of 1 to 10 based on 
        #                             relevance,quality,accuracy of answer depending upon the question.If the question's answer is based on past experience or
        #                             dependent on each person view's the you cna give it a rating of 5 and if the answer is totally wrong then give it a 0 rating.
        #                             Also provide a model asnwer to that question assuming yourslef
        #                             in that position.
        #                         ''',
        "chatbot_global_action":''' Task :You to analyze set of Questions and Answer from a interview.You have two task rate the answer 
                                         on the scale of 1 to 10 .Provide a better answer to that question.
                                         return the response in following format of:-
                                            Rating:"" 
                                            Model Answer:"",


                                    Style: Formal
                                    Tone: Professional
                                    word count : less than 50
                                                                '''

                                    ,
        "previous_history": [],
        "temperature": 0.9,
        "max_tokens": 1000,
        "fallback_providers": "replicate"
    }
   
    key1=key
    
   
    
    i=i+1
    try:
        response = requests.post(url, json=payload, headers=headers)
        result = json.loads(response.text)
        text=result['openai']['generated_text']
        

        
        pdf_style(i)
       
        print("hello")
       
    except KeyError:
        continue
   

print("stopped")
pdf.output("new-tuto2.pdf")






