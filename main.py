import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model

model = load_model('chatbot_model.h5')
import json
import random
from tkinter import *

# from googletrans import Translator
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
import pyttsx3

engine = pyttsx3.init()


# Language in which you want to convert
language = 'en'


# Passing the text and language to the engine,
# here we have marked slow=False. Which tells
# the module that the converted audio should
# have a high speed

from flask import Flask

app = Flask(__name__)


@app.route('/bot',methods=['GET'])
def hello():
  def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

  from googletrans import Translator
  from googletrans.gtoken import TokenAcquirer
  translator = Translator()
#flutter-chatbotapp54654
  def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_rec = translator.translate(sentence, dest='ar')
    reshaped_text = arabic_reshaper.reshape(sentence_rec.text)
    if (sentence_rec == 'ar'):
      arabic_reshaper.reshape(sentence_rec.text)
      rec_text = reshaped_text[::-1]
      rec_text = translator.translate(sentence, dest='en')
      sentence_words = clean_up_sentence(rec_text)
      print(rec_text)
      print(rec_text)
    else:
      sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
      for i, w in enumerate(words):
        if w == s:
          # assign 1 if current word is in the vocabulary position
          bag[i] = 1
          if show_details:
            print("found in bag: %s" % w)
    return (np.array(bag))

  def predict_class(sentence, model):  # ******
    # filter out predictions below a threshold

    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
      return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

  def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
      if (i['tag'] == tag):
        result = random.choice(i['responses'])
        break
    return result

  def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

  # Creating GUI with tkinter

  from googletrans import Translator
  import arabic_reshaper
  def send():
    msg = EntryBox.get("1.0", 'end-1c').strip()
    received = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)

    if msg != '':
      # make an object from translator
      translator = Translator()
      #
      ChatLog.config(state=NORMAL)

      receive = translator.translate(received, dest='ar')
      reshaped_text = arabic_reshaper.reshape(receive.text)
      if (receive.src == 'ar'):
        arabic_reshaper.reshape(receive.text)
        rec_text = reshaped_text[::-1]
        ChatLog.insert(END, "You: " + rec_text + '\n\n')
      else:

        ChatLog.insert(END, "You: " + msg + '\n\n')
      # make the object from translator detect the source of the enyered language
      FromUser = translator.translate(msg).src
      #
      ChatLog.config(foreground="#442265", font=("Verdana", 12))

      res = chatbot_response(msg)
      # make the destination language same as the source
      result = translator.translate(res, dest=FromUser)
      reshaped_text = arabic_reshaper.reshape(result.text)
      if (result.dest == 'ar'):
        arabic_reshaper.reshape(result.text)
        rev_text = reshaped_text[::-1]
        ChatLog.insert(END, "Bot: " + rev_text + '\n\n')
        # myobj = gTTS(text=result.text, lang='fr', slow=False)
        # myobj.save("welcome.mp3")
        # Playing the converted file
        # os.system("welcome.mp3")
      else:
        ChatLog.insert(END, "Bot: " + result.text + '\n\n')
        """
        say = result.text

        converter = pyttsx3.init()
        converter.setProperty('rate', 85)
        voice_id_Male = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
        voice_id_female = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

        # Use female voice
        converter.setProperty('voice', voice_id_female)
        engine.say(say)
        engine.runAndWait()
        # myobj = gTTS(text=result.text, lang='en', slow=False)
        # myobj.save("welcome.mp3")
      # Playing the converted file
      # os.system("welcome.mp3")
      #"""

      ChatLog.config(state=DISABLED)
      ChatLog.yview(END)

  base = Tk()
  base.title("MIU Chatbot")
  base.geometry("400x500")
  base.resizable(width=FALSE, height=FALSE)

  # Create Chat window
  ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial", )

  ChatLog.config(state=DISABLED)

  # Bind scrollbar to Chat window
  scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="hand1")
  ChatLog['yscrollcommand'] = scrollbar.set

  # Create Button to send message
  SendButton = Button(base, font=("Verdana", 12, 'bold'), text="Send", width="12", height=5,
                      bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff',
                      command=send)

  # Create the box to enter message
  EntryBox = Text(base, bd=0, bg="white", width="29", height="5", font="Arial")
  # EntryBox.bind("<Return>", send)

  # Place all components on the screen
  scrollbar.place(x=376, y=6, height=386)
  ChatLog.place(x=6, y=6, height=400, width=370)
  EntryBox.place(x=128, y=401, height=90, width=280)
  SendButton.place(x=6, y=401, height=90)

  return (base.mainloop())

if __name__== '__main__':
  app.run(debug=True)

