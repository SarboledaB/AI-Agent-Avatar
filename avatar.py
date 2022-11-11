from flask import Flask, request, jsonify
from flask_cors import CORS
import perception as model
import learning as learn_mdl
import project as avatar

from PIL import Image
import base64
import io
import numpy as np
import torch
import re
import random

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    newMessage = "Hello"
    intents = model.Pclass(newMessage, model.newWords, model.ourClasses)
    ourResult = model.getRes(intents, model.data)
    print(ourResult)
    return 'Working bitches'

@app.route('/perception', methods=['POST'])
def perception():
    response = {
        'type': '',
        'message': ''
    }
    try:
        message = request.json['message']
        intents = model.Pclass(message, model.newWords, model.ourClasses)
        response['type'] = True
        if (re.search("[0-9],[0-9],[0-9]", message)):
            message = message.split(',')
            avatar.result.input['worth'] = int(message[0])
            avatar.result.input['interest'] = int(message[1])
            avatar.result.input['teamwork'] = int(message[2])
            avatar.result.compute()
            print(avatar.result.output)
            response['message'] = 'I think my approximate grade would be around: %s' % (round(avatar.result.output['performance']/10,2))
            return response
        modelRes = model.getRes(intents, model.data)
        
        if (modelRes == "Yo no se pai"):
            schedule, score = avatar.Avatar.secondDeliverable()
            scheduleStr = []
            for h in schedule:
                subject, dayTime = h
                scheduleStr.append('Subject: %s, Schedule: %s, Score: %s' % (subject, str(dayTime[0]), dayTime[1]))
            scheduleStr.append('TOTAL SCORE: %i' % score)
            response['message'] = scheduleStr
        elif (modelRes == 'Understanding'):
            response['message'] = avatar.calcUnderstanding()
        else:
            print(modelRes)
            response['message'] = modelRes
    except Exception as ex:
        response["type"] = False
        response["message"] = str(ex)
    return jsonify(response)

@app.route('/learning', methods=['POST'])
def learning():
    response = {
        'type': '',
        'message': ''
    }
    image = request.json['image']
    dimensions = (128, 128)
    encoded_image = image.split(",")[1]
    decoded_image = base64.b64decode(encoded_image)

    ### APPROACH 1 (BROKEN):
    # ____________________
    # image is (302, 302)
    img = Image.open(io.BytesIO(decoded_image))
    # image is (28, 28)
    img = img.resize(dimensions, Image.ANTIALIAS)
    pixels = np.asarray(img, dtype='uint8')
    # force (28, 28)
    pixels = np.resize(pixels, (128,128))
    try:
        pred = learn_mdl.model.predict(pixels.reshape(1, 128, 128, 1))
        pred_gender = learn_mdl.gender_dict[round(pred[0][0][0])]
        pred_age = round(pred[1][0][0])
        response['type'] = True
        response['message'] = "Predicted Gender: %s \nPredicted Age: %s" % (pred_gender, pred_age)
    except Exception as ex:
        response["type"] = False
        response["message"] = str(ex)
    return jsonify(response)




if __name__ == '__main__':
    app.run(debug=True)