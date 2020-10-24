# -*- encoding: utf-8 -*-
import argparse

from flask import Flask, Blueprint, request # , jsonify
from flask_cors import CORS

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', action='store', default='127.0.0.1',
                        help='IP address')

    args = parser.parse_args()
    ip = str(args.ip)

    CORS(app)
    home = Blueprint('home_views', __name__)
    app.register_blueprint(home)
    app.run(host=ip, port=9002, debug=True)
