import pandas as pd
import regex as re

subject = "CMSC"
year = "2022"
df = pd.read_csv(subject+ "_"+year+"_Cleaned_Images_Done.csv")
for col in df.columns:
    means = list()
    yess = list()
    yess_flag = False
    means_flag = False
    for ind in df.index:
        if "Mean':" in str(df[col][ind]):
            print(df[col][ind])
            mean = re.findall(r"'Mean': '(.*?)'", str(df[col][ind]))[0]
            means.append(mean)
            means_flag = True
        else:
            means.append(df[col][ind])
        if 'Yes' in str(df[col][ind]) and any(re.findall(r"'Yes': '(.*?)%'", str(df[col][ind]))):
            yes = re.findall(r"'Yes': '(.*?)%'", str(df[col][ind]))[0]
            yes = float(yes)/100
            yess.append(yes)
            yess_flag = True
        else:
            yess.append(df[col][ind])
    if yess_flag:
        df[col]= yess
    elif means_flag:
        df[col] = means
#for x in df["Why did you choose to take this course? (Select all that apply)"]:
average_hours = list()
for x in df["How many hours per week outside of attending required sessions did you spend on this course?"]:
    if isinstance(x, float):
        average_hours.append("N/A")
        continue
    hours = re.findall(r": '(.*?)'", str(x))
    info = [2.5, 7.5, 12.5, 17.5, 22.5, 27.5, 32.5]
    num_people = 0
    total_hours = 0
    
    for y in range(len(info)):
        num_people += int(hours[y])
        total_hours += info[y] * int(hours[y])
    average_hours.append(total_hours/num_people)
df["How many hours per week outside of attending required sessions did you spend on this course?"] = average_hours
interest_score = list()
for x in df["Prior to starting this class, your interest level was?"]:
    if isinstance(x, float):
        interest_score.append("N/A")
        continue
    values = re.findall(r": '(.*?)'", str(x))
    info = [-1, -0.5, 0, 0.5, 1]
    num_people = 0
    total_value = 0
    for y in range(len(info)):
        num_people += int(values[y])
        total_value += info[y] * float(values[y])
    interest_score.append(total_value/num_people)
df["Prior to starting this class, your interest level was?"] = interest_score
reputation_score = list()
for x in df["Why did you choose to take this course? (Select all that apply)"]:
    if isinstance(x, float):
        reputation_score.append("N/A")
        continue
    values = re.findall(r": '(.*?)'", str(x))
    values = [int(value) for value in values]
    reputation_score.append(float(values[-1])/max(values))
df["Why did you choose to take this course? (Select all that apply)"] = reputation_score
df.to_csv("data_extracting_"+subject+"_"+year+".csv")
        
