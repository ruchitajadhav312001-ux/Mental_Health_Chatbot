from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import random

model_path = "my_model"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)
model.eval()

print("\n🌟 Heyyy! I'm Serena 🤍")
print("Your friendly mental health chatbot!")
print("I'm so happy you're here 💬")
print("(Type 'exit' to stop)\n")


therapy_responses = {

"greeting": [
"Heyyy! 😊 I'm Serena! It's really nice to meet you!",
"Hii there! 🌸 I'm Serena, your supportive buddy!",
"Hello! 💖 I'm so glad you came to talk to me!",
"Hey friend! 🌈 Serena here! How are you feeling today?"
],

"sad": [
"Feeling sad can be really heavy, and I’m glad you shared it with me. You don’t have to pretend to be okay here. Whatever you’re feeling right now is valid. Sometimes life just feels overwhelming, but remember you don’t have to go through it alone. I’m right here with you.",
"It’s okay to feel low sometimes. You’ve been carrying a lot emotionally, and it makes sense that you feel tired. Please be gentle with yourself. You deserve care and understanding.",
"Sadness doesn’t mean you’re weak. It means you’re human. Let’s take this moment slowly together."
],

"alone": [
"Feeling alone can be deeply painful. Even when people are around, the heart can still feel empty. But please remember, you matter and your presence has value. I’m here with you right now.",
"You don’t deserve to feel abandoned. Sometimes people don’t show up the way we need, but that doesn’t reduce your worth.",
"It’s brave of you to share this. You don’t have to face things by yourself."
],

"friend": [
"Losing a friend can hurt like a breakup. It leaves questions, pain, and emptiness. I’m really sorry you’re going through this.",
"Friendship wounds can take time to heal. It’s okay to grieve the connection you had.",
"Do you want to talk about what happened between you two?"
],

"lonely": [
"Loneliness can feel overwhelming and silent. But you’re not invisible here. I see you.",
"Sometimes we feel disconnected even when we try our best. That doesn’t make you unlovable.",
"You matter more than you think."
],

"stress": [
"It sounds like you’re under a lot of pressure. Stress can drain both your mind and body.",
"You’ve been trying so hard, and that effort counts. One step at a time.",
"Take a slow breath with me. You’re doing okay."
],

"anxiety": [
"Anxiety can make your thoughts race and your heart feel heavy. It’s okay to feel this way.",
"Let’s ground you together. Look around and name 5 things you see.",
"This feeling will pass, even if it doesn’t feel like it right now."
],

"academics": [
"Academic pressure can feel overwhelming. You’re doing your best and that’s enough.",
"Marks don’t define your intelligence or your future.",
"Would you like help making a small study plan?"
],

"career": [
"Career uncertainty is scary, but everyone’s journey is different.",
"You’re not behind in life. You’re exactly where you need to be.",
"Tell me what worries you about your future."
],

"breakup": [
"Breakups hurt deeply. It can feel like part of you is missing.",
"It’s okay to miss someone even if they hurt you.",
"Healing takes time. Be patient with yourself."
],

"confidence": [
"You are stronger than you realize.",
"Your worth doesn’t depend on anyone else’s opinion.",
"What’s one small thing you like about yourself?"
],

"anger": [
"It’s okay to feel angry. Your emotions are valid.",
"Let’s try to release some of that tension safely.",
"Do you want to tell me what triggered it?"
],

"burnout": [
"You sound exhausted. Burnout is real and serious.",
"Please give yourself permission to rest.",
"You don’t have to be productive all the time."
],

"family": [
"Family problems can be really painful.",
"It’s hard when the people closest to us hurt us.",
"You deserve peace and understanding."
],

"money": [
"Financial stress can feel overwhelming.",
"You’re not alone in this struggle.",
"Would you like to talk about what worries you?"
],

"selfhate": [
"I’m really sorry you’re feeling this way about yourself.",
"You deserve kindness, especially from yourself.",
"You are not a failure."
],

"overthinking": [
"Overthinking can drain your energy.",
"Let’s bring your focus to the present moment.",
"One thought at a time."
],

"sleep": [
"Sleep issues can affect your mood a lot.",
"Try creating a calming night routine.",
"You deserve good rest."
],

"trauma": [
"Thank you for trusting me with this.",
"Trauma leaves deep marks, and healing takes time.",
"You are brave for surviving."
],

"suicidal": [
"I’m really glad you told me this. You matter so much.",
"You don’t have to go through this alone.",
"Please consider reaching out to someone you trust.",
"Kiran Helpline (India): 1800-599-0019",
"AASRA: 91-22-27546669"
],

"motivation": [
"You are stronger than you think.",
"Every small step matters.",
"Don’t give up on yourself."
],

"affirmation": [
"You are enough just as you are.",
"You deserve love and happiness.",
"I’m proud of you for trying."
],

"yoga": [
"Let’s slow everything down together. Sit comfortably, inhale deeply… hold… now exhale slowly. Repeat this 3 times.",
"Put one hand on your chest and breathe slowly. You are safe.",
"Close your eyes and count your breaths from 1 to 5 slowly."
],

"default": [
"I’m here to listen. Tell me more.",
"You don’t have to carry this alone.",
"Your feelings are valid."
],
"solutions": [
"Let’s try some simple steps together. First, take 3 slow deep breaths. Then, write down what’s bothering you and focus on one thing at a time. You don’t have to solve everything today.",
"A small solution can help. Try drinking water, moving your body a little, and taking a short break. Sometimes physical care helps mental peace.",
"You can try grounding: look around and name 5 things you see, 4 you can touch, 3 you hear. It helps calm your mind."
]
}


