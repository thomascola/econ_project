import pandas as pd
from csv import DictReader
import regex as re
subject = "CMSC"
year = "2022"
df = pd.read_csv(subject + "_"+year+".csv")
print(df)
print(df.columns)
for col in df.columns:
    larger_numbers = list()
    for ind in df.index:
        if any(re.findall(r'\[\[.*\]\]', str(df[col][ind]))):
            numbers = re.findall(r"'(.*?)'", str(df[col][ind]))
            numbers = list(numbers)
            numbers_dict = dict()
            if len(numbers) == 2:
                numbers_dict['Yes'] = numbers[0]
                numbers_dict['No'] = numbers[1]
                larger_numbers.append(numbers_dict)
            elif len(numbers) == 7:
                numbers_dict['Mean'] = numbers[0]
                numbers_dict['Median'] = numbers[1]
                numbers_dict['Strongly Disagree'] = numbers[2]
                numbers_dict['Disagree'] = numbers[3]
                numbers_dict['Neutral'] = numbers[4]
                numbers_dict['Agree'] = numbers[5]
                numbers_dict['Strongly Agree'] = numbers[6]
                larger_numbers.append(numbers_dict)
            elif len(numbers) == 8:
                numbers_dict['Mean'] = numbers[0]
                numbers_dict['Median'] = numbers[1]
                numbers_dict['Strongly Disagree'] = numbers[2]
                numbers_dict['Disagree'] = numbers[3]
                numbers_dict['Neutral'] = numbers[4]
                numbers_dict['Agree'] = numbers[5]
                numbers_dict['Strongly Agree'] = numbers[6]
                numbers_dict['N/A'] = numbers[7]
                larger_numbers.append(numbers_dict)
            else:
                larger_numbers.append("hello")
        else:
            larger_numbers.append(df[col][ind])
        
    df[col] = larger_numbers
df = df.drop("Course Evaluation Data", axis=1)
df.to_csv(subject + "_"+year+"_Cleaned.csv")