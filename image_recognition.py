import requests # request img from web
import shutil # save img locally
import pandas as pd
import PyPDF2
from PIL import Image
from pytesseract import pytesseract
subject = "CMSC"
year = "2022"
df = pd.read_csv(subject+"_"+year+"_Cleaned.csv")

for col in df.columns:
    data = list()
    for ind in df.index:
        if '.png' in str(df[col][ind]):
            url = df[col][ind] #prompt user for img url
            file_name = 'testing.png' #prompt user for file_name
            res = requests.get(url, stream = True)
            if res.status_code == 200:
                with open(file_name,'wb') as f:
                    shutil.copyfileobj(res.raw, f)
            else:
                print('Image Couldn\'t be retrieved')
            img = Image.open('testing.png')
            text = pytesseract.image_to_string(img)
            data.append(text)
        else:
            data.append(df[col][ind])
    df[col] = data
df.to_csv(subject+"_"+year+"_Cleaned_Image.csv")