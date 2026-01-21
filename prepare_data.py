import pandas as pd

print("📥 Loading datasets...")

# Load files
df1 = pd.read_csv("backend/counsel_chat2.csv")
df2 = pd.read_csv("backend/counselchat-data.csv")

print("✅ Files loaded")

# Select columns
df1 = df1[['questionText', 'answerText']]
df2 = df2[['questionText', 'answerText']]

# Rename
df1.columns = ['user', 'bot']
df2.columns = ['user', 'bot']

print("✂ Cleaning done")

# Merge datasets
data = pd.concat([df1, df2])
data.dropna(inplace=True)

print("🔗 Merging completed")

# ---------------------------
# THERAPIST PROMPT ENGINEERING
# ---------------------------

final_rows = []

for _, row in data.iterrows():
    prompt = f"""
You are a kind, empathetic mental health companion.
Respond like a supportive therapist or close friend.
Avoid repeating yourself.
Ask thoughtful follow-up questions.

User: {row['user']}
Assistant:
"""

    final_rows.append({
        "text": prompt + row['bot']
    })

final_df = pd.DataFrame(final_rows)

# Save
final_df.to_csv("backend/final_train.csv", index=False)

print("\n🎉 SUCCESS!")
print("Saved as: backend/final_train.csv")
print("Total rows:", len(final_df))
