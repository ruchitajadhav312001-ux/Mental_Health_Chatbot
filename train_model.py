from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset
import pandas as pd

print("📥 Loading MASTER dataset...")

df = pd.read_csv("MASTER_DATA.csv")

df["text"] = "User: " + df["user"] + "\nBot: " + df["bot"]

df[["text"]].to_csv("train_text.csv", index=False)

dataset = load_dataset("csv", data_files="train_text.csv")

print("🤖 Loading base model...")
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)

tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name)
model.resize_token_embeddings(len(tokenizer))


def tokenize(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        padding="max_length",
        max_length=256
    )

dataset = dataset.map(tokenize, batched=True)
dataset.set_format(type="torch", columns=["input_ids", "attention_mask"])

print("⚙ Training setup...")

training_args = TrainingArguments(
    output_dir="my_model",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-5,
    logging_steps=50,
    save_strategy="epoch",
    fp16=False,
    report_to="none"
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    data_collator=data_collator
)

print("🔥 Training started...")
trainer.train()

print("\n🎉 MODEL TRAINED SUCCESSFULLY!")

trainer.save_model("my_model")
tokenizer.save_pretrained("my_model")
