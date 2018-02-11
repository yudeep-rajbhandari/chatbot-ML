import os
from scipy import spatial
import numpy as np
import gensim
import nltk
from keras.models import load_model

import re

import win32com.client as wincl


# This module is imported so that we can
# play the converted audio
import os


import theano

def untokenize(words):

    text = ' '.join(words)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
         "can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    return step6.strip()


language = 'en'
os.environ["KERAS_BACKEND"] = "theano"
model = load_model('LSTM2000.h5')
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
    # print(output)
    word_tokens=nltk.word_tokenize(output.lower())
    # print(finaloutput)
    stop_words = set(('kleiser', 'karluah'))
    filtered_sentence = [w for w in word_tokens if not w in stop_words]



    # for w in word_tokens:
    #     if w not in stop_words:
    #         filtered_sentence.append(w)


    # print(filtered_sentence)


    finaloutput1 =untokenize(filtered_sentence)
    # finaloutput1="".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in filtered_sentence]).strip()

    print(finaloutput1)



