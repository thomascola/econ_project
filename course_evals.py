from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import regex as re
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()
subject = "CMSC"
year = "2022"
driver.get("https://coursefeedback.uchicago.edu/?Department="+subject+"&AcademicYear="+year+"&AcademicTerm=All")
driver.implicitly_wait(30)
username = driver.find_element_by_xpath("/html/body/div[2]/div[2]/main/div[2]/div/div/form/div[1]/div[2]/div[1]/div[2]/span/input")
user = input("Username for uchicago: ")
username.send_keys(user)
password = driver.find_element_by_xpath("/html/body/div[2]/div[2]/main/div[2]/div/div/form/div[1]/div[2]/div[2]/div[2]/span/input")
user = input("Password for uchicago: ")
password.send_keys(user)
submit_button = driver.find_element_by_xpath("/html/body/div[2]/div[2]/main/div[2]/div/div/form/div[2]/input")
submit_button.click()
time.sleep(40)
soup = BeautifulSoup(driver.page_source)
table = soup.find_all("tbody")[0]
course_ids = list()
course_titles = list()
eval_links = list()
course_quarters = list()
large_datas = list()
course_instructors = list()
htmls = list()
for x in table:
    course_id = x.find_all(class_="course")[0].find_all("a")[0].contents[0]
    if any(re.findall(r'2[0-9]{4}', str(course_id))):
        continue
    if any(re.findall(r'3[0-9]{4}', str(course_id))):
        continue
    if any(re.findall(r'4[0-9]{4}', str(course_id))):
        continue
    course_quarter = x.find_all(class_="quarter")[0].contents[0]
    if any(re.findall(r'[sS]ummer', str(course_quarter))):
        continue
    course_title = x.find_all(class_="title")[0].find_all("a")[0].contents[0]
    eval_link = re.findall(r'href=(.*) target', str(x.find_all(class_="title")[0].find_all("a")[0]))[0]

    driver.execute_script('''window.open("http://bings.com","_blank");''')
    chwd = driver.window_handles
    driver.switch_to.window(chwd[-1])
    driver.get(x.find_all(class_="title")[0].find_all("a")[0]['href'])
    time.sleep(1)
    htmls.append(driver.page_source)
    driver.switch_to.window(chwd[0])
    if any(x.find_all(class_="instructor")):
        if any(x.find_all(class_="instructor")[0].contents):
            course_instructor = x.find_all(class_="instructor")[0].contents[0]
        else:
            course_instructor = "N/A"
    else: 
        course_instructor = "N/A"
    
    course_ids.append(course_id)
    course_titles.append(course_title)
    eval_links.append(eval_link)
    course_instructors.append(course_instructor)
    course_quarters.append(course_quarter)
print(htmls[0])
driver.quit()
large_datas = list()
for x in htmls:
    eval_soup = BeautifulSoup(x)
    article = eval_soup.find_all("article")[0]
    enrolled = re.findall(r'>([0-9]+)</span>',str(article.find_all("header", class_= "cover-page")[0].find_all("div", class_="metadata")[0].find_all(class_="audience-data")[0].contents[1].contents[3]))[0]
    responded = re.findall(r'>([0-9]+)</span>',str(article.find_all("header", class_= "cover-page")[0].find_all("div", class_="metadata")[0].find_all(class_="audience-data")[0].contents[1].contents[7]))[0]
    blocks = article.find_all(class_="report-block")
    block_titles = list()
    datas = list()
    for block in blocks:
        block_title = block.find_all(class_="ReportBlockTitle")[0].contents[0].contents[0]
        data = list()
        if any(block.find_all(class_= "CommentBlockRow TableContainer")):
            type = "CommentBlockRow TableContainer"
            block_content = block.find_all(class_= "CommentBlockRow TableContainer")[0].find_all("tbody")
            for x in block_content:
                comments = x.find_all(class_="TabularBody_LeftColumn")
                for comment in comments:
                    data.append((type, block_title,comment.contents[0]))
        elif any(block.find_all(class_= "SpreadsheetBlockRow TableContainer")):
            type = "SpreadsheetBlockRow TableContainer"
            categories = list()
            block_header = block.find_all(class_="CondensedTabularHeaderRows")[0].find_all("th")
            for info in block_header:
                if any(info.contents):
                    categories.append(info.contents[0])
                else:
                    categories.append("Blank")
            block_content = block.find_all(class_="CondensedTabularOddRows")
            full_stats = list()
            for content in block_content:
                one_stat = list()
                comment = content.find_all(class_="TabularBody_LeftColumn")[0]
                one_stat.append(comment.contents[0])
                stats = content.find_all(class_="TabularBody_RightColumn_NoWrap2")
                statistics = list()
                for stat in stats:
                    statistics.append(stat.contents[0])
                one_stat.append(statistics)
                full_stats.append(one_stat)
            data = list()
            for x in full_stats:
                data.append((type, block_title, x))
                
        elif any(block.find_all(class_ = "FrequencyBlockRow")):
            type = "FrequencyBlockRow"
            info = block.find_all(class_="FrequencyBlockRow")[0].find_all(class_="FrequencyBlock_chart")[0].contents[0]['src']
            prefix = "https://uchicago.bluera.com"
            data = (type, block_title, prefix+info)
        datas.append(data)
    large_datas.append(datas)
df = pd.DataFrame()
df["Course Code"] = course_ids
df["Course Title"] = course_titles
df["Quarter"] = course_quarters
df["Instructor"] = course_instructors
df["Course Evaluation Data"] = large_datas

comment_questions = set()
numerical_questions = set()
graphical_questions = set()
for x in df["Course Evaluation Data"]:
    for y in x:
        if y[0][0] == 'CommentBlockRow TableContainer':
            for z in y:
                comment_questions.add(z[1])
        elif y[0][0] == 'SpreadsheetBlockRow TableContainer':
            for z in y:
                numerical_questions.add(str(z[1] + str(z[2][0])))
        elif y[0] == 'FrequencyBlockRow':
            graphical_questions.add(y[1])
numerical_questions = list(numerical_questions)
comment_questions  = list(comment_questions)
for question in comment_questions:
    large_text = list()
    for x in df["Course Evaluation Data"]: #for each class in df#
        for y in x: # for each block in class #
            text = list()
            if y[0][1] == question:
                for z in y: #for each comment in block #
                    text.append(z[2])
                break
        large_text.append(text)
    df[question] = large_text
for question in numerical_questions:
    large_text = list()
    for x in df["Course Evaluation Data"]:
        for y in x:
            flag = False
            for z in y: 
                text = list()
                if str(z[1] + str(z[2][0])) == question:
                    print("hello")
                    text.append(z[2][1])
                    flag = True
                    break
            if flag:
                break
        large_text.append(text)
    df[question] = large_text
for question in graphical_questions:
    large_text = list()
    for x in df["Course Evaluation Data"]:
        for y in x:
            link = "N/A"
            if len(y) > 1 and y[1] == question:
                link = y[2]
                break
        large_text.append(link)
    df[question] = large_text
print(df)
df.to_csv(subject+"_"+year+".csv")