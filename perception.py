import json
import string
import random
import nltk
import numpy as num
from nltk.stem import WordNetLemmatizer # It has the ability to lemmatize.
import tensorflow as tensorF # A multidimensional array of elements is represented by this symbol.
from tensorflow.keras import Sequential # Sequential groups a linear stack of layers into a tf.keras.Model
from tensorflow.keras.layers import Dense, Dropout

nltk.download("punkt")# required package for tokenization
nltk.download("wordnet")# word database
nltk.download('omw-1.4')

data = {"intents": [
             {"tag": "age",
              "patterns": ["how old are you?"],
              "responses": ["I am 2 years old and my birthday was yesterday"]
             },
              {"tag": "greeting",
              "patterns": [ "Hi", "Hello", "Hey", "What’s up?", "Good morning", "Good afternoon", "Good evening"],
              "responses": ["Hi there", "Hello", "Hi :)"],
             },
              {"tag": "goodbye",
              "patterns": [ "Bye", "later", "have a nice day", "see you", "talk to you later"],
              "responses": ["Bye", "Take care", "have a nice day"]
             },
             {"tag": "thanks",
              "patterns": ["Thanks", "Thank you", "That's helpful"],
             "responses": ["Happy to help!", "Any time!", "My pleasure", "You're welcome", "No problem"]
             },
             {"tag": "name",
              "patterns": ["what's your name?", "who are you?"],
              "responses": ["I have no name yet", "You can give me one name and I will appreciate it", "Well, I'm the avatar of metaverse"]
             },
             {"tag": "question",
              "patterns": ["How are you?", "How’s it going?", "Are you well?"],
              "responses": ["Fine thanks, and you?", "I'm all right", "Good, thanks"]
             },
             {"tag": "schedule",
              "patterns": ["Whats your schedule?", "Is there any schedule available?", "What classes did you registered", "Schedule"],
              "responses": ["Yo no se pai"]
             },
             {"tag": "understanding",
              "patterns": ["Are you understanding your schedules?"],
              "responses": ["Understanding"]
             },
             {"tag": "UX",
              "patterns": ["How do you feel on UX Design?"],
              "responses": ["UX_Design"]
             },
             {"tag": "PM",
              "patterns": ["Are you confident on Projects management?"],
              "responses": ["Projects_management"]
             },
             {"tag": "MSDP",
              "patterns": ["Is Modern Sw Dev ok?"],
              "responses": ["Modern_SW_development_processes"]
             },
             {"tag": "AI_Intro",
              "patterns": ["Whats your prevision on AI_introduction?"],
              "responses": ["AI_introduction"]
             },


]}

lm = WordNetLemmatizer() #for getting words
# lists
ourClasses = []
newWords = []
documentX = []
documentY = []
# Each intent is tokenized into words and the patterns and their associated tags are added to their respective lists.
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        ournewTkns = nltk.word_tokenize(pattern)# tokenize the patterns
        newWords.extend(ournewTkns)# extends the tokens
        documentX.append(pattern)
        documentY.append(intent["tag"])


    if intent["tag"] not in ourClasses:# add unexisting tags to their respective classes
        ourClasses.append(intent["tag"])

newWords = [lm.lemmatize(word.lower()) for word in newWords if word not in string.punctuation] # set words to lowercase if not in punctuation
newWords = sorted(set(newWords))# sorting words
ourClasses = sorted(set(ourClasses))# sorting classes

trainingData = [] # training list array
outEmpty = [0] * len(ourClasses)
# bow model
for idx, doc in enumerate(documentX):
    bagOfwords = []
    text = lm.lemmatize(doc.lower())
    for word in newWords:
        bagOfwords.append(1) if word in text else bagOfwords.append(0)

    outputRow = list(outEmpty)
    outputRow[ourClasses.index(documentY[idx])] = 1
    trainingData.append([bagOfwords, outputRow])

random.shuffle(trainingData)
trainingData = num.array(trainingData, dtype=object)# coverting our data into an array afterv shuffling

x = num.array(list(trainingData[:, 0]))# first trainig phase
y = num.array(list(trainingData[:, 1]))# second training phase

iShape = (len(x[0]),)
oShape = len(y[0])
# parameter definition
ourNewModel = Sequential()
# In the case of a simple stack of layers, a Sequential model is appropriate

# Dense function adds an output layer
ourNewModel.add(Dense(128, input_shape=iShape, activation="relu"))
# The activation function in a neural network is in charge of converting the node's summed weighted input into activation of the node or output for the input in question
ourNewModel.add(Dropout(0.5))
# Dropout is used to enhance visual perception of input neurons
ourNewModel.add(Dense(64, activation="relu"))
ourNewModel.add(Dropout(0.3))
ourNewModel.add(Dense(oShape, activation = "softmax"))
# below is a callable that returns the value to be used with no arguments
md = tensorF.keras.optimizers.Adam(learning_rate=0.01, decay=1e-6)
# Below line improves the numerical stability and pushes the computation of the probability distribution into the categorical crossentropy loss function.
ourNewModel.compile(loss='categorical_crossentropy',
              optimizer=md,
              metrics=["accuracy"])
# Output the model in summary
print(ourNewModel.summary())
# Whilst training your Nural Network, you have the option of making the output verbose or simple.
ourNewModel.fit(x, y, epochs=200, verbose=1)
# By epochs, we mean the number of times you repeat a training set.

def ourText(text):
  newtkns = nltk.word_tokenize(text)
  newtkns = [lm.lemmatize(word) for word in newtkns]
  return newtkns

def wordBag(text, vocab):
  newtkns = ourText(text)
  bagOwords = [0] * len(vocab)
  for w in newtkns:
    for idx, word in enumerate(vocab):
      if word == w:
        bagOwords[idx] = 1
  return num.array(bagOwords)

def Pclass(text, vocab, labels):
  bagOwords = wordBag(text, vocab)
  ourResult = ourNewModel.predict(num.array([bagOwords]))[0]
  newThresh = 0.2
  yp = [[idx, res] for idx, res in enumerate(ourResult) if res > newThresh]

  yp.sort(key=lambda x: x[1], reverse=True)
  newList = []
  for r in yp:
    newList.append(labels[r[0]])
  return newList

def getRes(firstlist, fJson):
  tag = firstlist[0]
  listOfIntents = fJson["intents"]
  for i in listOfIntents:
    if i["tag"] == tag:
      ourResult = random.choice(i["responses"])
      break
  return ourResult

  