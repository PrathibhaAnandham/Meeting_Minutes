from gtts import gTTS

text = """అందరికి నమస్తే.

ఈ రోజు నేను చెప్పబోయే ప్రాజెక్ట్ పేరు "ఆటోమేటెడ్ మీటింగ్ మినిట్స్ జనరేటర్". ఈ ప్రాజెక్ట్ చాలా ఉపయోగపడేలా ఉంది, ముఖ్యంగా మీటింగ్‌లు జరిగే చోట్ల...


"""

tts = gTTS(text=text, lang='te')
tts.save("telugu_meeting.mp3")

print("Audio file saved as telugu_meeting.mp3")
