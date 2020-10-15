#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import json
import logging
import face_recognition
from PIL import Image, ImageDraw  # , ImageFont
import numpy as np

logging.basicConfig(level=logging.INFO)


def t_recog_avatar(image_name, lang="spanish"):
    """ Recognition face from avatar """

    directory = os.path.dirname(os.path.realpath(__file__))
    root_dir_idx = directory.find("backend")
    image_temp = os.path.join(directory[:root_dir_idx],
                              "backend/static/avatar")
    makeup_temp = os.path.join(directory[:root_dir_idx],
                               "backend/static/makeup")
    recog_temp = os.path.join(directory[:root_dir_idx],
                              "backend/static/recog")
    logging.info('Checking directories...')
    if (not os.path.isdir(image_temp)):
        os.makedirs(image_temp)
    if (not os.path.isdir(makeup_temp)):
        os.makedirs(makeup_temp)
    if (not os.path.isdir(recog_temp)):
        os.makedirs(recog_temp)

    logging.info('Face recognition...')
    known_image = face_recognition.load_image_file(image_temp + "/" +
                                                   image_name)
    known_image_encoding = face_recognition.face_encodings(known_image)[0]

    unknown_image = face_recognition.load_image_file(makeup_temp + "/" +
                                                     image_name)
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image,
                                                     face_locations)
    pil_image = Image.fromarray(unknown_image)
    pil_image = pil_image.convert("RGBA")
    draw = ImageDraw.Draw(pil_image)

    response = {'module': 'recog'}

    for (top, right, bottom, left), face_encoding in zip(
         face_locations, face_encodings):

        top += -20
        left += -10
        right += 10
        bottom += 10

        # TODO: Tolerance parameter
        matches = face_recognition.compare_faces([known_image_encoding],
                                                 face_encoding,
                                                 tolerance=0.40)
        name = "UNKNOWN"
        face_distances = face_recognition.face_distance([known_image_encoding],
                                                        face_encoding)
        print("Matches : {}".format(matches))
        print("Distance : {}".format(face_distances))
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = image_name.split(".")[0]

        response['matches'] = 'True' if matches else 'False'
        response['distance'] = 100 - face_distances[0] * 100
        response['name'] = name

    if (response['name'] == "UNKNOWN"):
        response['status'] = 'OK'
        if (lang == "english"):
            response['d1'] = 'UNKNOWN'
            response['d2'] = 'Not recognized'
            response['d3'] = 'The attacked face is not recognized from ' + \
                'the original image within a pre-set threshold (40%).<br>' + \
                'The result of the comparison between the original face' + \
                'and the attacked one is {}%.<br> This image can be ' + \
                'used as an avatar without being related ' + \
                'to its real face.'.format(response['distance'])
        else:
            response['d1'] = 'DESCONOCIDO'
            response['d2'] = 'No reconocido'
            response['d3'] = 'El rostro atacado no se reconoce respecto ' + \
                'de la imagen original dentro de umbral preestablecido ' + \
                '(40%).<br>El resultado de la comparación entre el rostro ' + \
                'original y el atacado es de {}%.<br> Esta imagen pued' + \
                'e ser utilizada como avatar sin que la misma se relacione' + \
                ' con su rostro verdadero.'.format(response['distance'])
    elif (response['name'] != "UNKNOWN"):
        response['status'] = 'OK'
        if (lang == "english"):
            response['d1'] = response['name']
            response['d2'] = 'Recognized'
            response['d3'] = 'The attacked face isn\'t bellow the pre-set ' + \
                'treeshold of 60% to be considered different from the ' + \
                'original. <br>It is not recommended to use this image ' + \
                'as an avatar because it can still be related to your ' + \
                'face.<br>The distance between both faces is ' + \
                '{}%.'.format(response['distance'])
        else:
            response['d1'] = response['name']
            response['d2'] = 'Reconocido'
            response['d3'] = 'El rostro atacado no esta por debajo del ' + \
                'umbral preestablecido de 60% para ser considerado ' + \
                'distinto al original. <br>No se recomienda utilizar esta ' + \
                'imagen como avatar porque puede aun ser relacionada con ' + \
                'su rostro.<br>La distancia entre ambos rostros es de ' + \
                '{}%.'.format(response['distance'])
        TINT_COLOR = (255, 40, 0)
        TRANSPARENCY = .50
        OPACITY = int(255 * TRANSPARENCY)
        overlay = Image.new('RGBA', pil_image.size, TINT_COLOR+(0,))
        draw = ImageDraw.Draw(overlay)
        width, height = pil_image.size
        draw.rectangle(((0, 0), (width, height)), fill=TINT_COLOR+(OPACITY,))
        pil_image = Image.alpha_composite(pil_image, overlay)
        pil_image = pil_image.convert("RGB")

        image_path = recog_temp + "/" + image_name
        pil_image.save(image_path)

        response["url_img"] = image_path[image_path.find("/static"):]
    else:
        response['status'] = 'Fail'
        response['d1'] = 'Unhandled error'
        response['d2'] = 'Unhandled error'
        response['d3'] = 'Unhandled error'
    return response


def output(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    image_name = sys.argv[1]
    result = t_recog_avatar(image_name)
    output(result)
