
import joblib
import pandas as pd
import json
import re

print('load model')
clf = joblib.load('decisiontree_API Frequency_gea.model')

with open('output/api_frequencies.json', 'r') as f:
    data = json.load(f)

for column in data:
    for cell in column:
        cell = re.sub('[^A-Za-z0-9_]+', '_', str(cell))

df = pd.DataFrame(data[1:], columns=data[0])
df = df.replace([None, 'Nan', 'None', 'unknown' ''], 0)

# 説明変数と目的変数に分ける
# 説明変数: (API Usage, API Frequency, API Sequence)
# 目的変数: (benign/malicious)
tmp = df.sample()
tmp_x = tmp.iloc[:, :-1]
tmp_y = df.iloc[:, -1].astype('int')

print(f"predicted: {clf.predict(tmp_x)}, want: {tmp_y}")
