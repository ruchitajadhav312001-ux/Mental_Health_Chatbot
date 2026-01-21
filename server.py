from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Chat(BaseModel):
    message: str

# ---------------- THERAPIST RESPONSES ----------------

responses = {

"greeting": [
"Heyyy 🤍 I'm Serena. I'm really glad you're here today. You don't have to pretend to be okay here. How are you truly feeling right now?",

"Hi 🌸 Take your time, there’s no rush. I’m here to listen and support you. What’s been on your mind lately?",

"Hello friend 🌈 This is a safe space for you. You can share anything without fear of judgment."
],

"sadness": [
"I'm really sorry you're feeling this way. When sadness stays too long, it feels heavy on the heart and mind. You don’t have to carry this alone. I’m here to walk through it with you. What do you think started this feeling?",

"It sounds like you're hurting inside, and that pain is very real. Anyone in your place would feel this way. You deserve care, understanding, and kindness — especially from yourself.",

"Feeling sad doesn't make you weak, it makes you human. Emotions are part of being alive. You’re allowed to feel this way, and you’re not a burden for sharing it."
],

"anxiety": [
"Anxiety can make your mind race with thoughts that feel uncontrollable. Let’s slow it down together. Try focusing on your breathing for a moment. You are safe right now.",

"Take a deep breath with me. Inhale slowly… hold it for a few seconds… now exhale gently. Repeat this a few times. Your body needs reassurance.",

"Anxiety can feel scary, but remember — feelings are temporary. This moment will pass. You are stronger than this wave."
],

"breakup": [
"Breakups hurt deeply. Losing someone you cared about can feel like losing a part of yourself. It’s okay to grieve this connection.",

"It’s completely normal to miss them, even if things ended badly. Healing isn’t linear. Some days will feel heavier than others.",

"Do you want to share what happened between you two? I’m here to listen without judging."
],

"loneliness": [
"Feeling lonely can be painful, even when people are around. It can feel like no one truly understands you.",

"You are not invisible here. I see you, I hear you, and your feelings matter.",

"Loneliness doesn’t mean you are unlovable. Sometimes we just need deeper connections."
],

"academics": [
"Academic pressure can feel overwhelming, especially when expectations are high. Remember, your marks do not define your intelligence.",

"It’s okay to feel stressed about studies. Would you like help creating a small, manageable study plan?",

"You are doing your best, and that’s enough."
],

"placement": [
"Placement stress is scary, I understand. Uncertainty about the future can feel overwhelming.",

"Everyone’s journey is different. Just because someone else got placed earlier doesn’t mean you are behind.",

"What worries you the most about your career right now?"
],

"family": [
"Family problems hurt deeply because they come from people closest to our heart.",

"It’s hard when people who should support us end up hurting us. Your pain is valid.",

"You deserve peace and emotional safety."
],

"money": [
"Financial stress can feel suffocating. Worrying about money drains emotional energy.",

"You are not alone in this struggle. Many people face this, even if they don’t talk about it.",

"If you’re comfortable, tell me what worries you most."
],

"burnout": [
"You sound exhausted. Burnout happens when you push yourself too hard for too long.",

"You don’t have to be productive every day. Rest is not laziness, it’s necessary.",

"Please be gentle with yourself. Your body and mind deserve care."
],

"trauma": [
"Thank you for trusting me with something so personal. That takes courage.",

"Trauma leaves deep scars, but healing is possible, even if it feels slow.",

"You survived something difficult, and that shows strength."
],

"motivation": [
"You are stronger than you think, even if you don’t feel it right now.",

"Small progress is still progress. Don’t underestimate yourself.",

"Your future needs you. Please don’t give up."
],

"affirmations": [
"You are enough just as you are. You don’t need to prove your worth.",

"You deserve love, respect, and happiness.",

"I’m proud of you for trying, even when it’s hard."
],

"yoga": [
"Let’s breathe together. Sit comfortably. Inhale slowly through your nose… hold… now exhale gently through your mouth.",

"Put one hand on your chest and feel your breath. You are safe in this moment.",

"Close your eyes and count your breaths from 1 to 5 slowly."
],

"solutions": [
"Let’s take this step by step. First, take 3 slow deep breaths. Then drink some water. Finally, write down what’s bothering you. Small steps make big difference.",

"Try grounding: name 5 things you see, 4 you touch, 3 you hear. This brings your mind to the present.",

"A short walk, stretching your body, or listening to calm music can help clear your thoughts."
],

"suicidal": [
"I'm really glad you told me this. Your life matters so much, even if you don’t feel it right now.",

"First, let’s focus on keeping you safe:\n• Move away from harmful objects\n• Stay near someone\n• Don’t isolate yourself",

"📞 Please reach out now:\nKiran Helpline (India): 1800-599-0019\nAASRA: 91-22-27546669\nThey really care and will listen to you."
],

"default": [
"I'm here to listen. You can share anything with me.",
"You don’t have to carry this alone.",
"Your feelings are valid. Tell me more."
]
}

# ---------------- INTENT DETECTOR ----------------

def therapist_reply(msg):

    m = msg.lower()

    if any(w in m for w in ["hi","hello","hey","hii"]):
        return random.choice(responses["greeting"])

    if any(w in m for w in ["sad","cry","low","hurt"]):
        return random.choice(responses["sadness"])

    if any(w in m for w in ["anx","panic","nervous"]):
        return random.choice(responses["anxiety"])

    if any(w in m for w in ["breakup","left","relationship"]):
        return random.choice(responses["breakup"])

    if any(w in m for w in ["lonely","alone"]):
        return random.choice(responses["loneliness"])

    if any(w in m for w in ["exam","study","college"]):
        return random.choice(responses["academics"])

    if any(w in m for w in ["placement","job","career"]):
        return random.choice(responses["placement"])

    if "family" in m:
        return random.choice(responses["family"])

    if any(w in m for w in ["money","finance"]):
        return random.choice(responses["money"])

    if any(w in m for w in ["burnout","tired","exhausted"]):
        return random.choice(responses["burnout"])

    if any(w in m for w in ["trauma","abuse"]):
        return random.choice(responses["trauma"])

    if any(w in m for w in ["motivate","give up"]):
        return random.choice(responses["motivation"])

    if any(w in m for w in ["affirm","confidence","worth"]):
        return random.choice(responses["affirmations"])

    if any(w in m for w in ["relax","breathe","calm"]):
        return random.choice(responses["yoga"])

    if any(w in m for w in ["solution","what should i do","help me"]):
        return random.choice(responses["solutions"])

    # 🚨 CRISIS SAFE
    if any(w in m for w in ["suicidal","die","kill myself","end my life"]):
        return random.choice(responses["suicidal"])

    return random.choice(responses["default"])

# ---------------- API ----------------

@app.post("/chat")
def chat(req: Chat):
    reply = therapist_reply(req.message)
    return {"reply": reply}
