import os
from scipy import spatial
import numpy as np
import gensim
import nltk
from keras.models import load_model
from gtts import gTTS

import win32com.client as wincl


# This module is imported so that we can
# play the converted audio
import os


import theano

theano.config.optimizer = "None"
language = 'en'

model = load_model('LSTM5000.h5')
mod = gensim.models.Word2Vec.load('word2vec.bin');
while (True):
    x = input("Enter the message:");
    sentend = np.ones((300), dtype=np.float32)

    sent = nltk.word_tokenize(x.lower())
    sentvec = [mod[w] for w in sent if w in mod.wv.vocab]

    sentvec[14:] = []
    sentvec.append(sentend)
    if len(sentvec) < 15:
        for i in range(15 - len(sentvec)):
            sentvec.append(sentend)
    sentvec = np.array([sentvec])

    predictions = model.predict(sentvec)
    outputlist = [mod.most_similar([predictions[0][i]])[0][0] for i in range(15)]
    output = ' '.join(outputlist)
    print(output)
    # myobj = gTTS(text=output, lang=language, slow=False)
    #
    # # Saving the converted audio in a mp3 file named
    # # welcome
    # myobj.save("welcome.mp3")
    #
    # # Playing the converted file
    # os.system("welcome.mp3")
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(output)
