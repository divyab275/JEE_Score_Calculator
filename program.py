import requests
import re
import sys

from bs4 import BeautifulSoup
webpage = sys.argv[1]
page = requests.get(webpage)
soup = BeautifulSoup(page.content, 'html.parser')
questions = soup.find_all('table',class_="menu-tbl")
answers={}
for que in questions:
    children  =list(que.children)
    qno = children[1].get_text()
    opt = children[8].get_text()
    if(opt.isdigit()):
        answers[qno[13:]] = children[int(opt)+1].get_text()[13:]
    else:
        answers[qno[13:]] = "0"
    


ans_page  = open('JEE(Main).htm',encoding="utf8")
soup = BeautifulSoup(ans_page, 'html.parser')
exp = re.compile("ctl00_ContentPlaceHolder1_grAnswerKey_ctl(0[2-9]|[1-8][0-9]|90|91)_lbl_QuestionNo")
result_que = soup.find_all(id=exp)
exp2 = re.compile("ctl00_ContentPlaceHolder1_grAnswerKey_ctl(0[2-9]|[1-8][0-9]|90|91)_lbl_RAnswer")
result_ans = soup.find_all(id=exp2)
result_ans_list = list(result_ans)
score = 0
no_of_answered = 0
no_of_unattempted = 0
no_of_correct = 0
no_of_incorrect = 0
ele = 0
for q in result_que:
    qid = q.get_text()
    correct_ans = result_ans_list[ele].get_text()
    marked_ans = answers[q.get_text()]
    # print(qid,correct_ans,marked_ans)
    if(marked_ans!="0"):
        #Answered
        if(marked_ans==correct_ans):
           #Correct
           no_of_correct += 1
           score += 4
        else:
            #Incorrect
            no_of_incorrect += 1
            score -= 1
        no_of_answered+=1
    else:
        no_of_unattempted += 1
        
    ele = ele+1
print("Answered",no_of_answered)
print("Unanswered",no_of_unattempted)
print("Correct Answers",no_of_correct)
print("Incorrect Answers",no_of_incorrect)
print("Score",score)