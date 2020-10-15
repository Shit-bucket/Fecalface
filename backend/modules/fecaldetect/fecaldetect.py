#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import json
import logging
import face_recognition
from PIL import Image

logging.basicConfig(level=logging.INFO)


def t_detect_avatar(image_name, lang="spanish"):
    """ Detect face from avatar """

    directory = os.path.dirname(os.path.realpath(__file__))
    root_dir_idx = directory.find("backend")
    image_temp = os.path.join(directory[:root_dir_idx],
                              "backend/static/avatar")
    face_temp = os.path.join(directory[:root_dir_idx], "backend/static/face")
    logging.info('Checking directories...')
    if (not os.path.isdir(image_temp)):
        os.makedirs(image_temp)
    if (not os.path.isdir(face_temp)):
        os.makedirs(face_temp)

    logging.info('Face detection...')
    image = face_recognition.load_image_file(image_temp + "/" + image_name)
    face_locations = face_recognition.face_locations(image)

    if (len(face_locations) == 0):
        logging.warning('Face Not Found...')
        if (lang == "english"):
            response = {'module': 'detect',
                        'status': 'Face Not Found',
                        'd1': 'Face not found',
                        'd2': 'This avatar hasn\'t face',
                        'd3': 'This avatar hasn\'t a face, maybe this ' +
                        'can\'t detect it, maybe there isn\'t a face.' +
                        '<br>Anyway, CONGRATULATIONS!'}
        else:
            response = {'module': 'detect',
                        'status': 'Face Not Found',
                        'd1': 'Rostro no encontrado',
                        'd2': 'Este avatar no tiene rostro',
                        'd3': 'Este avatar no tiene rostro, tal vez no ' +
                        'podemos detectarlo, tal vez no haya un rostro.' +
                        '<br>De cualquier manera FELICITACIONES!'}
    elif (len(face_locations) > 1):
        logging.warning('More than one face...')
        if (lang == "english"):
            response = {'module': 'detect',
                        'status': 'Too many Faces',
                        'd1': 'Too many faces',
                        'd2': 'This avatar has too many faces',
                        'd3': 'This program cannot process more than one ' +
                        'face because its objective is to attack the ' +
                        'face present in the avatar and it needs to be ' +
                        'able to identify it. We recommend changing your ' +
                        'avatar even if you are sharing the picture ' +
                        'with a loved one.'}
        else:
            response = {'module': 'detect',
                        'status': 'Too many Faces',
                        'd1': 'Demasiados rostros',
                        'd2': 'Este avatar tiene más de un rostro',
                        'd3': 'Este programa no puede procesar más de una ' +
                        'cara porque su objetivo es atacar la cara presente ' +
                        'en el avatar y necesita poder identificarla.<br>' +
                        'Recomendamos cambiar su avatar incluso si esta ' +
                        'compartiendo la fotografia con un familiar querido.'}
    else:
        logging.info('Face detected...')
        face_encodings = face_recognition.face_encodings(image, face_locations)
        response = {'module': 'detect',
                    'status': 'Face detected',
                    'd1': 'Face detected'}

        for (top, right, bottom, left), face_encoding in zip(
             face_locations, face_encodings):
            response['coord'] = {'top': top, 'right': right,
                                 'bottom': bottom, 'left': left}
            top += -10
            left += -10
            right += 10
            bottom += 10
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        image_path = face_temp + "/" + image_name
        pil_image.save(image_path)
        response["url_img"] = image_path[image_path.find("/static"):]
        response["d2"] = "( {}, {}, {}, {} )".format(top, right,
                                                     bottom, left)

        if (lang == "english"):
            response["d3"] = "A face was detected in the avatar and " + \
                             "the coordinates shown above belong to the " + \
                             "to the location of the face in the " + \
                             "avatar photo."
        else:
            response["d3"] = "Se detecto un rostro en el avatar y las " + \
                             "coordenadas mostradas arriba pertenecen a " + \
                             "la ubicación del rostro en la foto del avatar"
    return response


def output(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    image_name = sys.argv[1]
    result = t_detect_avatar(image_name)
    output(result)
