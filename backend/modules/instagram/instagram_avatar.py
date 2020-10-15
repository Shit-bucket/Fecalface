#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import json
import instaloader
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)


def t_instagram_avatar(username, lang="spanish"):
    """ Get avatar from instagram """

    directory = os.path.dirname(os.path.realpath(__file__))
    root_dir_idx = directory.find("backend")
    image_temp = os.path.join(directory[:root_dir_idx],
                              "backend/static/avatar")
    logging.info('Checking directory...{}'.format(image_temp))
    if (not os.path.isdir(image_temp)):
        os.makedirs(image_temp)

    L = instaloader.Instaloader()

    try:
        logging.info('Getting User info...')
        profile = instaloader.Profile.from_username(L.context, username)
    except instaloader.exceptions.ProfileNotExistsException:
        logging.error('User Not Found...')
        if (lang == "english"):
            response = {'module': 'source',
                        'submodule': 'instagram',
                        'status': 'Profile Not Found',
                        'd1': 'Profile not found',
                        'd2': 'The selected profile is not found',
                        'd3': 'Please make sure you have entered your ' +
                        'instagram username correctly to get the avatar ' +
                        'for your account.'}
        else:
            response = {'module': 'source',
                        'submodule': 'instagram',
                        'status': 'Profile Not Found',
                        'd1': 'Perfile inexistente',
                        'd2': 'El perfil seleccionado no se encuentra',
                        'd3': 'Asegúrese de haber ingresado correctamente ' +
                        'el nombre de usuario de instagram para obtener el ' +
                        'avatar correspondiente a la cuenta.'}
        return response

    logging.info('Getting User avatar...')
    if (profile.profile_pic_url):
        if (lang == "english"):
            response = {'module': 'source',
                        'submodule': 'instagram',
                        'status': 'Profile Ok',
                        'avatar_url': profile.profile_pic_url,
                        'username': profile.username,
                        'fullname': profile.full_name,
                        'd1': profile.full_name,
                        'd2': 'Avatar gather from instagram',
                        'd3': 'Through scraping the URL of the image ' +
                        'was obtained and downloaded the avatar to continue ' +
                        'with the process of face detection'}
        else:
            response = {'module': 'source',
                        'submodule': 'instagram',
                        'status': 'Profile Ok',
                        'avatar_url': profile.profile_pic_url,
                        'username': profile.username,
                        'fullname': profile.full_name,
                        'd1': profile.full_name,
                        'd2': 'Avatar obtenido de instagram',
                        'd3': 'A traves del scraping se obtuvo la URL de la ' +
                        'imagen y se descargo para continuar con el proceso ' +
                        'de deteccion de rostro'}
    else:
        logging.error('Avatar Not Found...')
        response = {'module': 'source',
                    'submodule': 'instagram',
                    'status': 'Avatar Not Found',
                    'd1': 'Avatar not found',
                    'd2': 'Avatar not found',
                    'd3': 'Avatar not found'}

    try:
        backend_img = image_temp + "/" + profile.username
        L.download_pic(backend_img, profile.profile_pic_url, datetime.now(),
                       _attempt=2)
        logging.info('Downloaded... {}'.format(profile.username))
        response["backend_img"] = backend_img + ".jpg"
        response["url_img"] = backend_img[backend_img.find("/static"):] + \
            ".jpg"
    except:
        logging.error('Downloaded... ERROR - {}'.format(profile.username))

    return response


def output(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    username = sys.argv[1]
    result = t_instagram_avatar(username)
    output(result)
