import pandas as pd
import regex as re
subject = "CMSC"
year = "2022"
df = pd.read_csv(subject+ "_"+year+"_Cleaned_Image.csv")
for col in df.columns:
    responses = list()
    for ind in df.index:
        if any(re.findall(r'([0-9a-zA-Z <>.\-%]+) \(([0-9]+)\)', str(df[col][ind]))):
            response = re.findall(r'([0-9a-zA-Z <>.\-%]+) \(([0-9]+)\)', str(df[col][ind]))
            response_dict = dict()
            for x in response:
                if 'Total' not in str(x[0]):
                    response_dict[x[0]] = x[1]
            responses.append(response_dict)
            
        else:
            responses.append(df[col][ind])
    df[col] = responses
df = df.drop("Unnamed: 0.2", axis = 1)
df = df.drop("Unnamed: 0.1", axis = 1)
df = df.drop("Unnamed: 0", axis = 1)
df.to_csv(subject+ "_"+year+"_Cleaned_Images_Done.csv")
    