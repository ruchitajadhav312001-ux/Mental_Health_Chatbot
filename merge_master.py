import pandas as pd
import json
import ast

print("📥 Loading datasets...")

# 1) counsel_chat2.csv
df1 = pd.read_csv("counsel_chat2.csv")[['questionText','answerText']]
df2 = pd.read_csv("counselchat-data.csv")[['questionText','answerText']]
df1.columns = df2.columns = ['user','bot']

# 2) train.csv (conversation format)
df3_raw = pd.read_csv("train.csv")
rows3 = []

for convo in df3_raw['conversations']:
    try:
        messages = ast.literal_eval(convo)
        for i in range(len(messages)-1):
            if messages[i]['from']=="user" and messages[i+1]['from']=="assistant":
                rows3.append({
                    "user": messages[i]['value'],
                    "bot": messages[i+1]['value']
                })
    except:
        continue

df3 = pd.DataFrame(rows3)

# 3) mental_health_dataset.json (JSON LINES)
rows4 = []
with open("mental_health_dataset.json") as f:
    for line in f:
        try:
            i = json.loads(line)
            rows4.append({
                "user": i.get('text'),
                "bot": i.get('label')
            })
        except:
            continue

df4 = pd.DataFrame(rows4)

# 4) synthetic_mental_health_chatgroq.json (JSON LINES)
rows5 = []
with open("synthetic_mental_health_chatgroq.json") as f:
    for line in f:
        try:
            i = json.loads(line)
            rows5.append({
                "user": i.get('user'),
                "bot": i.get('assistant')
            })
        except:
            continue

df5 = pd.DataFrame(rows5)

# MERGE ALL
data = pd.concat([df1, df2, df3, df4, df5])

# CLEAN
data.dropna(inplace=True)
data.drop_duplicates(inplace=True)
data = data.sample(frac=1).reset_index(drop=True)

# SAVE
data.to_csv("MASTER_DATA.csv", index=False)

print("🎉 MERGE DONE SUCCESSFULLY!")
print("Total rows:", len(data))
