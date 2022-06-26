import pyttsx3

engine = pyttsx3.init()

engine.setProperty('rate', 150)
engine.setProperty('volume', 0.5)
# voices = engine.getProperty('voices')
engine.setProperty('voice', 'english-us')
# for voice in voices:
#     engine.setProperty('voice', voice.id)
#     print(voice.id)
#     # engine.say('The quick brown fox jumped over the lazy dog.')
#     engine.say("Hello, I am robot")
engine.say("Hello, I am robot")
engine.runAndWait()