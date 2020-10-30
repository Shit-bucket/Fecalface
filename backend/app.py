# -*- encoding: utf-8 -*-
import argparse

from flask import Flask, Blueprint, request  # , jsonify
from flask_cors import CORS

import multiprocessing
import http.server
import socketserver

import modules.instagram.instagram_avatar as instagram
import modules.fecaldetect.fecaldetect as fecaldetect
import modules.fecalmakeup.fecalmakeup as fecalmakeup
import modules.fecalrecog.fecalrecog as fecalrecog


app = Flask(__name__)


################################################
# Instagram
################################################
@app.route("/instagram", methods=["POST"])
def r_instagram():
    json_result = request.get_json()
    username = json_result.get("username", "")
    lang = json_result.get("lang", "")
    print("Instagram - Detected Username : ", username, lang)
    result = instagram.t_instagram_avatar(username, lang)
    return result


################################################
# Fecaldetect
################################################
@app.route("/fecaldetect", methods=["POST"])
def r_detect():
    json_result = request.get_json()
    image_name = json_result.get("image_name", "")
    lang = json_result.get("lang", "")
    print("Fecaldetect - Detected image : ", image_name, lang)
    result = fecaldetect.t_detect_avatar(image_name, lang)
    return result


################################################
# Fecalmakeup
################################################
@app.route("/fecalmakeup", methods=["POST"])
def r_makeup():
    json_result = request.get_json()
    image_name = json_result.get("image_name", "")
    lang = json_result.get("lang", "")
    print("Fecalmakeup - Detected image : ", image_name, lang)
    result = fecalmakeup.t_makeup_avatar(image_name, lang)
    return result


################################################
# Fecalrecog
################################################
@app.route("/fecalrecog", methods=["POST"])
def r_recog():
    json_result = request.get_json()
    image_name = json_result.get("image_name", "")
    lang = json_result.get("lang", "")
    print("Fecalmakeup - Detected image : ", image_name, lang)
    result = fecalrecog.t_recog_avatar(image_name, lang)
    return result


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="../frontend/dis/", **kwargs)


def startHttpServer():
    PORT = 9001
    # TODO : Add directory validation
    with socketserver.TCPServer(("", PORT), Handler) as httpd_server:
        print("serving at port", PORT)
        httpd_server.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', action='store', default='127.0.0.1',
                        help='IP address')
    parser.add_argument('-e', '--env', action='store', default='dev',
                        help='Environment [dev, prod]')

    args = parser.parse_args()
    ip = str(args.ip)
    env = str(args.env)

    CORS(app)
    home = Blueprint('home_views', __name__)
    app.register_blueprint(home)

    if (env == "prod"):

        kwargs_flask = {"host": ip, "port": 9002}
        flask_proc = multiprocessing.Process(name='flask',
                                             target=app.run,
                                             kwargs=kwargs_flask)
        flask_proc.daemon = True

        httpd_proc = multiprocessing.Process(name='httpd',
            target=startHttpServer)
        httpd_proc.daemon = True

        httpd_proc.start()
        flask_proc.start()
        flask_proc.join()
        httpd_proc.join()
    else:
        app.run(host=ip, port=9002, debug=True)