intent_keywords = {
"sad": ["sad","low","cry","hurt"],
"alone": ["alone","abandoned"],
"friend": ["friend","left"],
"lonely": ["lonely"],
"stress": ["stress","pressure"],
"anxiety": ["anxious","panic"],
"academics": ["exam","study","college"],
"career": ["job","career","placement"],
"breakup": ["breakup","relationship"],
"confidence": ["worthless","failure"],
"anger": ["angry","frustrated"],
"burnout": ["tired","burnout"],
"family": ["family","parents"],
"money": ["money","finance"],
"selfhate": ["hate myself"],
"overthinking": ["overthink"],
"sleep": ["sleep","insomnia"],
"trauma": ["trauma","abuse"],
"suicidal": ["suicidal","die","kill myself"],
"motivation": ["motivate"],
"affirmation": ["affirm"],
"yoga": ["relax","breathe","calm"]
}


def rule_based_reply(text):
    text = text.lower().strip()

    # Greeting only if user actually greets
    if text in ["hi", "hello", "hey", "hii"]:
        return random.choice(therapy_responses["greeting"])

    # Highest priority – crisis
    if any(w in text for w in ["suicidal", "die", "kill myself"]):
        return random.choice(therapy_responses["suicidal"])

    # Calm support
    if any(w in text for w in ["calm", "relax", "breathe", "panic"]):
        return random.choice(therapy_responses["yoga"])

    # Normal intent detection
    for intent, words in intent_keywords.items():
        for w in words:
            if w in text:
                return random.choice(therapy_responses[intent])

    return random.choice(therapy_responses["default"])


while True:
    user = input("You: ")

    if user.lower() == "exit":
        break

    prompt = f"User: {user}\nBot:"
    inputs = tokenizer(prompt, return_tensors="pt")

    try:
        output = model.generate(
            **inputs,
            max_new_tokens=40,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

        text = tokenizer.decode(output[0], skip_special_tokens=True)
        reply = text.split("Bot:")[-1].strip() if "Bot:" in text else ""

        if len(reply) < 5 or "!" in reply:
            reply = rule_based_reply(user)

    except:
        reply = rule_based_reply(user)

    print("\nSerena:", reply, "\n")
